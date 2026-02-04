import pandas as pd
import json
from collections import defaultdict
import csv
import numpy as np
import krippendorff


def calculate_krippendorff_alpha(df):
    """
    Calculate Krippendorff's alpha for inter-annotator agreement on gender annotations.
    Returns the alpha value and additional statistics.
    """
    # Build reliability data matrix: rows = items, columns = annotators
    # For each sentence, we have multiple annotators giving gender ratings
    
    # Extract all gender lists
    all_items = []
    for idx, row in df.iterrows():
        try:
            gender_list = json.loads(row['gender'].replace("'", '"'))
            all_items.append(gender_list)
        except:
            continue
    
    if not all_items:
        return None, "No valid data found"
    
    # Convert to numpy array
    num_items = len(all_items)
    num_annotators = len(all_items[0]) if all_items else 0
    
    # Create reliability matrix (items x annotators)
    # Map gender values to numeric codes
    gender_map = {'m': 1, 'f': 2, 'n': 3, 'u': 4}
    reverse_map = {1: 'm', 2: 'f', 3: 'n', 4: 'u'}
    
    data_matrix = np.zeros((num_items, num_annotators))
    for i, gender_list in enumerate(all_items):
        for j, gender in enumerate(gender_list):
            data_matrix[i, j] = gender_map.get(gender, 4)  # Default to 'u' (unknown)
    
    # Calculate Krippendorff's alpha using nominal metric
    # Transpose because krippendorff library expects (annotators x items)
    alpha = krippendorff.alpha(reliability_data=data_matrix.T, level_of_measurement='nominal')
    
    # Additional statistics
    total_annotations = num_items * num_annotators
    agreement_count = 0
    
    # Count full agreement (all annotators agree)
    for i in range(num_items):
        row = data_matrix[i, :]
        if len(set(row)) == 1:  # All values are the same
            agreement_count += 1
    
    full_agreement_pct = (agreement_count / num_items * 100) if num_items > 0 else 0
    
    stats = {
        'alpha': alpha,
        'num_items': num_items,
        'num_annotators': num_annotators,
        'total_annotations': total_annotations,
        'full_agreement_count': agreement_count,
        'full_agreement_pct': full_agreement_pct
    }
    
    return alpha, stats


def analyze_gender_matches(csv_file):
    """
    Analyze gender matches by translator/language.
    Returns a summary table with match counts and a list of mismatch indices.
    """
    
    df = pd.read_csv(csv_file)
    
    # Group by translator
    summary_by_lang = defaultdict(lambda: {
        'total_entries': 0,
        'match_original': 0,
        'match_old': 0,
        'match_new': 0,
        'with_adj_match_original': 0,
        'with_adj_match_new': 0,
        'without_adj_match_original': 0,
        'without_adj_match_new': 0,
        'match_yes': 0,
        'makesense_yes': 0
    })
    
    # Track mismatches (where gender doesn't match old OR new alignment)
    mismatches = []
    
    for idx, row in df.iterrows():
        # Parse the gender list
        try:
            gender_list = json.loads(row['gender'].replace("'", '"'))
        except:
            gender_list = []

        try:
            match_list = json.loads(row['match'].replace("'", '"'))
        except:
            match_list = []

        try:
            makesense_list = json.loads(row['makesense'].replace("'", '"'))
        except:
            makesense_list = []
        
        translator = row['translator']
        original = row['original_gender']
        new_align = row['gender_new_alignment']
        old_align = row['gender_old_alignment']
        csv_index = row['index']  # Get the index from the CSV's 'index' column
        has_adjective = row.get('has_adjective', False)
        
        # Convert to single letter representation for comparison
        gender_mapping = {
            'MASCULINE': 'm',
            'FEMININE': 'f',
            'UNKNOWN': 'u',
            'DIVERSE': 'n',
            'NEUTRAL': 'n',
            'm': 'm',
            'f': 'f',
            'n': 'n'
        }
        
        orig_letter = gender_mapping.get(original, 'unknown')
        new_letter = gender_mapping.get(new_align, 'unknown')
        old_letter = gender_mapping.get(old_align, 'unknown')
        
        # Check matches for each gender list entry
        for i, gender_val in enumerate(gender_list):
            summary_by_lang[translator]['total_entries'] += 1

            match_val = match_list[i] if i < len(match_list) else None
            makesense_val = makesense_list[i] if i < len(makesense_list) else None
            
            matches_original = gender_val == orig_letter
            matches_new = gender_val == new_letter
            matches_old = gender_val == old_letter
            
            if matches_original:
                summary_by_lang[translator]['match_original'] += 1
                if has_adjective:
                    summary_by_lang[translator]['with_adj_match_original'] += 1
                else:
                    summary_by_lang[translator]['without_adj_match_original'] += 1
            if matches_new:
                summary_by_lang[translator]['match_new'] += 1
                if has_adjective:
                    summary_by_lang[translator]['with_adj_match_new'] += 1
                else:
                    summary_by_lang[translator]['without_adj_match_new'] += 1
            if matches_old:
                summary_by_lang[translator]['match_old'] += 1

            if match_val == 'yes':
                summary_by_lang[translator]['match_yes'] += 1
            if makesense_val == 'yes':
                summary_by_lang[translator]['makesense_yes'] += 1
            
            
            # Track mismatches: doesn't match new alignment (then the morphological analysis might be problematic)
            if not matches_new:
                mismatches.append({
                    'csv_index': csv_index,
                    'translator': translator,
                    'human_response': gender_val,
                    'original': original,
                    'new_alignment': new_align,
                    'old_alignment': old_align,
                    'has_adjective': has_adjective,
                    'makesense': makesense_val
                })
    
    return summary_by_lang, df, mismatches


