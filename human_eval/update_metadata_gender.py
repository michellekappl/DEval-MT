"""
Script to update x_gender_morph in metadata files with values from new_morpho files.
Matches rows by source_file_line and translator.
"""

import pandas as pd
import os
from pathlib import Path


def update_metadata_gender(metadata_file_path):
    """
    Update x_gender_morph column in metadata file with values from new_morpho files.
    
    Args:
        metadata_file_path: Path to the metadata CSV file (e.g., ar_Multi_hev_metadata.csv)
    """
    # Extract language from filename (e.g., "ar" from "ar_Multi_hev_metadata.csv")
    filename = os.path.basename(metadata_file_path)
    language = filename.split('_')[0]
    
    print(f"Processing metadata file: {filename}")
    print(f"Extracted language: {language}")
    
    # Read metadata file
    print(f"\nReading metadata file...")
    metadata_df = pd.read_csv(metadata_file_path, sep=';')
    print(f"Loaded {len(metadata_df)} rows from metadata file")
    
    # Get the new_morpho folder path
    # metadata file is at: human_eval/outputs/metadata/xxx.csv
    # new_morpho is at: human_eval/new_morpho/
    # So we need to go up 3 levels from metadata file (metadata -> outputs -> human_eval)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(metadata_file_path)))
    new_morpho_dir = os.path.join(base_dir, 'new_morpho')
    
    if not os.path.exists(new_morpho_dir):
        raise FileNotFoundError(f"new_morpho directory not found at: {new_morpho_dir}")
    
    print(f"new_morpho directory: {new_morpho_dir}")
    
    # Column name for gender in new_morpho files
    gender_column = f'x_gender_{language}'
    
    # Map translator names to file names
    translator_file_map = {
        'Deepl': 'deepl_processed.csv',
        'Google': 'google_processed.csv',
        'Systran': 'systran_processed.csv',
        'Microsoft': 'microsoft_processed.csv',
        'GPT-4o': 'gpt-4o_processed.csv',
        'Gpt-4o': 'gpt-4o_processed.csv',  # Handle case variation
        #'Google_llm': 'google_llm_processed.csv'
    }
    
    # Load all translator files into memory for faster lookup
    translator_data = {}
    for translator, filename in translator_file_map.items():
        file_path = os.path.join(new_morpho_dir, filename)
        if os.path.exists(file_path):
            print(f"Loading {filename}...")
            df = pd.read_csv(file_path, sep=';')
            # Store as-is, we'll access by row index
            translator_data[translator] = df
            print(f"  Loaded {len(df)} rows")
        else:
            print(f"  Warning: {filename} not found")
    
    # Update each row in metadata
    print(f"\nUpdating x_gender_morph column...")
    updates_made = 0
    rows_not_found = 0
    
    for idx, row in metadata_df.iterrows():
        translator = row['Translator']
        source_line = row['Source_File_Line']
        
        if translator not in translator_data:
            print(f"  Warning: No data loaded for translator '{translator}' (row {idx})")
            continue
        
        # Convert source_line to DataFrame index
        # source_line is the CSV line number (line 1 = header, line 2 = first data row)
        # So DataFrame index = source_line - 2
        df_index = source_line - 2
        
        # Look up the gender in the translator's data
        if df_index < 0 or df_index >= len(translator_data[translator]):
            rows_not_found += 1
            if rows_not_found <= 5:  # Show first 5 missing
                print(f"  Warning: Line {source_line} (index {df_index}) out of range in {translator} data (row {idx})")
            continue
        
        try:
            morph_row = translator_data[translator].iloc[df_index]
            
            # Check if gender_column exists
            if gender_column in morph_row:
                new_gender = morph_row[gender_column]
                old_gender = row['x_gender_morph']
                
                # Update the value
                metadata_df.at[idx, 'x_gender_morph'] = new_gender
                
                if new_gender != old_gender:
                    updates_made += 1
                    if updates_made <= 5:  # Show first 5 changes
                        print(f"  Row {idx}: {translator}, Line {source_line}: {old_gender} -> {new_gender}")
            else:
                print(f"  Warning: Column '{gender_column}' not found in {translator} data (row {idx})")
                
        except Exception as e:
            rows_not_found += 1
            if rows_not_found <= 5:  # Show first 5 errors
                print(f"  Warning: Error accessing line {source_line} in {translator} data (row {idx}): {e}")
    
    print(f"\nSummary:")
    print(f"  Total rows processed: {len(metadata_df)}")
    print(f"  Values updated: {updates_made}")
    print(f"  Rows where source_line not found: {rows_not_found}")
    
    # Save updated metadata
    output_path = metadata_file_path.replace('.csv', '_updated.csv')
    metadata_df.to_csv(output_path, sep=';', index=False)
    print(f"\nUpdated metadata saved to: {output_path}")
    
    return metadata_df


def update_all_metadata_files(metadata_dir):
    """
    Update all metadata files in the given directory.
    
    Args:
        metadata_dir: Path to the directory containing metadata files
    """
    metadata_files = list(Path(metadata_dir).glob('*_Multi_hev_metadata.csv'))
    
    print(f"Found {len(metadata_files)} metadata files to process\n")
    print("="*80)
    
    for file_path in metadata_files:
        try:
            update_metadata_gender(str(file_path))
            print("="*80)
        except Exception as e:
            print(f"Error processing {file_path.name}: {e}")
            print("="*80)


if __name__ == "__main__":
    # Get the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to metadata directory
    metadata_dir = os.path.join(script_dir, 'outputs', 'metadata')
    
    # Option 1: Update a single file
    metadata_file = os.path.join(metadata_dir, 'uk_Multi_hev_metadata.csv')
    update_metadata_gender(metadata_file)
    
    # Option 2: Update all metadata files
    #update_all_metadata_files(metadata_dir)
