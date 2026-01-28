import csv
import sys
import os
import random
from typing import List, Optional, Dict, Tuple


def get_translator(filename):
    # Extract translator name from filename
    # e.g., "google_processed.csv" -> "Google"
    base = os.path.basename(filename)
    name = base.replace("_processed.csv", "")
    # Capitalize only the first letter
    return name[0].upper() + name[1:] if name else ""


def create_eval_csv(input_file, lang):
    # Adjust path to be relative to parent directory if not absolute
    if not os.path.isabs(input_file) and not input_file.startswith(".."):
        input_file = os.path.join("..", input_file)

    translator = get_translator(input_file)
    output_file = f"{lang}_{translator}_hev.csv"

    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")

        # Group rows by x_gender
        groups = {"MASCULINE": [], "FEMININE": [], "DIVERSE": []}
        for row in reader:
            gender = row.get("x_gender", "")
            if gender in groups:
                groups[gender].append(row)

        # Sample: 49 MASCULINE, 49 FEMININE, 2 DIVERSE -> similiar distribution to original dataset
        sampled = []
        sampled.extend(random.sample(groups["MASCULINE"], min(49, len(groups["MASCULINE"]))))
        sampled.extend(random.sample(groups["FEMININE"], min(49, len(groups["FEMININE"]))))
        sampled.extend(random.sample(groups["DIVERSE"], min(2, len(groups["DIVERSE"]))))

        # Shuffle the sampled rows
        random.shuffle(sampled)

        rows = []
        for idx, row in enumerate(sampled, start=1):
            sentence = row.get(lang, "")
            x_phrase = row.get("x_phrase_" + lang, "")

            if sentence and x_phrase:
                entity = f"The expression: {x_phrase}"
                sentence_text = f"The sentence: {sentence}"
                rows.append([idx, translator, entity, sentence_text])

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Index", "Translator", "Entity", "Sentence"])
        writer.writerows(rows)


def _find_processed_files(base_dir: str) -> List[str]:
    """Find all *_processed.csv files in the given base directory."""
    files = []
    for name in os.listdir(base_dir):
        if name.endswith("_processed.csv") and os.path.isfile(os.path.join(base_dir, name)):
            files.append(os.path.join(base_dir, name))
    return files


