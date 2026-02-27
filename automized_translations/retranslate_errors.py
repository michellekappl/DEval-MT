import os
import csv
import time
from typing import List

from systran_translate import translate_text_systran
from google_translate import translate_text_google, translate_text_google_llm
from deepl_translate import translate_text_deepl
from microsoft_translate import translate_text_microsoft
from gpt_translate import translate_text_gpt


def find_error_lines(translation_file: str) -> List[int]:
    error_lines = []
    with open(translation_file, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if line.strip().startswith("ERROR:"):
                error_lines.append(i)
    return error_lines


def load_source_sentences(csv_path: str) -> List[str]:
    sentences = []
    with open(csv_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            if "text" in row:
                sentences.append(row["text"])
            else:
                raise ValueError("CSV must have a 'text' column")
    return sentences


def translate_single(sentence: str, lang: str, provider: str) -> str:
    if provider == "systran":
        return translate_text_systran(sentence, lang)
    elif provider == "google":
        result = translate_text_google(sentence, lang)
        return result["translatedText"]
    elif provider == "google_llm":
        result = translate_text_google_llm(sentence, lang)
        return result.translations[0].translated_text
    elif provider == "deepl":
        return translate_text_deepl(sentence, lang)
    elif provider == "microsoft":
        return translate_text_microsoft(sentence, lang)
    elif provider in ["gpt-4o", "gpt-4o-mini", "gpt-5-mini"]:
        return translate_text_gpt(sentence, lang, provider)
    else:
        raise ValueError(f"Unknown provider: {provider}")


def retranslate_errors(
    csv_path: str,
    translation_dir: str,
    max_retries: int = 3,
    retry_delay: float = 2.0,
    only_file: str = None,
):
    """
    Find and retranslate all error lines in translation files.

    Args:
        csv_path: Path to the source CSV with 'text' column
        translation_dir: Directory containing translation files
        max_retries: Maximum number of retries per sentence
        retry_delay: Delay in seconds between retries
        only_file: If specified, only process this file (e.g., "he_microsoft.txt")
    """
    # Load source sentences
    print(f"Loading source sentences from {csv_path}...")
    sentences = load_source_sentences(csv_path)
    print(f"Loaded {len(sentences)} sentences")

    # Find all translation files
    translation_files = [f for f in os.listdir(translation_dir) if f.endswith(".txt")]

    # Filter to only the specified file if provided
    if only_file:
        if only_file in translation_files:
            translation_files = [only_file]
            print(f"Processing only: {only_file}")
        else:
            print(f"File not found: {only_file}")
            return

    total_errors = 0
    total_fixed = 0

    for filename in sorted(translation_files):
        filepath = os.path.join(translation_dir, filename)

        # Parse language and provider from filename (e.g., "he_microsoft.txt")
        parts = filename.replace(".txt", "").split("_", 1)
        if len(parts) != 2:
            print(f"Skipping {filename} - unexpected format")
            continue

        lang, provider = parts

        # Find error lines
        error_lines = find_error_lines(filepath)
        if not error_lines:
            continue

        print(f"\n{'='*60}")
        print(f"File: {filename}")
        print(f"Language: {lang}, Provider: {provider}")
        print(
            f"Found {len(error_lines)} errors at lines: {error_lines[:10]}{'...' if len(error_lines) > 10 else ''}"
        )
        print(f"{'='*60}")

        total_errors += len(error_lines)

        # Read all lines from the translation file
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Retranslate each error line
        fixed_count = 0
        for line_idx in error_lines:
            if line_idx >= len(sentences):
                print(
                    f"  Line {line_idx + 1}: Index out of range (only {len(sentences)} sentences in dataset)"
                )
                continue

            source_sentence = sentences[line_idx]
            print(f"  Line {line_idx + 1}: Retranslating '{source_sentence[:50]}...'")

            # Try to translate with retries
            for attempt in range(max_retries):
                try:
                    translated = translate_single(source_sentence, lang, provider)
                    lines[line_idx] = translated + "\n"
                    fixed_count += 1
                    print(f"    ✓ Success: '{translated[:50]}...'")
                    break
                except Exception as e:
                    print(f"    Attempt {attempt + 1}/{max_retries} failed: {str(e)[:50]}")
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
            else:
                print(f"    ✗ Failed after {max_retries} attempts")

        # Write back the fixed file
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(lines)

        print(f"Fixed {fixed_count}/{len(error_lines)} errors in {filename}")
        total_fixed += fixed_count

    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Total errors found: {total_errors}")
    print(f"Total errors fixed: {total_fixed}")
    print(f"Remaining errors: {total_errors - total_fixed}")


if __name__ == "__main__":
    # Retranslate errors in the romantic_name translations
    # Test with just one file first - change to None to process all files
    retranslate_errors(
        csv_path="../Name_Romantic.csv",
        translation_dir="../translations/romantic_name",
        max_retries=3,
        retry_delay=2.0,
    )
