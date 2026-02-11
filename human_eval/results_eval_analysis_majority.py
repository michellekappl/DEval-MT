import pandas as pd
import json
from collections import defaultdict, Counter
import csv
import numpy as np
import krippendorff
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class SummaryStatistics:
    """Container for summary statistics."""
    total_sentences: int = 0
    match_original: int = 0
    match_new: int = 0
    with_adj_match_original: int = 0
    with_adj_match_new: int = 0
    without_adj_match_original: int = 0
    without_adj_match_new: int = 0
    match_yes: int = 0
    makesense_yes: int = 0
    # Track total sentences with/without adjectives for correct percentages
    total_with_adj: int = 0
    total_without_adj: int = 0


class MajorityVoteAnalyzer:
    """Analyzes gender evaluation results using majority voting."""
    
    GENDER_MAP = {'MASCULINE': 'm', 'FEMININE': 'f', 'UNKNOWN': 'u', 'DIVERSE': 'n', 
                  'NEUTRAL': 'n', 'm': 'm', 'f': 'f', 'n': 'n', 'u': 'u'}
    
    def __init__(self, csv_file: str, num_sentences: int = 100):
        self.csv_file = csv_file
        self.num_sentences = num_sentences
        self.df = pd.read_csv(csv_file)
        
        # Extract language and date from filename
        import re
        match = re.search(r'human_eval_([a-z]+)_results_([0-9]+)\.csv', csv_file)
        if match:
            self.language = match.group(1)
            self.date = match.group(2)
        else:
            self.language = csv_file.replace("human_eval_", "").replace("_results.csv", "")
            self.date = None
        
        # Compute majority votes for each sentence
        self.majority_votes = self._compute_majority_votes()
        
        # Get number of participants from first row
        self.num_participants = self._get_num_participants()
        
        # Calculate inter-annotator agreement
        self.alpha, self.iaa_stats = self._compute_krippendorff_alpha()
        
        # Compute summary statistics
        self.summary_by_translator = self._compute_summary()
        self.summary_by_translator_filtered = self._compute_summary(filter_makesense=True)
        
        # Compute mismatches
        self.mismatches = self._compute_mismatches()
        self.mismatches_filtered = self._compute_mismatches(filter_makesense=True)
        
        # Computed properties
        self.sentences_with_adjective = len(self.df[self.df['has_adjective'] == True])
        self.sentences_without_adjective = self.num_sentences - self.sentences_with_adjective
    
    def _parse_json_list(self, value: str) -> List:
        """Parse JSON string safely."""
        try:
            return json.loads(value.replace("'", '"'))
        except:
            return []
    
    def _get_num_participants(self) -> int:
        """Extract number of participants from first valid gender list."""
        for _, row in self.df.iterrows():
            gender_list = self._parse_json_list(row['gender'])
            if gender_list:
                return len(gender_list)
        return 0
    
    def _compute_krippendorff_alpha(self) -> Tuple[float, Dict]:
        """Calculate Krippendorff's alpha for inter-annotator agreement."""
        all_items = []
        for _, row in self.df.iterrows():
            gender_list = self._parse_json_list(row['gender'])
            if gender_list:
                all_items.append(gender_list)
        
        if not all_items:
            return None, {}
        
        num_items = len(all_items)
        num_annotators = len(all_items[0])
        
        # Map to numeric codes
        gender_to_num = {'m': 1, 'f': 2, 'n': 3, 'u': 4}
        data_matrix = np.zeros((num_items, num_annotators))
        for i, gender_list in enumerate(all_items):
            for j, gender in enumerate(gender_list):
                data_matrix[i, j] = gender_to_num.get(gender, 4)
        
        alpha = krippendorff.alpha(reliability_data=data_matrix.T, level_of_measurement='nominal')
        
        # Count full agreement
        agreement_count = sum(1 for i in range(num_items) if len(set(data_matrix[i, :])) == 1)
        
        return alpha, {
            'alpha': alpha,
            'num_items': num_items,
            'num_annotators': num_annotators,
            'full_agreement_count': agreement_count,
            'full_agreement_pct': (agreement_count / num_items * 100) if num_items > 0 else 0
        }
    
    def _majority_vote(self, values: List) -> str:
        """Return the majority value, or 'u' (unknown) if there's a tie."""
        if not values:
            return 'u'
        
        counter = Counter(values)
        most_common = counter.most_common(2)
        
        # Check for tie
        if len(most_common) > 1 and most_common[0][1] == most_common[1][1]:
            return 'u'  # Tie - mark as unknown
        
        return most_common[0][0]
    
    def _compute_majority_votes(self) -> List[Dict]:
        """Compute majority vote for each sentence."""
        majority_data = []
        
        for _, row in self.df.iterrows():
            gender_list = self._parse_json_list(row['gender'])
            match_list = self._parse_json_list(row['match'])
            makesense_list = self._parse_json_list(row['makesense'])
            
            # Get majority votes
            majority_gender = self._majority_vote(gender_list)
            majority_match = self._majority_vote(match_list)
            majority_makesense = self._majority_vote(makesense_list)
            
            # Convert genders to single letter
            orig_letter = self.GENDER_MAP.get(row['original_gender'], 'u')
            new_letter = self.GENDER_MAP.get(row['gender_new_alignment'], 'u')
            old_letter = self.GENDER_MAP.get(row['gender_old_alignment'], 'u')
            
            majority_data.append({
                'csv_index': row['index'],
                'translator': row['translator'],
                'majority_gender': majority_gender,
                'majority_match': majority_match,
                'majority_makesense': majority_makesense,
                'original_gender': orig_letter,
                'new_alignment': new_letter,
                'old_alignment': old_letter,
                'has_adjective': row.get('has_adjective', False)
            })
        
        return majority_data
    
    def _compute_summary(self, filter_makesense: bool = False) -> Dict[str, SummaryStatistics]:
        """Compute summary statistics by translator using majority votes."""
        summary = defaultdict(SummaryStatistics)
        
        for vote_data in self.majority_votes:
            # Skip if filtering and majority makesense != 'yes'
            if filter_makesense and vote_data['majority_makesense'] != 'yes':
                continue
            
            translator = vote_data['translator']
            stats = summary[translator]
            
            stats.total_sentences += 1
            
            # Track adjective counts
            if vote_data['has_adjective']:
                stats.total_with_adj += 1
            else:
                stats.total_without_adj += 1
            
            # Check matches
            if vote_data['majority_gender'] == vote_data['original_gender']:
                stats.match_original += 1
                if vote_data['has_adjective']:
                    stats.with_adj_match_original += 1
                else:
                    stats.without_adj_match_original += 1
            
            if vote_data['majority_gender'] == vote_data['new_alignment']:
                stats.match_new += 1
                if vote_data['has_adjective']:
                    stats.with_adj_match_new += 1
                else:
                    stats.without_adj_match_new += 1
            
            if vote_data['majority_match'] == 'yes':
                stats.match_yes += 1
            
            if vote_data['majority_makesense'] == 'yes':
                stats.makesense_yes += 1
        
        return dict(summary)
    
    def _compute_mismatches(self, filter_makesense: bool = False) -> List[Dict]:
        """Identify cases where majority vote doesn't match new alignment."""
        mismatches = []
        
        for vote_data in self.majority_votes:
            # Skip if filtering and majority makesense != 'yes'
            if filter_makesense and vote_data['majority_makesense'] != 'yes':
                continue
            
            if vote_data['majority_gender'] != vote_data['new_alignment']:
                mismatches.append({
                    'csv_index': vote_data['csv_index'],
                    'translator': vote_data['translator'],
                    'majority_gender': vote_data['majority_gender'],
                    'original': vote_data['original_gender'],
                    'new_alignment': vote_data['new_alignment'],
                    'old_alignment': vote_data['old_alignment'],
                    'has_adjective': vote_data['has_adjective']
                })
        
        return mismatches
    
    def _calculate_totals(self, summary_dict: Dict) -> Dict:
        """Calculate total statistics across all translators."""
        return {
            'total_sentences': sum(s.total_sentences for s in summary_dict.values()),
            'match_original': sum(s.match_original for s in summary_dict.values()),
            'match_new': sum(s.match_new for s in summary_dict.values()),
            'with_adj_match_original': sum(s.with_adj_match_original for s in summary_dict.values()),
            'with_adj_match_new': sum(s.with_adj_match_new for s in summary_dict.values()),
            'without_adj_match_original': sum(s.without_adj_match_original for s in summary_dict.values()),
            'without_adj_match_new': sum(s.without_adj_match_new for s in summary_dict.values()),
            'match_yes': sum(s.match_yes for s in summary_dict.values()),
            'makesense_yes': sum(s.makesense_yes for s in summary_dict.values()),
            'total_with_adj': sum(s.total_with_adj for s in summary_dict.values()),
            'total_without_adj': sum(s.total_without_adj for s in summary_dict.values()),
        }
    
    def _calculate_percentages(self, totals: Dict, total_sentences: int) -> Dict:
        """Calculate percentage values."""
        return {
            'match_original': (totals['match_original'] / total_sentences * 100) if total_sentences > 0 else 0,
            'match_new': (totals['match_new'] / total_sentences * 100) if total_sentences > 0 else 0,
            'match_yes': (totals['match_yes'] / total_sentences * 100) if total_sentences > 0 else 0,
            'makesense_yes': (totals['makesense_yes'] / total_sentences * 100) if total_sentences > 0 else 0,
            # Divide by total sentences with adjectives (in this filtered set)
            'with_adj_orig': (totals['with_adj_match_original'] / totals['total_with_adj'] * 100) if totals['total_with_adj'] > 0 else 0,
            'with_adj_new': (totals['with_adj_match_new'] / totals['total_with_adj'] * 100) if totals['total_with_adj'] > 0 else 0,
            # Divide by total sentences without adjectives (in this filtered set)
            'without_adj_orig': (totals['without_adj_match_original'] / totals['total_without_adj'] * 100) if totals['total_without_adj'] > 0 else 0,
            'without_adj_new': (totals['without_adj_match_new'] / totals['total_without_adj'] * 100) if totals['total_without_adj'] > 0 else 0,
        }
    
    def print_summary(self):
        """Print comprehensive summary table."""
        # Print all data results
        self._print_summary_table("ALL DATA (Majority Vote)", self.summary_by_translator)
        
        # Calculate percentages for all data (for comparison)
        totals_all = self._calculate_totals(self.summary_by_translator)
        percentages_all = self._calculate_percentages(totals_all, totals_all['total_sentences'])
        
        # Print filtered results
        print("\n\n")
        totals_filtered = self._calculate_totals(self.summary_by_translator_filtered)
        self._print_summary_table("FILTERED (Majority makesense='yes')", 
                                 self.summary_by_translator_filtered,
                                 comparison_percentages=percentages_all)
    
    def _print_summary_table(self, title: str, summary_dict: Dict, comparison_percentages=None):
        """Helper method to print a summary table."""
        totals = self._calculate_totals(summary_dict)
        percentages = self._calculate_percentages(totals, totals['total_sentences'])
        
        print("\n" + "="*160)
        print(f"GENDER MATCH SUMMARY BY TRANSLATOR ({self.language}) - {title}")
        print("="*160)
        print(f"Total sentences: {totals['total_sentences']} (based on majority vote from {self.num_participants} participants)")
        print(f"Sentences with adjective: {totals['total_with_adj']} | Sentences without adjective: {totals['total_without_adj']}")
        print("-"*160)
        if self.alpha is not None:
            print(f"Inter-Annotator Agreement (Krippendorff's Alpha): {self.alpha:.4f}")
            print(f"Full agreement (all annotators agree): {self.iaa_stats['full_agreement_count']}/{self.iaa_stats['num_items']}")
        print("="*160)
        print(f"{'Translator':<15} {'Total':<8} {'Match Orig':<12} {'Match New':<10} {'Expression match':<12} {'Makes Sense Yes':<17} {'With Adj':<10} {'Without Adj':<20}")
        print(f"{'':15} {'':8} {'':12} {'':12} {'':10} {'':21} {'Orig|New':<14} {'Orig|New':<20}")
        print("-"*160)
        
        for translator, stats in sorted(summary_dict.items()):
            with_adj = f"{stats.with_adj_match_original}|{stats.with_adj_match_new}"
            without_adj = f"{stats.without_adj_match_original}|{stats.without_adj_match_new}"
            print(f"{translator:<18} {stats.total_sentences:<10} {stats.match_original:<12} {stats.match_new:<12} {stats.match_yes:<15} {stats.makesense_yes:<12} {with_adj:<14} {without_adj:<20}")
        
        print("-"*160)
        with_adj_total = f"{totals['with_adj_match_original']}|{totals['with_adj_match_new']}"
        without_adj_total = f"{totals['without_adj_match_original']}|{totals['without_adj_match_new']}"
        print(f"{'TOTAL':<18} {totals['total_sentences']:<10} {totals['match_original']:<12} {totals['match_new']:<12} {totals['match_yes']:<15} {totals['makesense_yes']:<12} {with_adj_total:<14} {without_adj_total:<20}")
        
        with_adj_pct = f"{percentages['with_adj_orig']:.1f}%|{percentages['with_adj_new']:.1f}%"
        without_adj_pct = f"{percentages['without_adj_orig']:.1f}%|{percentages['without_adj_new']:.1f}%"
        print(f"{'%':<18} {'':10} {percentages['match_original']:.1f}%{'':<8} {percentages['match_new']:.1f}%{'':<8} {percentages['match_yes']:.1f}%{'':<11} {percentages['makesense_yes']:.1f}%{'':<8} {with_adj_pct:<10} {without_adj_pct:<20}")
        
        # If comparison percentages provided, show the difference
        if comparison_percentages:
            diff_orig = percentages['match_original'] - comparison_percentages['match_original']
            diff_new = percentages['match_new'] - comparison_percentages['match_new']
            diff_match = percentages['match_yes'] - comparison_percentages['match_yes']
            diff_makesense = percentages['makesense_yes'] - comparison_percentages['makesense_yes']
            diff_with_adj_orig = percentages['with_adj_orig'] - comparison_percentages['with_adj_orig']
            diff_with_adj_new = percentages['with_adj_new'] - comparison_percentages['with_adj_new']
            diff_without_adj_orig = percentages['without_adj_orig'] - comparison_percentages['without_adj_orig']
            diff_without_adj_new = percentages['without_adj_new'] - comparison_percentages['without_adj_new']
            
            with_adj_diff = f"{diff_with_adj_orig:+.1f}%|{diff_with_adj_new:+.1f}%"
            without_adj_diff = f"{diff_without_adj_orig:+.1f}%|{diff_without_adj_new:+.1f}%"
            print(f"{'Δ vs ALL':<18} {'':10} {diff_orig:+.1f}%{'':<8} {diff_new:+.1f}%{'':<8} {diff_match:+.1f}%{'':<11} {diff_makesense:+.1f}%{'':<8} {with_adj_diff:<10} {without_adj_diff:<20}")
        
        print("="*160)
    
    def print_mismatches(self):
        """Print detailed mismatch information."""
        self._print_mismatch_table("ALL DATA", self.mismatches)
        print("\n\n")
        self._print_mismatch_table("FILTERED (Majority makesense='yes')", self.mismatches_filtered)
    
    def _print_mismatch_table(self, title: str, mismatches: List[Dict]):
        """Helper method to print mismatch information."""
        print("\n" + "="*130)
        print(f"MISMATCH INDICES - {title} (majority vote doesn't match new alignment)")
        print("="*130)
        
        if not mismatches:
            print("No mismatches found!")
            return
        
        mismatch_indices = sorted(set(m['csv_index'] for m in mismatches))
        print(f"\nTotal mismatched sentences: {len(mismatch_indices)}")
        print(f"Mismatch indices: {mismatch_indices}")
        
        # Count by original gender
        gender_counts = defaultdict(int)
        for m in mismatches:
            gender_counts[m['original']] += 1
        
        total_mismatch_count = sum(gender_counts.values())
        
        print("\n\nMismatch distribution by original gender:")
        print(f"{'Gender':<15} {'Count':<8} {'Percentage':<10}")
        print("-"*50)
        for gender in sorted(gender_counts.keys()):
            count = gender_counts[gender]
            pct = (count / total_mismatch_count * 100) if total_mismatch_count > 0 else 0
            print(f"{gender:<15} {count:<8} {pct:.1f}%")
        
        print("\n\nDetailed mismatches:")
        print(f"{'CSV Index':<10} {'Translator':<15} {'Majority Gender':<15} {'Original':<12} {'Old':<12} {'New':<12} {'Adjective':<10}")
        print("-"*130)
        
        for m in sorted(mismatches, key=lambda x: x['csv_index']):
            adj_str = "Yes" if m['has_adjective'] else "No"
            print(f"{m['csv_index']:<10} {m['translator']:<15} {m['majority_gender']:<15} {m['original']:<12} {m['old_alignment']:<12} {m['new_alignment']:<12} {adj_str:<10}")
    
    def save_to_csv(self, output_file: str):
        """Save complete analysis to CSV file."""
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Explanation comment
            writer.writerow(['EXPLANATION'])
            writer.writerow(['Match Original: human annotated gender matches the gender in the German sentence'])
            writer.writerow([' (then the MT translated the gender correctly, participants dont see the German version)'])
            writer.writerow(['Match New: human annotated gender matches the new alignment machine gender annotation'])
            writer.writerow(['Expression Match: participants agree that the expression matches the subject in the sentence'])
            writer.writerow(['Makes Sense Yes: participants agree that the sentence makes sense'])
            writer.writerow(['With/out Adj: statistics for sentences with/without adjectives for German original gender and new alignment annotation'])
            writer.writerow([])
            
            # Header information
            writer.writerow(['Language', self.language])
            writer.writerow(['Date', self.date if self.date else 'N/A'])
            writer.writerow(['Analysis Method', 'Majority Vote'])
            writer.writerow(['Number of participants', self.num_participants])
            writer.writerow(['Total sentences', self.num_sentences])
            writer.writerow(['Sentences with adjective', self.sentences_with_adjective])
            writer.writerow(['Sentences without adjective', self.sentences_without_adjective])
            writer.writerow([])
            
            # Inter-annotator agreement
            writer.writerow(['Inter-Annotator Agreement'])
            if self.alpha is not None:
                writer.writerow(['Krippendorff Alpha', f"{self.alpha:.4f}"])
                writer.writerow(['Full agreement (out of 100 sentences)', self.iaa_stats['full_agreement_count']])
            writer.writerow([])
            
            # === ALL DATA ===
            writer.writerow(['=' * 50])
            writer.writerow(['ALL DATA (Majority Vote)'])
            writer.writerow(['=' * 50])
            writer.writerow([])
            
            totals_all = self._calculate_totals(self.summary_by_translator)
            percentages_all = self._calculate_percentages(totals_all, totals_all['total_sentences'])
            
            self._write_summary_section(writer, self.summary_by_translator, totals_all, percentages_all)
            self._write_mismatch_section(writer, self.mismatches)
            
            # === FILTERED DATA ===
            writer.writerow([])
            writer.writerow([])
            writer.writerow(['=' * 50])
            writer.writerow(['FILTERED DATA (Majority makesense=yes)'])
            writer.writerow(['=' * 50])
            writer.writerow([])
            
            totals_filtered = self._calculate_totals(self.summary_by_translator_filtered)
            percentages_filtered = self._calculate_percentages(totals_filtered, totals_filtered['total_sentences'])
            
            writer.writerow(['Total sentences analyzed', totals_filtered['total_sentences']])
            writer.writerow([])
            
            self._write_summary_section(writer, self.summary_by_translator_filtered, 
                                      totals_filtered, percentages_filtered,
                                      comparison_percentages=percentages_all)
            self._write_mismatch_section(writer, self.mismatches_filtered)
        
        print(f"\nSummary saved to {output_file}")
    
    def _write_summary_section(self, writer, summary_dict: Dict, totals: Dict, percentages: Dict, comparison_percentages=None):
        """Helper to write summary statistics section to CSV."""
        # Summary table
        writer.writerow(['SUMMARY TABLE'])
        writer.writerow(['Translator', 'Total Sentences', 'Match Orig', 'Match New', 'Expression Match', 'Makes Sense Yes',
                        'With Adj Orig', 'With Adj New', 'Without Adj Orig', 'Without Adj New'])
        
        for translator, stats in sorted(summary_dict.items()):
            writer.writerow([
                translator, stats.total_sentences, stats.match_original, stats.match_new,
                stats.match_yes, stats.makesense_yes, stats.with_adj_match_original,
                stats.with_adj_match_new, stats.without_adj_match_original, stats.without_adj_match_new
            ])
        
        writer.writerow([
            'TOTAL', totals['total_sentences'], totals['match_original'], totals['match_new'],
            totals['match_yes'], totals['makesense_yes'], totals['with_adj_match_original'],
            totals['with_adj_match_new'], totals['without_adj_match_original'], totals['without_adj_match_new']
        ])
        
        writer.writerow([
            '%', '', f"{percentages['match_original']:.1f}%", f"{percentages['match_new']:.1f}%",
            f"{percentages['match_yes']:.1f}%", f"{percentages['makesense_yes']:.1f}%",
            f"{percentages['with_adj_orig']:.1f}%", f"{percentages['with_adj_new']:.1f}%",
            f"{percentages['without_adj_orig']:.1f}%", f"{percentages['without_adj_new']:.1f}%"
        ])
        
        # If comparison percentages provided, show the difference
        if comparison_percentages:
            diff_orig = percentages['match_original'] - comparison_percentages['match_original']
            diff_new = percentages['match_new'] - comparison_percentages['match_new']
            diff_match = percentages['match_yes'] - comparison_percentages['match_yes']
            diff_makesense = percentages['makesense_yes'] - comparison_percentages['makesense_yes']
            diff_with_adj_orig = percentages['with_adj_orig'] - comparison_percentages['with_adj_orig']
            diff_with_adj_new = percentages['with_adj_new'] - comparison_percentages['with_adj_new']
            diff_without_adj_orig = percentages['without_adj_orig'] - comparison_percentages['without_adj_orig']
            diff_without_adj_new = percentages['without_adj_new'] - comparison_percentages['without_adj_new']
            
            writer.writerow([
                'Δ vs ALL', '', f"{diff_orig:+.1f}%", f"{diff_new:+.1f}%",
                f"{diff_match:+.1f}%", f"{diff_makesense:+.1f}%",
                f"{diff_with_adj_orig:+.1f}%", f"{diff_with_adj_new:+.1f}%",
                f"{diff_without_adj_orig:+.1f}%", f"{diff_without_adj_new:+.1f}%"
            ])
        
        writer.writerow([])
    
    def _write_mismatch_section(self, writer, mismatches: List[Dict]):
        """Helper to write mismatch analysis section to CSV."""
        writer.writerow(['MISMATCH ANALYSIS'])
        writer.writerow([])
        
        mismatch_indices = sorted(set(m['csv_index'] for m in mismatches))
        writer.writerow(['Total mismatched sentences', len(mismatch_indices)])
        writer.writerow(['Mismatch indices', str(mismatch_indices)])
        writer.writerow([])
        
        # Gender distribution
        gender_counts = defaultdict(int)
        for m in mismatches:
            gender_counts[m['original']] += 1
        
        total_mismatch_count = sum(gender_counts.values())
        
        writer.writerow(['Mismatch distribution by original gender'])
        writer.writerow(['Gender', 'Count', 'Percentage'])
        for gender in sorted(gender_counts.keys()):
            count = gender_counts[gender]
            pct = (count / total_mismatch_count * 100) if total_mismatch_count > 0 else 0
            writer.writerow([gender, count, f"{pct:.1f}%"])
        
        writer.writerow([])
        writer.writerow(['Detailed Mismatches'])
        writer.writerow(['CSV Index', 'Translator', 'Majority Gender', 'Original', 'Old', 'New', 'Adjective'])
        
        for m in sorted(mismatches, key=lambda x: x['csv_index']):
            adj_str = "Yes" if m['has_adjective'] else "No"
            writer.writerow([
                m['csv_index'], m['translator'], m['majority_gender'],
                m['original'], m['old_alignment'], m['new_alignment'], adj_str
            ])
        writer.writerow([])


if __name__ == "__main__":
    # Analyze with majority voting
    analyzer = MajorityVoteAnalyzer("human_eval_uk_results_0211.csv")
    
    # Print and save results
    analyzer.print_summary()
    #analyzer.print_mismatches()
    
    # Generate output filename with date
    output_name = f"analysis_majority_{analyzer.language}"
    if analyzer.date:
        output_name += f"_{analyzer.date}"
    output_name += ".csv"
    
    analyzer.save_to_csv(output_name)