def create_multi_eval_csv(
    lang: str,
    input_files: Optional[List[str]] = None,
    seed: int = 42,
    output_file: Optional[str] = None,
    metadata_file: Optional[str] = None,
) -> Tuple[str, Dict[str, int]]:
    """
    Create a single evaluation CSV for a given language from multiple
    *_processed.csv files in the repository root. Ensures no duplicates
    across models, maintains target distribution (49/49/2).

    Parameters:
        lang: Language column to use (e.g., 'fr', 'es').
        input_files: Optional explicit list of file paths. If None, scans ../ for *_processed.csv.
        seed: Random seed for reproducibility.
        output_file: Optional explicit output filename. Defaults to f"{lang}_Multi_hev.csv".
        metadata_file: Optional CSV file to save info about selected rows. Defaults to f"{lang}_Multi_hev_metadata.csv".

    Returns:
        (output_file_path, sampled_counts_by_gender)
    """
    random.seed(seed)

    # Resolve input files (default: scan parent directory)
    parent_dir = ".."
    if input_files is None:
        input_files = _find_processed_files(parent_dir)
    else:
        # Normalize non-absolute paths to be relative to parent
        normalized = []
        for f in input_files:
            if not os.path.isabs(f) and not f.startswith(".."):
                normalized.append(os.path.join(parent_dir, f))
            else:
                normalized.append(f)
        input_files = normalized

    if not input_files:
        raise FileNotFoundError("No *_processed.csv files found.")

    # Dedup across models based on (sentence, x_phrase_lang)
    # Group by (translator, gender) for balanced sampling
    dedup_key_seen = set()
    grouped_by_translator_gender: Dict[Tuple[str, str], List[Dict[str, str]]] = {}

    for file_path in input_files:
        translator = get_translator(file_path)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter=";")
                for row_num, row in enumerate(reader, start=2):  # Start at 2 to account for header
                    gender = row.get("x_gender", "")
                    sentence = row.get(lang, "")
                    x_phrase = row.get(f"x_phrase_{lang}", "")

                    if not sentence or not x_phrase:
                        continue
                    if gender not in ["MASCULINE", "FEMININE", "DIVERSE"]:
                        continue

                    key = (sentence.strip(), x_phrase.strip())
                    if key in dedup_key_seen:
                        continue
                    dedup_key_seen.add(key)

                    trans_gender_key = (translator, gender)
                    if trans_gender_key not in grouped_by_translator_gender:
                        grouped_by_translator_gender[trans_gender_key] = []

                    grouped_by_translator_gender[trans_gender_key].append(
                        {
                            "Translator": translator,
                            "Sentence": sentence,
                            "Entity": f"The expression: {x_phrase}",
                            "SourceFile": os.path.basename(file_path),
                            "SourceLine": row_num,
                            "Gender": gender,
                        }
                    )
        except FileNotFoundError:
            # Skip missing files silently
            continue

    # Determine unique translators
    all_translators = set(t for t, g in grouped_by_translator_gender.keys())
    num_translators = len(all_translators)

    if num_translators == 0:
        raise ValueError("No translators found in input files.")

    # Target distribution (strict 100 rows: 49/49/2)
    target = {"MASCULINE": 49, "FEMININE": 49, "DIVERSE": 2}

    # Calculate per-translator targets, ensuring balanced sampling
    per_translator_target = {}
    for gender in ["MASCULINE", "FEMININE", "DIVERSE"]:
        base_count = target[gender] // num_translators
        remainder = target[gender] % num_translators
        for idx, translator in enumerate(sorted(all_translators)):
            # Distribute remainder across first few translators
            count = base_count + (1 if idx < remainder else 0)
            per_translator_target[(translator, gender)] = count

    # Sample from each (translator, gender) group
    sampled_rows: List[List[str]] = []
    metadata_records = []  # Track source info for each selected row

    for (translator, gender), target_count in per_translator_target.items():
        if target_count <= 0:
            continue

        pool = grouped_by_translator_gender.get((translator, gender), [])
        available_count = len(pool)

        if available_count < target_count:
            raise ValueError(
                f"Not enough unique {gender} rows from {translator}: "
                f"need {target_count}, have {available_count}."
            )

        sampled = random.sample(pool, target_count)
        for item in sampled:
            sampled_rows.append(
                [item["Translator"], item["Entity"], f"The sentence: {item['Sentence']}"]
            )
            metadata_records.append(
                {
                    "Translator": item["Translator"],
                    "SourceFile": item["SourceFile"],
                    "SourceLine": item["SourceLine"],
                    "Gender": item["Gender"],
                    "Sentence": item["Sentence"],
                    "Entity": item["Entity"],
                }
            )

    sampled_counts = target

    # Shuffle across models and genders, then assign unique global indices
    # Keep metadata aligned with sampled_rows for shuffling
    combined = list(zip(sampled_rows, metadata_records))
    random.shuffle(combined)
    sampled_rows, metadata_records = zip(*combined) if combined else ([], [])

    rows_with_index = []
    metadata_with_index = []
    for idx, (row, meta) in enumerate(zip(sampled_rows, metadata_records), start=1):
        # row = [Translator, Entity, Sentence]
        rows_with_index.append([idx] + list(row))
        metadata_with_index.append((idx, meta))

    # Create output directories if needed
    output_dir = "outputs/multi_model"
    metadata_dir = "outputs/metadata"
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(metadata_dir, exist_ok=True)

    # Output file name
    final_output = output_file or os.path.join(output_dir, f"{lang}_Multi_hev.csv")
    with open(final_output, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Index", "Translator", "Entity", "Sentence"])
        writer.writerows(rows_with_index)

    # Write metadata CSV file
    metadata_output = metadata_file or os.path.join(metadata_dir, f"{lang}_Multi_hev_metadata.csv")
    with open(metadata_output, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(
            [
                "Index",
                "Translator",
                "Gold_Gender",
                "Source_File_Line",
                "Sentence",
            ]
        )
        for idx, meta in metadata_with_index:
            writer.writerow(
                [
                    idx,
                    meta["Translator"],
                    meta["Gender"],
                    meta["SourceLine"],
                    meta["Sentence"],
                ]
            )

    return final_output, sampled_counts