def print_summary_table(summary_by_lang, num_participants, df, language):
    """Print results as a clean table."""
    num_sentences = 100
    total_possible_answers = num_sentences * num_participants
    
    # Calculate inter-annotator agreement
    alpha, iaa_stats = calculate_krippendorff_alpha(df)
    
    # Count sentences with adjectives
    sentences_with_adjective = len(df[df['has_adjective'] == True])
    sentences_without_adjective = num_sentences - sentences_with_adjective
    
    # Calculate totals across all translators
    total_entries = sum(stats['total_entries'] for stats in summary_by_lang.values())
    total_match_original = sum(stats['match_original'] for stats in summary_by_lang.values())
    total_match_old = sum(stats['match_old'] for stats in summary_by_lang.values())
    total_match_new = sum(stats['match_new'] for stats in summary_by_lang.values())
    total_with_adj_match_original = sum(stats['with_adj_match_original'] for stats in summary_by_lang.values())
    total_with_adj_match_new = sum(stats['with_adj_match_new'] for stats in summary_by_lang.values())
    total_without_adj_match_original = sum(stats['without_adj_match_original'] for stats in summary_by_lang.values())
    total_without_adj_match_new = sum(stats['without_adj_match_new'] for stats in summary_by_lang.values())
    total_match_yes = sum(stats['match_yes'] for stats in summary_by_lang.values())
    total_makesense_yes = sum(stats['makesense_yes'] for stats in summary_by_lang.values())
    
    print("\n" + "="*160)
    print(f"GENDER MATCH SUMMARY BY TRANSLATOR ({language})")
    print("="*160)
    print(f"Dataset info: {num_sentences} sentences × {num_participants} participants = {total_possible_answers} possible answers")
    print(f"Sentences with adjective: {sentences_with_adjective} | Sentences without adjective: {sentences_without_adjective}")
    print("-"*160)
    print(f"Inter-Annotator Agreement (Krippendorff's Alpha): {alpha:.4f}")
    print(f"Full agreement (all annotators agree): {iaa_stats['full_agreement_count']}/{iaa_stats['num_items']} ({iaa_stats['full_agreement_pct']:.1f}%)")
    print("="*160)
    print(f"{'Translator':<15} {'Total':<8} {'Match Orig':<12} {'Match New':<10} {'Expression match':<12} {'Makes Sense Yes':<17} {'With Adj':<10} {'Without Adj':<20}")
    print(f"{'':15} {'':8} {'':12} {'':12} {'':10} {'':21} {'Orig|New':<14} {'Orig|New':<20}")
    print("-"*160)
    
    for translator, stats in sorted(summary_by_lang.items()):
        with_adj = f"{stats['with_adj_match_original']}|{stats['with_adj_match_new']}"
        without_adj = f"{stats['without_adj_match_original']}|{stats['without_adj_match_new']}"
        print(f"{translator:<18} {stats['total_entries']:<10} {stats['match_original']:<12} {stats['match_new']:<12} {stats['match_yes']:<15} {stats['makesense_yes']:<12} {with_adj:<14} {without_adj:<20}")
    
    print("-"*160)
    with_adj_total = f"{total_with_adj_match_original}|{total_with_adj_match_new}"
    without_adj_total = f"{total_without_adj_match_original}|{total_without_adj_match_new}"
    print(f"{'TOTAL':<18} {total_entries:<10} {total_match_original:<12} {total_match_new:<12} {total_match_yes:<15} {total_makesense_yes:<12} {with_adj_total:<14} {without_adj_total:<20}")
    
    # Calculate percentages
    total_possible_answers = num_sentences * num_participants
    with_adj_poss = sentences_with_adjective * num_participants
    without_adj_poss = sentences_without_adjective * num_participants
    
    pct_match_original = (total_match_original / total_possible_answers * 100) if total_possible_answers > 0 else 0
    pct_match_new = (total_match_new / total_possible_answers * 100) if total_possible_answers > 0 else 0
    pct_match_yes = (total_match_yes / total_possible_answers * 100) if total_possible_answers > 0 else 0
    pct_makesense_yes = (total_makesense_yes / total_possible_answers * 100) if total_possible_answers > 0 else 0
    pct_with_adj_orig = (total_with_adj_match_original / with_adj_poss * 100) if with_adj_poss > 0 else 0
    pct_with_adj_new = (total_with_adj_match_new / with_adj_poss * 100) if with_adj_poss > 0 else 0
    pct_without_adj_orig = (total_without_adj_match_original / without_adj_poss * 100) if without_adj_poss > 0 else 0
    pct_without_adj_new = (total_without_adj_match_new / without_adj_poss * 100) if without_adj_poss > 0 else 0
    
    with_adj_pct = f"{pct_with_adj_orig:.1f}%|{pct_with_adj_new:.1f}%"
    without_adj_pct = f"{pct_without_adj_orig:.1f}%|{pct_without_adj_new:.1f}%"
    pct_orig_str = f"{pct_match_original:.1f}%"
    pct_new_str = f"{pct_match_new:.1f}%"
    pct_match_yes_str = f"{pct_match_yes:.1f}%"
    pct_makesense_yes_str = f"{pct_makesense_yes:.1f}%"
    print(f"{'%':<18} {'':10} {pct_orig_str:<12} {pct_new_str:<12} {pct_match_yes_str:<15} {pct_makesense_yes_str:<12} {with_adj_pct:<10} {without_adj_pct:<20}")
    print("="*160)


