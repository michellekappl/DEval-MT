# Automated translation for Microsoft API 
# has functions for each for single sentence translation and batch translation 
# also includes function for reading a dataset.csv and extracting and translating the 
# sentences from the text column 

import os
import requests
from typing import List, Union
from dotenv import load_dotenv
import uuid

load_dotenv()

# Environment variables
MICROSOFT_API_KEY = os.getenv("MICROSOFT_TRANSLATOR_KEY")
MICROSOFT_ENDPOINT = os.getenv("MICROSOFT_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com")
MICROSOFT_REGION = os.getenv("MICROSOFT_TRANSLATOR_REGION", "")



def translate_text_microsoft(text: str, target: str) -> str:
    """
    Translate text using Microsoft Translator API.
    Source language is automatically detected.

    Args:
        text: Text to translate.
        target: Target language code (e.g., "en", "fr", "ja").

    Returns:
        Translated text as a string.
    """
    url = f"{MICROSOFT_ENDPOINT}/translate"
    
    headers = {
        "Ocp-Apim-Subscription-Key": MICROSOFT_API_KEY,
        "Content-Type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }
    if MICROSOFT_REGION:
        headers["Ocp-Apim-Subscription-Region"] = MICROSOFT_REGION

    params = {
        "api-version": "3.0",
        "to": [target.lower()],  # single target language
        # omit 'from' to let Microsoft detect the source language automatically
    }

    body = [{"text": text}]
    
    response = requests.post(url, headers=headers, params=params, json=body)
    response.raise_for_status()
    data = response.json()

    # Response format: [{"translations": [{"text": "...", "to": "en"}]}]
    return data[0]["translations"][0]["text"]




def batch_translate_and_write_microsoft(texts: List[str], target: Union[str, List[str]], source: str, output_files: dict):
    """
    Batch translate texts using Microsoft Translator API and write directly to files.
    Respects 50,000 character limit per request.
    """
    if isinstance(target, str):
        target_list = [target]
    else:
        target_list = target
    
    url = f"{MICROSOFT_ENDPOINT}/translate"
    headers = {
        "Ocp-Apim-Subscription-Key": MICROSOFT_API_KEY,
        "Content-Type": "application/json",
    }
    if MICROSOFT_REGION:
        headers["Ocp-Apim-Subscription-Region"] = MICROSOFT_REGION
    
    params = {
        "api-version": "3.0",
        "from": source,
        "to": target_list,
    }
    
    batch = []
    batch_char_count = 0
    MAX_CHARS = 50000
    total_texts = len(texts)
    processed_texts = 0
    
    for i, text in enumerate(texts):
        text_len = len(text)
        
        # If adding this text exceeds limit, process current batch
        if batch and (batch_char_count + text_len > MAX_CHARS):
            print(f"[Microsoft] Processing batch of {len(batch)} sentences ({batch_char_count:,} chars)")
            body = [{"text": t} for t in batch]
            response = requests.post(url, headers=headers, params=params, json=body)
            response.raise_for_status()
            data = response.json()
            
            # Write translations immediately
            for item in data:
                translations = item["translations"]
                for trans in translations:
                    lang = trans["to"]
                    output_files[lang].write(trans["text"] + "\n")
            
            processed_texts += len(batch)
            progress = (processed_texts / total_texts) * 100
            print(f"[Microsoft] Progress: {processed_texts}/{total_texts} sentences translated ({progress:.1f}%)")
            
            batch = []
            batch_char_count = 0
        
        batch.append(text)
        batch_char_count += text_len
    
    # Process remaining batch
    if batch:
        print(f"[Microsoft] Processing final batch of {len(batch)} sentences ({batch_char_count:,} chars)")
        body = [{"text": t} for t in batch]
        response = requests.post(url, headers=headers, params=params, json=body)
        response.raise_for_status()
        data = response.json()
        
        for item in data:
            translations = item["translations"]
            for trans in translations:
                lang = trans["to"]
                output_files[lang].write(trans["text"] + "\n")
        
        processed_texts += len(batch)
        print(f"[Microsoft] Progress: {processed_texts}/{total_texts} sentences translated (100.0%)")

