import csv
import sys
import os
import random

def get_translator(filename):
    # Extract translator name from filename
    # e.g., "google_processed.csv" -> "Google"
    base = os.path.basename(filename)
    name = base.replace('_processed.csv', '')
    # Capitalize only the first letter
    return name[0].upper() + name[1:] if name else ''

def create_eval_csv(input_file, lang):
    # Adjust path to be relative to parent directory if not absolute
    if not os.path.isabs(input_file) and not input_file.startswith('..'):
        input_file = os.path.join('..', input_file)
    
    translator = get_translator(input_file)
    output_file = f"{lang}_{translator}_hev.csv"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        
        # Group rows by x_gender
        groups = {'MASCULINE': [], 'FEMININE': [], 'DIVERSE': []}
        for row in reader:
            gender = row.get('x_gender', '')
            if gender in groups:
                groups[gender].append(row)
        
        # Sample: 40 MASCULINE, 40 FEMININE, 20 DIVERSE
        sampled = []
        sampled.extend(random.sample(groups['MASCULINE'], min(40, len(groups['MASCULINE']))))
        sampled.extend(random.sample(groups['FEMININE'], min(40, len(groups['FEMININE']))))
        sampled.extend(random.sample(groups['DIVERSE'], min(20, len(groups['DIVERSE']))))
        
        # Shuffle the sampled rows
        random.shuffle(sampled)
        
        rows = []
        for idx, row in enumerate(sampled, start=1):
            sentence = row.get(lang, '')
            x_phrase = row.get('x_phrase_' + lang, '')
            
            if sentence and x_phrase:
                entity = f"The expression: {x_phrase}"
                sentence_text = f"The sentence: {sentence}"
                rows.append([idx, translator, entity, sentence_text])
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Index', 'Translator', 'Entity', 'Sentence'])
        writer.writerows(rows)
