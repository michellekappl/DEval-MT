"""Example usage of the modular analysis system for DEval-MT."""

import os
import pandas as pd
import numpy as np
from Dataset import DEvalDataset
from analysis import (
    ErrorAnalysis,
    ConfusionMatrix,
    LogisticRegressionAnalysis,
)
from morphological_analysis.base_analyzer import BaseMorphologicalAnalyzer
from morphological_analysis.qalsadi_morph_analyzer import QalsadiMorphAnalyzer
from morphological_analysis.spacy_morph_analyzer import SpaCyMorphAnalyzer
from morphological_analysis.hebrew_morph_analyzer import HebrewMorphAnalyzer
from sdk import run_subject_pipeline

# Import plotting functions from your modular package
from plots import (
    plot_error_analysis,
    plot_confusion_matrix,
    plot_logistic_regression,
    save_dataframes,
)


def example_data(model_name: str) -> DEvalDataset:
    if os.path.exists(f"{model_name}_processed.csv"):
        ds = DEvalDataset.from_csv(
            f"{model_name}_processed.csv",
            text_column="text",
            sep=";",
            translation_columns={
                "es": "es",
                "fr": "fr",
                "it": "it",
                # "no": "no",
                # "sv": "sv",
                "ar": "ar",
                "ru": "ru",
                "uk": "uk",
                "he": "he",
            },
            prediction_columns={"es": "x_gender_es", "fr": "x_gender_fr"},
        )
        return ds
    else:
        print(f"{model_name}_processed.csv not found, creating from scratch...")
        df = pd.read_csv("DEval_dataset.csv", sep=";")
        ds = DEvalDataset(df, text_column="text")

        list_of_es_translations = pd.read_csv(
            f"translations/es_{model_name}.txt", header=None, sep=";"
        )[0].tolist()
        list_of_fr_translations = pd.read_csv(
            f"translations/fr_{model_name}.txt", header=None, sep=";"
        )[0].tolist()
        list_of_it_translations = pd.read_csv(
            f"translations/it_{model_name}.txt", header=None, sep=";"
        )[0].tolist()
        # list_of_no_translations = pd.read_csv(
        #     f"translations/no_{model_name}.txt", header=None, sep=";"
        # )[0].tolist()
        # list_of_sv_translations = pd.read_csv(
        #     f"translations/sv_{model_name}.txt", header=None, sep=";"
        # )[0].tolist()
        with open(f"translations/ar_{model_name}.txt", "r", encoding="utf-8") as f:
            list_of_ar_translations = [line.strip() for line in f.readlines()]
        #
        with open(f"translations/ru_{model_name}.txt", "r", encoding="utf-8") as f:
            list_of_ru_translations = [line.strip() for line in f.readlines()]
        with open(f"translations/uk_{model_name}.txt", "r", encoding="utf-8") as f:
            list_of_uk_translations = [line.strip() for line in f.readlines()]
        with open(f"translations/he_{model_name}.txt", "r", encoding="utf-8") as f:
            list_of_he_translations = [line.strip() for line in f.readlines()]

        ds.add_translations("es", list_of_es_translations, "es")
        ds.add_translations("fr", list_of_fr_translations, "fr")
        ds.add_translations("it", list_of_it_translations, "it")
        # ds.add_translations("no", list_of_no_translations, "no")
        # ds.add_translations("sv", list_of_sv_translations, "sv")
        ds.add_translations("ar", list_of_ar_translations, "ar")
        ds.add_translations("ru", list_of_ru_translations, "ru")
        ds.add_translations("uk", list_of_uk_translations, "uk")
        ds.add_translations("he", list_of_he_translations, "he")

        morph_es = SpaCyMorphAnalyzer("es_dep_news_trf")
        morph_es.load()
        morph_fr = SpaCyMorphAnalyzer("fr_dep_news_trf")
        morph_fr.load()
        morph_it = SpaCyMorphAnalyzer("it_core_news_lg")
        morph_it.load()
        # morph_no = SpaCyMorphAnalyzer("nb_core_news_lg")
        # morph_no.load()
        # morph_sv = SpaCyMorphAnalyzer("sv_core_news_lg")
        # morph_sv.load()
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
            # "no": morph_no,
            # "sv": morph_sv,
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
            article_offset=-1,
            use_multiprocessing=False,
        )

        return ds


if __name__ == "__main__":
    for model_name in ["microsoft"]:
        ds1 = example_data(model_name)
        ds1.df.to_csv(f"{model_name}_processed.csv", sep=";", index=False)