def save_summary_to_csv(summary_by_lang, num_participants, df, language, mismatches, output_file):
    """Save summary table to CSV file."""
    num_sentences = 100
    total_possible_answers = num_sentences * num_participants
    
    # Calculate inter-annotator agreement
    alpha, iaa_stats = calculate_krippendorff_alpha(df)
    
    # Count sentences with adjectives
    sentences_with_adjective = len(df[df['has_adjective'] == True])
    sentences_without_adjective = num_sentences - sentences_with_adjective
    
    # Calculate totals across all translators
    total_entries = sum(stats['total_entries'] for stats in summary_by_lang.values())
    total_match_original = sum(stats['match_original'] for stats in summary_by_lang.values())
    total_match_new = sum(stats['match_new'] for stats in summary_by_lang.values())
    total_with_adj_match_original = sum(stats['with_adj_match_original'] for stats in summary_by_lang.values())
    total_with_adj_match_new = sum(stats['with_adj_match_new'] for stats in summary_by_lang.values())
    total_without_adj_match_original = sum(stats['without_adj_match_original'] for stats in summary_by_lang.values())
    total_without_adj_match_new = sum(stats['without_adj_match_new'] for stats in summary_by_lang.values())
    total_match_yes = sum(stats['match_yes'] for stats in summary_by_lang.values())
    total_makesense_yes = sum(stats['makesense_yes'] for stats in summary_by_lang.values())
    
    # Calculate percentages
    with_adj_poss = sentences_with_adjective * num_participants
    without_adj_poss = sentences_without_adjective * num_participants
    
    pct_match_original = (total_match_original / total_possible_answers * 100) if total_possible_answers > 0 else 0
    pct_match_new = (total_match_new / total_possible_answers * 100) if total_possible_answers > 0 else 0
    pct_match_yes = (total_match_yes / total_possible_answers * 100) if total_possible_answers > 0 else 0
    pct_makesense_yes = (total_makesense_yes / total_possible_answers * 100) if total_possible_answers > 0 else 0
    pct_with_adj_orig = (total_with_adj_match_original / with_adj_poss * 100) if with_adj_poss > 0 else 0
    pct_with_adj_new = (total_with_adj_match_new / with_adj_poss * 100) if with_adj_poss > 0 else 0
    pct_without_adj_orig = (total_without_adj_match_original / without_adj_poss * 100) if without_adj_poss > 0 else 0
    pct_without_adj_new = (total_without_adj_match_new / without_adj_poss * 100) if without_adj_poss > 0 else 0
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write header
        writer.writerow(['Language', language])
        writer.writerow(['Sentences', num_sentences])
        writer.writerow(['Participants', num_participants])
        writer.writerow(['Total possible answers', total_possible_answers])
        writer.writerow(['Sentences with adjective', sentences_with_adjective])
        writer.writerow(['Sentences without adjective', sentences_without_adjective])
        writer.writerow([])  # Empty row
        
        # Write inter-annotator agreement
        writer.writerow(['Inter-Annotator Agreement'])
        writer.writerow(['Krippendorff Alpha', f"{alpha:.4f}"])
        writer.writerow(['Full agreement count', iaa_stats['full_agreement_count']])
        writer.writerow(['Full agreement percentage', f"{iaa_stats['full_agreement_pct']:.1f}%"])
        writer.writerow([])  # Empty row
        
        # Write column headers
        writer.writerow(['Translator', 'Total', 'Match Orig', 'Match New', 'Expression Match', 'Makes Sense Yes', 
                        'With Adj Orig', 'With Adj New', 'Without Adj Orig', 'Without Adj New'])
        
        # Write translator data
        for translator, stats in sorted(summary_by_lang.items()):
            writer.writerow([
                translator,
                stats['total_entries'],
                stats['match_original'],
                stats['match_new'],
                stats['match_yes'],
                stats['makesense_yes'],
                stats['with_adj_match_original'],
                stats['with_adj_match_new'],
                stats['without_adj_match_original'],
                stats['without_adj_match_new']
            ])
        
        # Write totals
        writer.writerow([
            'TOTAL',
            total_entries,
            total_match_original,
            total_match_new,
            total_match_yes,
            total_makesense_yes,
            total_with_adj_match_original,
            total_with_adj_match_new,
            total_without_adj_match_original,
            total_without_adj_match_new
        ])
        
        # Write percentages
        writer.writerow([
            '%',
            '',
            f"{pct_match_original:.1f}%",
            f"{pct_match_new:.1f}%",
            f"{pct_match_yes:.1f}%",
            f"{pct_makesense_yes:.1f}%",
            f"{pct_with_adj_orig:.1f}%",
            f"{pct_with_adj_new:.1f}%",
            f"{pct_without_adj_orig:.1f}%",
            f"{pct_without_adj_new:.1f}%"
        ])
        
        # Add mismatches section
        writer.writerow([])  # Empty row
        writer.writerow([])  # Empty row
        writer.writerow(['MISMATCH ANALYSIS'])
        writer.writerow([])  # Empty row
        
        # Get unique sentence indices with mismatches
        mismatch_indices = sorted(set([m['csv_index'] for m in mismatches]))
        writer.writerow(['Total mismatched sentences (at least one participant disagreed with the new alignment)', len(mismatch_indices)])
        writer.writerow(['Mismatch indices', str(mismatch_indices)])
        writer.writerow([])  # Empty row
        
        # Count mismatches by original gender
        gender_counts = defaultdict(int)
        for mismatch in mismatches:
            gender_counts[mismatch['original']] += 1
        
        total_mismatch_count = sum(gender_counts.values())
        
        writer.writerow(['Mismatch distribution by original gender'])
        writer.writerow(['Gender', 'Count', 'Percentage'])
        for gender in sorted(gender_counts.keys()):
            count = gender_counts[gender]
            pct = (count / total_mismatch_count * 100) if total_mismatch_count > 0 else 0
            writer.writerow([gender, count, f"{pct:.1f}%"])
        
        writer.writerow([])  # Empty row
        
        # Write detailed mismatches
        writer.writerow(['Detailed Mismatches'])
        writer.writerow(['CSV Index', 'Translator', 'Gender Value', 'Original', 'Old', 'New', 'Adjective'])
        
        seen = set()
        unique_mismatches = []
        for mismatch in sorted(mismatches, key=lambda x: x['csv_index']):
            key = (
                mismatch['csv_index'],
                mismatch['translator'],
                mismatch['human_response']
            )
            if key in seen:
                continue
            seen.add(key)
            unique_mismatches.append(mismatch)

        for mismatch in unique_mismatches:
            adj_str = "Yes" if mismatch['has_adjective'] else "No"
            writer.writerow([
                mismatch['csv_index'],
                mismatch['translator'],
                mismatch['human_response'],
                mismatch['original'],
                mismatch['old_alignment'],
                mismatch['new_alignment'],
                adj_str
            ])
    
    print(f"\nSummary saved to {output_file}")


