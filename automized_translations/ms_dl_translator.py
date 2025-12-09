from typing import List, Union
import os
import csv

from microsoft_translate import batch_translate_and_write_microsoft
from deepl_translate import batch_translate_and_write_deepl

def translate_dataset(csv_path: str, target: Union[str, List[str]], provider: Union[str, List[str]], 
                      source: str = "de", output_dir: str = "../test_data/translations", repeat: bool = False):
    """
    Translates a CSV dataset using the specified translation provider(s).
    Writes translations to files as batches are processed.
    
    Args:
        csv_path: Path to CSV file with a 'text' column
        target: Target language(s) - string or list of strings
        provider: Translation provider(s) - "microsoft", "deepl", or list of both
        source: Source language (default: "de")
        output_dir: Directory to save translation files
        repeat: If False (default), skips translations that already exist
    """
    # Normalize providers to list
    if isinstance(provider, str):
        provider_list = [provider]
    else:
        provider_list = provider
    
    # Normalize targets to list
    if isinstance(target, str):
        target_list = [target]
    else:
        target_list = target
    
    # Read sentences from CSV
    sentences = []
    print(f"\n{'='*60}")
    print(f"Reading CSV from: {csv_path}")
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            if 'text' in row:
                sentences.append(row['text'])
            else:
                raise ValueError("CSV must have a 'text' column")
    
    print(f"Found {len(sentences)} sentences to translate")
    print(f"Target languages: {', '.join(target_list)}")
    print(f"Providers: {', '.join(provider_list)}")
    print(f"{'='*60}\n")
    
    # Prepare output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each provider
    for prov in provider_list:
        if prov not in ["microsoft", "deepl"]:
            raise ValueError(f"Unknown provider: {prov}. Use 'microsoft' or 'deepl'")
        
        print(f"\n{'='*60}")
        print(f"PROVIDER: {prov.upper()}")
        print(f"{'='*60}")
        
        # Check which translations already exist
        files_to_process = {}
        for lang in target_list:
            file_name = f"{lang}_{prov}.txt"
            file_path = os.path.join(output_dir, file_name)
            
            if os.path.exists(file_path) and not repeat:
                print(f"[{prov.upper()}] Skipping {lang} - translation already exists at {file_path}")
            else:
                if os.path.exists(file_path) and repeat:
                    print(f"[{prov.upper()}] Overwriting existing translation: {file_path}")
                else:
                    print(f"[{prov.upper()}] Creating new translation: {file_path}")
                files_to_process[lang] = file_path
        
        # Skip this provider if no files need processing
        if not files_to_process:
            print(f"[{prov.upper()}] All translations exist. Skipping provider.")
            continue
        
        # Open file handles for languages that need translation
        output_files = {}
        for lang, file_path in files_to_process.items():
            output_files[lang] = open(file_path, 'w', encoding='utf-8')
        
        try:
            # Translate and write directly
            if prov == "microsoft":
                print(f"\n[Microsoft] Starting translation (source: {source})")
                batch_translate_and_write_microsoft(sentences, list(files_to_process.keys()), source, output_files)
            elif prov == "deepl":
                print(f"\n[DeepL] Starting translation (source: {source})")
                batch_translate_and_write_deepl(sentences, list(files_to_process.keys()), source, output_files)
        finally:
            # Close all file handles
            for f in output_files.values():
                f.close()
        
        print(f"\n[{prov.upper()}] Translation complete!")
    
    print(f"\n{'='*60}")
    print("ALL TRANSLATIONS COMPLETE!")
    print(f"{'='*60}\n")


# Example usage
if __name__ == "__main__":
    dataset_path = "../test_data/test_data_mini.csv"
    
    # Single provider, single target
    # translate_dataset(dataset_path, "es", "microsoft")
    
    # Single provider, multiple targets
    # translate_dataset(dataset_path, ["en", "es", "fr"], "deepl")
    
    # Multiple providers, multiple targets
    translate_dataset(dataset_path, ["en", "es"], ["microsoft", "deepl"])
    
    # With repeat=True to overwrite existing translations
    # translate_dataset(dataset_path, ["en"], "deepl", repeat=True)