"""Build study/processed_data/<model>_processed.csv from
study/data/deval_dataset.csv + study/data/translations/<lang>_<model>.txt, for
every model in MODELS. Skips a model if its output file already exists.

Run from the repository root: `python study/usage_example_generate_processed_data.py`.
"""

import os

import pandas as pd

from deval_mt import (
    DEvalDataset,
    BaseMorphologicalAnalyzer,
    HebrewMorphAnalyzer,
    QalsadiMorphAnalyzer,
    SpaCyMorphAnalyzer,
    run_subject_pipeline,
)

LANGUAGES = ["es", "fr", "it", "ar", "ru", "uk", "he"]
MODELS = ["deepl", "google", "google_llm", "gpt-4o", "microsoft", "systran"]
SOURCE_CSV = "study/data/deval_dataset.csv"
TRANSLATIONS_DIR = "study/data/translations"
OUTPUT_DIR = "study/processed_data"


def build_processed_data(model_name: str) -> DEvalDataset:
    out_path = os.path.join(OUTPUT_DIR, f"{model_name}_processed.csv")
    if os.path.exists(out_path):
        print(f"{out_path} already exists, skipping.")
        return DEvalDataset.from_csv(out_path, text_column="text", sep=";", translation_columns={})

    df = pd.read_csv(SOURCE_CSV, sep=";")
    ds = DEvalDataset(df, text_column="text")

    for lang in LANGUAGES:
        path = os.path.join(TRANSLATIONS_DIR, f"{lang}_{model_name}.txt")
        with open(path, "r", encoding="utf-8") as f:
            translations = [line.rstrip("\n") for line in f]
        if len(translations) == len(df) + 1 and translations[-1] == "":
            translations = translations[:-1]
        if len(translations) != len(df):
            raise ValueError(f"{path}: {len(translations)} lines but {len(df)} source rows")
        ds.add_translations(lang, translations, lang)

    morph_es = SpaCyMorphAnalyzer("es_dep_news_trf")
    morph_es.load()
    morph_fr = SpaCyMorphAnalyzer("fr_dep_news_trf")
    morph_fr.load()
    morph_it = SpaCyMorphAnalyzer("it_core_news_lg")
    morph_it.load()
    morph_ar = QalsadiMorphAnalyzer()
    morph_ru = SpaCyMorphAnalyzer("ru_core_news_lg")
    morph_ru.load()
    morph_uk = SpaCyMorphAnalyzer("uk_core_news_trf")
    morph_uk.load()
    morph_he = HebrewMorphAnalyzer()

    analyzers: dict[str, BaseMorphologicalAnalyzer] = {
        "es": morph_es,
        "fr": morph_fr,
        "it": morph_it,
        "ar": morph_ar,
        "ru": morph_ru,
        "uk": morph_uk,
        "he": morph_he,
    }

    run_subject_pipeline(
        ds,
        analyzers=analyzers,
        source_column="text",
        subject_index_column="x_idx",
        output_prefix="x",
        use_multiprocessing=False,
    )

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    ds.df.to_csv(out_path, sep=";", index=False)
    print(f"Saved {out_path}")
    return ds


if __name__ == "__main__":
    for model in MODELS:
        build_processed_data(model)
