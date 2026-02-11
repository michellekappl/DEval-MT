import pandas as pd
import json
from collections import defaultdict
import csv
import numpy as np
import krippendorff
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class SummaryStatistics:
    """Container for summary statistics."""
    total_entries: int = 0
    match_original: int = 0
    match_old: int = 0
    match_new: int = 0
    with_adj_match_original: int = 0
    with_adj_match_new: int = 0
    without_adj_match_original: int = 0
    without_adj_match_new: int = 0
    match_yes: int = 0
    makesense_yes: int = 0


class GenderEvaluationAnalyzer:
    """Analyzes gender evaluation results from human annotators."""
    
    GENDER_MAP = {'MASCULINE': 'm', 'FEMININE': 'f', 'UNKNOWN': 'u', 'DIVERSE': 'n', 
                  'NEUTRAL': 'n', 'm': 'm', 'f': 'f', 'n': 'n'}
    
    def __init__(self, csv_file: str, num_sentences: int = 100):
        self.csv_file = csv_file
        self.num_sentences = num_sentences
        self.df = pd.read_csv(csv_file)
        
        # Extract language and date from filename
        # Expected format: human_eval_{lang}_results_{date}.csv
        import re
        match = re.search(r'human_eval_([a-z]+)_results_([0-9]+)\.csv', csv_file)
        if match:
            self.language = match.group(1)
            self.date = match.group(2)
        else:
            # Fallback for old format: human_eval_{lang}_results.csv
            self.language = csv_file.replace("human_eval_", "").replace("_results.csv", "")
            self.date = None
        
        # Compute everything once
        self.num_participants = self._get_num_participants()
        self.summary_by_lang = self._compute_summary()
        self.mismatches = self._compute_mismatches()
        self.alpha, self.iaa_stats = self._compute_krippendorff_alpha()
        
        # Computed properties
        self.sentences_with_adjective = len(self.df[self.df['has_adjective'] == True])
        self.sentences_without_adjective = self.num_sentences - self.sentences_with_adjective
        self.total_possible_answers = self.num_sentences * self.num_participants
    
    def _get_num_participants(self) -> int:
        """Extract number of participants from first valid gender list."""
        for _, row in self.df.iterrows():
            try:
                gender_list = json.loads(row['gender'].replace("'", '"'))
                return len(gender_list)
            except:
                continue
        return 0
    
    def _parse_json_list(self, value: str) -> List:
        """Parse JSON string safely."""
        try:
            return json.loads(value.replace("'", '"'))
        except:
            return []
    
    def _compute_krippendorff_alpha(self) -> Tuple[float, Dict]:
        """Calculate Krippendorff's alpha for inter-annotator agreement."""
        all_items = []
        for _, row in self.df.iterrows():
            gender_list = self._parse_json_list(row['gender'])
            if not gender_list:
                continue
            
            all_items.append(gender_list)
        
        if not all_items:
            return None, {}
        
        num_items = len(all_items)
        num_annotators = len(all_items[0])
        
        # Map to numeric codes
        gender_to_num = {'m': 1, 'f': 2, 'n': 3, 'u': 4}
        data_matrix = np.full((num_items, num_annotators), np.nan)  # Use NaN for missing
        for i, gender_list in enumerate(all_items):
            for j, gender in enumerate(gender_list):
                if gender is not None:  # Only set if not filtered out
                    data_matrix[i, j] = gender_to_num.get(gender, 4)
        
        alpha = krippendorff.alpha(reliability_data=data_matrix.T, level_of_measurement='nominal')
        
        # Count full agreement (ignoring NaN values)
        agreement_count = 0
        for i in range(num_items):
            row = data_matrix[i, :]
            valid_values = row[~np.isnan(row)]
            if len(valid_values) > 1 and len(set(valid_values)) == 1:
                agreement_count += 1
        
        return alpha, {
            'alpha': alpha,
            'num_items': num_items,
            'num_annotators': num_annotators,
            'total_annotations': num_items * num_annotators,
            'full_agreement_count': agreement_count,
            'full_agreement_pct': (agreement_count / num_items * 100) if num_items > 0 else 0
        }
    
    def _compute_summary(self) -> Dict[str, SummaryStatistics]:
        """Compute summary statistics by translator."""
        summary = defaultdict(SummaryStatistics)
        
        for _, row in self.df.iterrows():
            gender_list = self._parse_json_list(row['gender'])
            match_list = self._parse_json_list(row['match'])
            makesense_list = self._parse_json_list(row['makesense'])
            
            translator = row['translator']
            has_adjective = row.get('has_adjective', False)
            
            # Convert genders to single letter
            orig_letter = self.GENDER_MAP.get(row['original_gender'], 'unknown')
            new_letter = self.GENDER_MAP.get(row['gender_new_alignment'], 'unknown')
            old_letter = self.GENDER_MAP.get(row['gender_old_alignment'], 'unknown')
            
            for i, gender_val in enumerate(gender_list):
                stats = summary[translator]
                stats.total_entries += 1
                
                if gender_val == orig_letter:
                    stats.match_original += 1
                    if has_adjective:
                        stats.with_adj_match_original += 1
                    else:
                        stats.without_adj_match_original += 1
                
                if gender_val == new_letter:
                    stats.match_new += 1
                    if has_adjective:
                        stats.with_adj_match_new += 1
                    else:
                        stats.without_adj_match_new += 1
                
                if gender_val == old_letter:
                    stats.match_old += 1
                
                if i < len(match_list) and match_list[i] == 'yes':
                    stats.match_yes += 1
                
                if i < len(makesense_list) and makesense_list[i] == 'yes':
                    stats.makesense_yes += 1
        
        return dict(summary)
    
    def _compute_mismatches(self) -> List[Dict]:
        """Identify cases where human annotation doesn't match new alignment."""
        mismatches = []
        
        for _, row in self.df.iterrows():
            gender_list = self._parse_json_list(row['gender'])
            makesense_list = self._parse_json_list(row['makesense'])
            new_letter = self.GENDER_MAP.get(row['gender_new_alignment'], 'unknown')
            
            for i, gender_val in enumerate(gender_list):
                if gender_val != new_letter:
                    mismatches.append({
                        'csv_index': row['index'],
                        'translator': row['translator'],
                        'human_response': gender_val,
                        'original': row['original_gender'],
                        'new_alignment': row['gender_new_alignment'],
                        'old_alignment': row['gender_old_alignment'],
                        'has_adjective': row.get('has_adjective', False)
                    })
        
        return mismatches
    
    def _calculate_totals(self, summary_dict=None) -> Dict:
        """Calculate total statistics across all translators."""
        if summary_dict is None:
            summary_dict = self.summary_by_lang
        
        return {
            'total_entries': sum(s.total_entries for s in summary_dict.values()),
            'match_original': sum(s.match_original for s in summary_dict.values()),
            'match_old': sum(s.match_old for s in summary_dict.values()),
            'match_new': sum(s.match_new for s in summary_dict.values()),
            'with_adj_match_original': sum(s.with_adj_match_original for s in summary_dict.values()),
            'with_adj_match_new': sum(s.with_adj_match_new for s in summary_dict.values()),
            'without_adj_match_original': sum(s.without_adj_match_original for s in summary_dict.values()),
            'without_adj_match_new': sum(s.without_adj_match_new for s in summary_dict.values()),
            'match_yes': sum(s.match_yes for s in summary_dict.values()),
            'makesense_yes': sum(s.makesense_yes for s in summary_dict.values()),
        }
    
    def _calculate_percentages(self, totals: Dict, total_possible=None) -> Dict:
        """Calculate percentage values."""
        if total_possible is None:
            total_possible = self.total_possible_answers
            with_adj_poss = self.sentences_with_adjective * self.num_participants
            without_adj_poss = self.sentences_without_adjective * self.num_participants
        else:
            # When using filtered data, calculate adjective denominators proportionally
            # Use the actual filtered counts for adjectives
            with_adj_poss = totals['with_adj_match_original'] + totals['with_adj_match_new']
            without_adj_poss = totals['without_adj_match_original'] + totals['without_adj_match_new']
            
            # Alternative: use total_possible as base for all
            # This makes percentages consistent across the board
            if with_adj_poss == 0:
                with_adj_poss = total_possible  # Avoid division by zero
            if without_adj_poss == 0:
                without_adj_poss = total_possible
        
        return {
            'match_original': (totals['match_original'] / total_possible * 100) if total_possible > 0 else 0,
            'match_new': (totals['match_new'] / total_possible * 100) if total_possible > 0 else 0,
            'match_yes': (totals['match_yes'] / total_possible * 100) if total_possible > 0 else 0,
            'makesense_yes': (totals['makesense_yes'] / total_possible * 100) if total_possible > 0 else 0,
            'with_adj_orig': (totals['with_adj_match_original'] / with_adj_poss * 100) if with_adj_poss > 0 else 0,
            'with_adj_new': (totals['with_adj_match_new'] / with_adj_poss * 100) if with_adj_poss > 0 else 0,
            'without_adj_orig': (totals['without_adj_match_original'] / without_adj_poss * 100) if without_adj_poss > 0 else 0,
            'without_adj_new': (totals['without_adj_match_new'] / without_adj_poss * 100) if without_adj_poss > 0 else 0,
        }
    
    def print_summary(self):
        """Print comprehensive summary table."""
        self._print_summary_table("OVERALL SUMMARY", self.summary_by_lang, self.alpha, self.iaa_stats)
    
    def _print_summary_table(self, title: str, summary_dict: Dict, alpha: float, iaa_stats: Dict, total_entries_for_pct=None, comparison_percentages=None):
        """Helper method to print a summary table."""
        totals = self._calculate_totals(summary_dict)
        percentages = self._calculate_percentages(totals, total_entries_for_pct)
        
        print("\n" + "="*160)
        print(f"GENDER MATCH SUMMARY BY TRANSLATOR ({self.language}) - {title}")
        print("="*160)
        if total_entries_for_pct:
            print(f"Dataset info: Total entries analyzed: {total_entries_for_pct}")
        else:
            print(f"Dataset info: {self.num_sentences} sentences × {self.num_participants} participants = {self.total_possible_answers} possible answers")
        print(f"Sentences with adjective: {self.sentences_with_adjective} | Sentences without adjective: {self.sentences_without_adjective}")
        print("-"*160)
        if alpha is not None:
            print(f"Inter-Annotator Agreement (Krippendorff's Alpha): {alpha:.4f}")
            print(f"Full agreement (all annotators agree): {iaa_stats['full_agreement_count']}/{iaa_stats['num_items']}")
        print("="*160)
        print(f"{'Translator':<15} {'Total':<8} {'Match Orig':<12} {'Match New':<10} {'Expression match':<12} {'Makes Sense Yes':<17} {'With Adj':<10} {'Without Adj':<20}")
        print(f"{'':15} {'':8} {'':12} {'':12} {'':10} {'':21} {'Orig|New':<14} {'Orig|New':<20}")
        print("-"*160)
        
        for translator, stats in sorted(summary_dict.items()):
            with_adj = f"{stats.with_adj_match_original}|{stats.with_adj_match_new}"
            without_adj = f"{stats.without_adj_match_original}|{stats.without_adj_match_new}"
            print(f"{translator:<18} {stats.total_entries:<10} {stats.match_original:<12} {stats.match_new:<12} {stats.match_yes:<15} {stats.makesense_yes:<12} {with_adj:<14} {without_adj:<20}")
        
        print("-"*160)
        with_adj_total = f"{totals['with_adj_match_original']}|{totals['with_adj_match_new']}"
        without_adj_total = f"{totals['without_adj_match_original']}|{totals['without_adj_match_new']}"
        print(f"{'TOTAL':<18} {totals['total_entries']:<10} {totals['match_original']:<12} {totals['match_new']:<12} {totals['match_yes']:<15} {totals['makesense_yes']:<12} {with_adj_total:<14} {without_adj_total:<20}")
        
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
        self._print_mismatch_table("OVERALL MISMATCHES", self.mismatches)
    
    def _print_mismatch_table(self, title: str, mismatches: List[Dict]):
        """Helper method to print mismatch information."""
        print("\n" + "="*130)
        print(f"MISMATCH INDICES - {title} (doesn't match new alignment)")
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
        print(f"{'CSV Index':<10} {'Translator':<15} {'Gender Value':<12} {'Original':<12} {'Old':<12} {'New':<12} {'Adjective':<10}")
        print("-"*130)
        
        # Deduplicate
        seen = set()
        for m in sorted(mismatches, key=lambda x: x['csv_index']):
            key = (m['csv_index'], m['translator'], m['human_response'])
            if key in seen:
                continue
            seen.add(key)
            adj_str = "Yes" if m['has_adjective'] else "No"
            print(f"{m['csv_index']:<10} {m['translator']:<15} {m['human_response']:<12} {m['original']:<12} {m['old_alignment']:<12} {m['new_alignment']:<12} {adj_str:<10}")
    
    def save_to_csv(self, output_file: str):
        """Save complete analysis to CSV file."""
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Explanation section
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
            writer.writerow(['Analysis Method', 'Per Participant'])
            writer.writerow(['Number of participants', self.num_participants])
            writer.writerow(['Total sentences', self.num_sentences])
            writer.writerow(['Total possible answers', self.total_possible_answers])
            writer.writerow(['Sentences with adjective', self.sentences_with_adjective])
            writer.writerow(['Sentences without adjective', self.sentences_without_adjective])
            writer.writerow([])
            
            # === ANALYSIS RESULTS ===
            writer.writerow(['=' * 50])
            writer.writerow(['OVERALL SUMMARY (Per Participant)'])
            writer.writerow(['=' * 50])
            writer.writerow([])
            
            self._write_summary_section(writer, self.summary_by_lang, self.alpha, self.iaa_stats)
            self._write_mismatch_section(writer, self.mismatches)
        
        print(f"\nSummary saved to {output_file}")
    
    def _write_summary_section(self, writer, summary_dict: Dict, alpha: float, iaa_stats: Dict, total_entries_for_pct=None, comparison_percentages=None):
        """Helper to write summary statistics section to CSV."""
        totals = self._calculate_totals(summary_dict)
        percentages = self._calculate_percentages(totals, total_entries_for_pct)
        
        # Inter-annotator agreement
        writer.writerow(['Inter-Annotator Agreement'])
        if alpha is not None:
            writer.writerow(['Krippendorff Alpha', f"{alpha:.4f}"])
            writer.writerow(['Full agreement (out of 100 sentences)', iaa_stats['full_agreement_count']])
        writer.writerow([])
        
        # Summary table
        writer.writerow(['Translator', 'Total', 'Match Orig', 'Match New', 'Expression Match', 'Makes Sense Yes',
                        'With Adj Orig', 'With Adj New', 'Without Adj Orig', 'Without Adj New'])
        
        for translator, stats in sorted(summary_dict.items()):
            writer.writerow([
                translator, stats.total_entries, stats.match_original, stats.match_new,
                stats.match_yes, stats.makesense_yes, stats.with_adj_match_original,
                stats.with_adj_match_new, stats.without_adj_match_original, stats.without_adj_match_new
            ])
        
        writer.writerow([
            'TOTAL', totals['total_entries'], totals['match_original'], totals['match_new'],
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
        writer.writerow(['CSV Index', 'Translator', 'Gender Value', 'Original', 'Old', 'New', 'Adjective'])
        
        seen = set()
        for m in sorted(mismatches, key=lambda x: x['csv_index']):
            key = (m['csv_index'], m['translator'], m['human_response'])
            if key in seen:
                continue
            seen.add(key)
            adj_str = "Yes" if m['has_adjective'] else "No"
            writer.writerow([
                m['csv_index'], m['translator'], m['human_response'],
                m['original'], m['old_alignment'], m['new_alignment'], adj_str
            ])
        writer.writerow([])


if __name__ == "__main__":
    # Analyze Italian results
    analyzer = GenderEvaluationAnalyzer("human_eval_he_results_0204.csv")
    
    # Print and save results
    analyzer.print_summary()
    analyzer.print_mismatches()
    
    # Generate output filename with date
    output_name = f"analysis_results_p_part_{analyzer.language}"
    if analyzer.date:
        output_name += f"_{analyzer.date}"
    output_name += ".csv"
    
    analyzer.save_to_csv(output_name)
