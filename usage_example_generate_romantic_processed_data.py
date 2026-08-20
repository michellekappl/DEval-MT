"""Build processed_data/romantic_names/romantic_name_<model>_processed.csv from
Name_Romantic.csv + translations/romantic_name/<lang>_<model>.txt, mirroring
usage_example_generate_processed_data.py for the main avg_DEval dataset.

Only gpt-4o is missing at the time of writing: the other 5 systems already have
their processed_data/romantic_names/*.csv (see usage_example_romantic_names.py),
and now that the GPT-4o translations for all 7 languages are complete, this
fills the same gap for the romantic-partner/names dataset.
"""

import os

import pandas as pd

from Dataset import DEvalDataset
from morphological_analysis.base_analyzer import BaseMorphologicalAnalyzer
from morphological_analysis.hebrew_morph_analyzer import HebrewMorphAnalyzer
from morphological_analysis.qalsadi_morph_analyzer import QalsadiMorphAnalyzer
from morphological_analysis.spacy_morph_analyzer import SpaCyMorphAnalyzer
from sdk import run_subject_pipeline

LANGUAGES = ["es", "fr", "it", "ar", "ru", "uk", "he"]
SOURCE_CSV = "Name_Romantic.csv"
TRANSLATIONS_DIR = "translations/romantic_name"
OUTPUT_DIR = "processed_data/romantic_names"


def build_romantic_data(model_name: str) -> DEvalDataset:
    out_path = os.path.join(OUTPUT_DIR, f"romantic_name_{model_name}_processed.csv")
    if os.path.exists(out_path):
        print(f"{out_path} already exists, skipping.")
        return DEvalDataset.from_csv(out_path, text_column="text", sep=";", translation_columns={})

    df = pd.read_csv(SOURCE_CSV, sep=";")
    ds = DEvalDataset(df, text_column="text")

    for lang in LANGUAGES:
        path = os.path.join(TRANSLATIONS_DIR, f"{lang}_{model_name}.txt")
        with open(path, "r", encoding="utf-8") as f:
            translations = [line.rstrip("\n") for line in f]
        # translate_romantic_names_gpt.py writes one trailing blank line
        # (the file ends with "\n" after the last real line's content).
        if len(translations) == len(df) + 1 and translations[-1] == "":
            translations = translations[:-1]
        if len(translations) != len(df):
            raise ValueError(
                f"{path}: {len(translations)} lines but {len(df)} source rows"
            )
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
    build_romantic_data("gpt-4o")
