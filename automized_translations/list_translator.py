# accepts language(s) and provider(s) as string or list of strings


from systran_translate import translate_text_systran
from google_translate import translate_text_google
from deepl_translate import translate_text_deepl
from microsoft_translate import translate_text_microsoft
from gpt_translate import translate_text_gpt
import csv
import os
from typing import List, Union


def translate_dataset(
    csv_path: str,
    target: Union[str, List[str]],
    provider: Union[str, List[str]],
    output_dir: str = "../test_data/translations",
    overwrite_translation: bool = False,
    # gpt_model: str = "gpt-4o-mini"
):
    """
    Translates a CSV dataset using specified translation provider(s) and target language(s).
    Writes translations directly to files. (default folder /test_data/translations)
    Tracks translation progress in 25% increments.

    Args:
        csv_path: Path to CSV file with a 'text' column
        target: Target language(s) - string or list of strings (e.g., "es" or ["es", "fr"])
        provider: Translation provider(s) - "systran", "google", "deepl", "microsoft", or list of these
        output_dir: Directory to save translation files (default: "../test_data/translations")
        overwrite_translation: If False (default), skips translations that already exist
        gpt_model: GPT model to use if provider is "gpt" (default: "gpt-4o-mini"), also allowed gpt-4o
    """
    # Normalize inputs to lists
    if isinstance(provider, str):
        provider_list = [provider]
    else:
        provider_list = provider

    if isinstance(target, str):
        target_list = [target]
    else:
        target_list = target

    # Read sentences from CSV
    sentences = []
    print(f"\n{'='*60}")
    print(f"Reading CSV from: {csv_path}")
    with open(csv_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            if "text" in row:
                sentences.append(row["text"])
            else:
                raise ValueError("CSV must have a 'text' column")

    print(f"Found {len(sentences)} sentences to translate")
    print(f"TARGET LANGUAGES: {', '.join(target_list)}")
    print(f"PROVIDERS: {', '.join(provider_list)}")
    print(f"{'='*60}\n")

    # Prepare output directory
    os.makedirs(output_dir, exist_ok=True)

    # Calculate progress interval (25% of sentences)
    progress_interval = max(1, len(sentences) // 4)

    # Process each provider
    for prov in provider_list:
        print(f"\n{'='*40}")
        print(f"Provider: {prov.upper()}")
        print(f"{'='*40}")

        # Process each target language
        for lang in target_list:
            file_name = f"{lang}_{prov}.txt"
            file_path = os.path.join(output_dir, file_name)

            # Check if translation already exists
            if os.path.exists(file_path) and not overwrite_translation:
                print(f"[{prov}] Skipping {lang} - translation already exists")
                continue

            if os.path.exists(file_path) and overwrite_translation:
                print(f"[{prov}] Overwriting existing translation for {lang}")
            else:
                print(f"[{prov}] Creating translation for {lang}")

            # Translate sentences
            with open(file_path, "w", encoding="utf-8") as file:
                for i, sentence in enumerate(sentences):
                    try:
                        # Call the appropriate translator function
                        if prov == "systran":
                            translated_sentence = translate_text_systran(sentence, lang)
                        elif prov == "google":
                            translated_sentence = translate_text_google(sentence, lang)
                            translated_sentence = translated_sentence["translatedText"]
                        elif prov == "deepl":
                            translated_sentence = translate_text_deepl(sentence, lang)
                        elif prov == "microsoft":
                            translated_sentence = translate_text_microsoft(sentence, lang)
                        elif prov == "gpt-4o":
                            translated_sentence = translate_text_gpt(sentence, lang, prov)
                        elif prov == "gpt-4o-mini":
                            translated_sentence = translate_text_gpt(sentence, lang, prov)
                        elif prov == "gpt-5-mini":
                            translated_sentence = translate_text_gpt(sentence, lang, prov)

                        else:
                            raise ValueError(
                                f"Unknown provider: {prov}. Available: systran, google, deepl, microsoft, gpt-4o, gpt-4o-mini"
                            )
                        file.write(translated_sentence + "\n")

                        if (i + 1) % progress_interval == 0:
                            progress_percent = ((i + 1) / len(sentences)) * 100
                            print(
                                f"[{prov}] {progress_percent:.0f}% - Translated {i + 1}/{len(sentences)} sentences for {lang}"
                            )

                    except Exception as e:
                        print(f"[{prov}] Error translating sentence {i + 1} for {lang}: {str(e)}")
                        file.write(f"ERROR: {str(e)}\n")

            print(f"[{prov}] Completed {lang} - saved to {file_path}\n")


# Example usage:
if __name__ == "__main__":
    dataset_path = "../test_data/output.csv"

    # Single language, single provider
    translate_dataset(dataset_path, "es", "systran")

    # Multiple languages, single provider
    translate_dataset(dataset_path, ["es", "fr"], "google")

    # Single language, multiple providers
    translate_dataset(dataset_path, "es", ["systran", "google"])

    # Multiple languages, multiple providers
    translate_dataset(
        dataset_path, ["es", "fr"], ["systran", "google"], overwrite_translation=False
    )
