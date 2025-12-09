# Automated translation for DeepL API 
# has functions for each for single sentence translation and batch translation 
# also includes function for reading a dataset.csv and extracting and translating the 
# sentences from the text column 

import os
import requests
from typing import List, Union
from dotenv import load_dotenv

load_dotenv()

# Environment variables
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
DEEPL_BASE_URL = os.getenv("DEEPL_API_URL", "https://api-free.deepl.com/v2")  # or api.deepl.com for pro

def translate_text_deepl(text: str, target: Union[str, List[str]], source: str = "DE") -> Union[str, dict]:
    """
    Translates text using DeepL API.
    Max 128 KiB per request (~131,072 characters).
    
    Note: DeepL uses uppercase language codes (e.g., "EN", "DE")
    For English, you can specify "EN-US" or "EN-GB"
    
    Returns:
        - Single string if target is a string
        - Dict of {language: translation} if target is a list
    """
    if isinstance(target, str):
        target_list = [target.upper()]
        return_single = True
    else:
        target_list = [t.upper() for t in target]
        return_single = False
    
    url = f"{DEEPL_BASE_URL}/translate"
    headers = {
        "Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}",
        "Content-Type": "application/json",
    }
    
    results = {}
    for tgt in target_list:
        body = {
            "text": [text],
            "source_lang": source.upper(),
            "target_lang": tgt,
        }
        
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        data = response.json()
        
        # Response format: {"translations": [{"detected_source_language": "DE", "text": "..."}]}
        translated_text = data["translations"][0]["text"]
        results[tgt.lower()] = translated_text
    
    if return_single:
        return list(results.values())[0]
    else:
        return results


def batch_translate_and_write_deepl(texts: List[str], target: Union[str, List[str]], source: str, output_files: dict):
    """
    Batch translate texts using DeepL API and write directly to files.
    Respects 128 KiB limit per request (~131,072 characters).
    """
    if isinstance(target, str):
        target_list = [target.upper()]
    else:
        target_list = [t.upper() for t in target]
    
    url = f"{DEEPL_BASE_URL}/translate"
    headers = {
        "Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}",
        "Content-Type": "application/json",
    }
    
    total_texts = len(texts)
    
    for tgt in target_list:
        print(f"[DeepL] Translating to {tgt}")
        batch = []
        batch_char_count = 0
        MAX_CHARS = 131072  # 128 KiB
        processed_texts = 0
        
        for i, text in enumerate(texts):
            text_len = len(text)
            
            # If adding this text exceeds limit, process current batch
            if batch and (batch_char_count + text_len > MAX_CHARS):
                print(f"[DeepL] Processing batch of {len(batch)} sentences ({batch_char_count:,} chars)")
                body = {
                    "text": batch,
                    "source_lang": source.upper(),
                    "target_lang": tgt,
                }
                response = requests.post(url, headers=headers, json=body)
                response.raise_for_status()
                data = response.json()
                
                # Write translations immediately
                for translation in data["translations"]:
                    output_files[tgt.lower()].write(translation["text"] + "\n")
                
                processed_texts += len(batch)
                progress = (processed_texts / total_texts) * 100
                print(f"[DeepL] Progress: {processed_texts}/{total_texts} sentences translated ({progress:.1f}%)")
                
                batch = []
                batch_char_count = 0
            
            batch.append(text)
            batch_char_count += text_len
        
        # Process remaining batch
        if batch:
            print(f"[DeepL] Processing final batch of {len(batch)} sentences ({batch_char_count:,} chars)")
            body = {
                "text": batch,
                "source_lang": source.upper(),
                "target_lang": tgt,
            }
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()
            data = response.json()
            
            for translation in data["translations"]:
                output_files[tgt.lower()].write(translation["text"] + "\n")
            
            processed_texts += len(batch)
            print(f"[DeepL] Progress: {processed_texts}/{total_texts} sentences translated (100.0%)")
