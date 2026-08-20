"""Translate Name_Romantic.csv into GPT-4o for all 7 core languages.

The other 5 systems (Google, Google LLM, DeepL, Microsoft, SYSTRAN) already have
translations/romantic_name/<lang>_<model>.txt for this dataset; GPT-4o is the only
one missing. This fills that gap using the same translate_text_gpt() function and
output convention as the rest of the pipeline (one line per sentence, same order
as Name_Romantic.csv, written to translations/romantic_name/<lang>_gpt-4o.txt).

Resumable: if a partial output file exists, already-translated lines are kept and
only the remaining lines are translated, so an interrupted run can be restarted
without re-paying for or re-waiting on completed lines.
"""

import csv
import os
import sys
import time

from gpt_translate import translate_text_gpt

LANGUAGES = ["es", "fr", "it", "ar", "ru", "uk", "he"]
SOURCE_CSV = "../Name_Romantic.csv"
OUTPUT_DIR = "../translations/romantic_name"
MODEL_NAME = "gpt-4o"
MAX_RETRIES = 3
RETRY_DELAY = 2.0


def load_source_sentences(csv_path: str) -> list[str]:
    sentences = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            sentences.append(row["text"])
    return sentences


def load_existing_translations(output_path: str) -> list[str]:
    if not os.path.exists(output_path):
        return []
    with open(output_path, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


def translate_language(sentences: list[str], lang: str) -> None:
    output_path = os.path.join(OUTPUT_DIR, f"{lang}_{MODEL_NAME}.txt")
    existing = load_existing_translations(output_path)

    if len(existing) >= len(sentences) and "ERROR:" not in "".join(existing):
        print(f"[{lang}] already complete ({len(existing)} lines), skipping.")
        return

    # Keep already-translated, non-error lines; retranslate the rest.
    results = existing + [""] * (len(sentences) - len(existing))

    for i, sentence in enumerate(sentences):
        if results[i] and not results[i].startswith("ERROR:"):
            continue

        sentence = sentence.strip()
        if not sentence:
            results[i] = ""
            continue

        translated = None
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                translated = translate_text_gpt(sentence, lang, MODEL_NAME)
                break
            except Exception as exc:  # noqa: BLE001 - log and retry
                print(f"[{lang}] line {i}: attempt {attempt} failed: {exc}")
                time.sleep(RETRY_DELAY)

        results[i] = translated if translated is not None else f"ERROR: {sentence}"

        if i % 50 == 0:
            print(f"[{lang}] {i}/{len(sentences)} done")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("\n".join(results) + "\n")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(results) + "\n")
    print(f"[{lang}] complete: {output_path}")


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    sentences = load_source_sentences(SOURCE_CSV)
    print(f"Loaded {len(sentences)} sentences from {SOURCE_CSV}")

    langs = sys.argv[1:] if len(sys.argv) > 1 else LANGUAGES
    for lang in langs:
        print(f"\n=== Translating to {lang} ===")
        translate_language(sentences, lang)

    print("\nAll languages done.")