def print_mismatches(mismatches):
    """Print list of indices with mismatches (doesn't match old or new alignment)."""
    print("\n" + "="*130)
    print("MISMATCH INDICES (doesn't match new alignment)")
    print("="*130)
    
    if not mismatches:
        print("No mismatches found!")
        return
    
    mismatch_indices = sorted(set([m['csv_index'] for m in mismatches]))
    print(f"\nTotal mismatched sentences (where at least one participant disagreed with the (new) alignment): {len(mismatch_indices)}")
    print(f"Mismatch indices: {mismatch_indices}")
    
    # Count mismatches by original gender
    gender_counts = defaultdict(int)
    for mismatch in mismatches:
        gender_counts[mismatch['original']] += 1
    
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
    seen = set()
    unique_mismatches = []
    for mismatch in sorted(mismatches, key=lambda x: x['csv_index']):
        key = (
            mismatch['csv_index'],
            mismatch['translator'],
            mismatch['human_response']
        )
        if key in seen:
            continue
        seen.add(key)
        unique_mismatches.append(mismatch)

    for mismatch in unique_mismatches:
        adj_str = "Yes" if mismatch['has_adjective'] else "No"
        print(f"{mismatch['csv_index']:<10} {mismatch['translator']:<15} {mismatch['human_response']:<12} {mismatch['original']:<12} {mismatch['old_alignment']:<12} {mismatch['new_alignment']:<12} {adj_str:<10}")


if __name__ == "__main__":
    # Analyze the Spanish results file
    csv_file = "human_eval_ru_results.csv"
    
    summary_by_lang, df, mismatches = analyze_gender_matches(csv_file)

    language = csv_file.replace("human_eval_", "").replace("_results.csv", "")
    
    # Calculate number of participants from the first gender vector
    num_participants = 0
    for idx, row in df.iterrows():
        try:
            gender_list = json.loads(row['gender'].replace("'", '"'))
            num_participants = len(gender_list)
            break
        except:
            continue
    
    print_summary_table(summary_by_lang, num_participants, df, language)
    print_mismatches(mismatches)
    
    # Save results to CSV
    output_csv = f"analyis_results_h_eval_{language}.csv"
   # save_summary_to_csv(summary_by_lang, num_participants, df, language, mismatches, output_csv)
