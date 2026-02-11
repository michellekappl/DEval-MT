"""
Example usage of DEval-MT (dataset loading → translations → subject pipeline → analysis → plots).

What this script demonstrates
-----------------------------
1) Automatically discovers *all* translation files in ./translations/
   Expected filename pattern: <lang>_<provider>.txt
   e.g.  es_deepl.txt, fr_gpt-4o.txt, ar_systran.txt

2) Builds one processed dataset per provider (DeepL / Google / GPT / Systran / Microsoft / …),
   runs the x-subject pipeline, and writes:
      processed_data/<provider>_processed.csv

3) Runs the analysis suite (NEW analysis/error_analysis.py + confusion matrix + logistic regression)
   and optionally creates plots via plots.py into:
      outputs/<provider>/

Notes
-----
- This file is meant as an *executable* usage example and a template.
- If you only want to *analyze already processed data*, set --rebuild-datasets 0.
- For spaCy-based analyzers you need the corresponding models installed.
"""

from __future__ import annotations

import argparse
import os
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd

from Dataset import DEvalDataset
from sdk import run_subject_pipeline

# NEW analysis implementation (uses analysis/error_analysis.py, not error_analysis_old.py)
from analysis import ErrorAnalysis, ConfusionMatrix, LogisticRegressionAnalysis

# Plot helpers (optional but recommended)
from plots import (
    plot_error_analysis,
    plot_confusion_metrics,
    plot_logistic_regression,
    save_dataframes,
)

from morphological_analysis.base_analyzer import BaseMorphologicalAnalyzer
from morphological_analysis.spacy_morph_analyzer import SpaCyMorphAnalyzer
from morphological_analysis.hebrew_morph_analyzer import HebrewMorphAnalyzer
from morphological_analysis.qalsadi_morph_analyzer import QalsadiMorphAnalyzer

def add_translations_safely(ds, lang: str, translations: list[str], column_name: str, source_col: str = "text"):
    n_rows = len(ds.df)
    n_trans = len(translations)
    n_unique = ds.df[source_col].nunique()

    if n_trans == n_rows:
        ds.add_translations(lang, translations, column_name)
        return True

    if n_trans == n_unique:
        unique_texts = ds.df[source_col].drop_duplicates().tolist()
        mapping = dict(zip(unique_texts, translations))
        ds.df[column_name] = ds.df[source_col].map(mapping)
        missing = ds.df[column_name].isna().sum()
        if missing:
            print(
                f"[WARN] [{lang}] Mapping by unique text produced {missing} NaNs "
                f"(unique_texts={n_unique}, translations={n_trans}). Skipping."
            )
            ds.df.drop(columns=[column_name], inplace=True, errors="ignore")
            return False
        return True

    print(
        f"[WARN] [{lang}] Translation length mismatch: translations={n_trans}, rows={n_rows}, unique_texts={n_unique}. "
        f"Skipping this language for this provider."
    )
    return False



# ---------------------------------------------------------------------
# Translation discovery + loading
# ---------------------------------------------------------------------

_TRANSLATION_FILENAME_RE = re.compile(r"^(?P<lang>[a-z]{2,3})_(?P<provider>.+)\.txt$", re.IGNORECASE)


def discover_translations(translations_dir: Path) -> Dict[str, Dict[str, Path]]:
    """
    Returns: provider -> { lang -> file_path }
    Example:
      {
        "deepl": {"es": ".../es_deepl.txt", "fr": ".../fr_deepl.txt"},
        "gpt-4o": {"es": ".../es_gpt-4o.txt", ...},
      }
    """
    if not translations_dir.exists():
        raise FileNotFoundError(
            f"translations directory not found: {translations_dir.resolve()}\n"
            "Expected a folder named 'translations' next to this script."
        )

    providers: Dict[str, Dict[str, Path]] = defaultdict(dict)

    for fp in sorted(translations_dir.glob("*.txt")):
        m = _TRANSLATION_FILENAME_RE.match(fp.name)
        if not m:
            # Skip files that don't follow the pattern (e.g. backups / notes)
            continue

        lang = m.group("lang").lower()
        provider = m.group("provider").strip().lower()

        # Normalize provider: avoid spaces and weird suffixes in output paths
        provider = re.sub(r"\s+", "_", provider)
        provider = provider.replace("/", "_")

        providers[provider][lang] = fp

    if not providers:
        raise RuntimeError(
            f"No translation files found in {translations_dir.resolve()}.\n"
            "Expected files like 'es_deepl.txt' or 'fr_gpt-4o.txt'."
        )

    return dict(providers)


def read_translation_list(fp: Path) -> List[str]:
    """
    Robust reader for your translation files.
    - Works for plain line-based files
    - Works for 'one column CSV' files (with or without ';' separators)
    """
    text = fp.read_text(encoding="utf-8", errors="replace")

    # If it looks like a 1-col CSV with separators, let pandas parse it
    if ";" in text[:2000] or "\t" in text[:2000] or "," in text[:2000]:
        try:
            df = pd.read_csv(fp, header=None, sep=";", engine="python")
            if df.shape[1] >= 1:
                return df.iloc[:, 0].astype(str).tolist()
        except Exception:
            pass

    # Fallback: treat as one translation per line
    return [line.rstrip("\n") for line in text.splitlines()]


# ---------------------------------------------------------------------
# Analyzer factory
# ---------------------------------------------------------------------

# You can extend/adjust this mapping depending on what you have installed.
# If a model is missing, the script will warn and skip that language for that provider.
SPACY_MODEL_BY_LANG = {
    "es": "es_dep_news_trf",
    "fr": "fr_dep_news_trf",
    # Common spaCy model names (may differ in your setup):
    "it": "it_core_news_lg",
    "no": "nb_core_news_lg",
    "ru": "ru_core_news_lg",
    "uk": "uk_core_news_sm",
    "sv": "sv_core_news_lg",
}


def build_analyzers(languages: List[str]) -> Tuple[Dict[str, BaseMorphologicalAnalyzer], List[str]]:
    """
    Returns (analyzers, usable_languages).

    - Arabic: QalsadiMorphAnalyzer
    - Hebrew: HebrewMorphAnalyzer
    - Others: SpaCyMorphAnalyzer(model_name)
    """
    analyzers: Dict[str, BaseMorphologicalAnalyzer] = {}
    usable: List[str] = []

    # Build shared instances so we don't reload a spaCy pipeline N times.
    spacy_cache: Dict[str, SpaCyMorphAnalyzer] = {}

    for lang in languages:
        try:
            if lang == "ar":
                analyzers[lang] = QalsadiMorphAnalyzer()
                usable.append(lang)

            elif lang == "he":
                analyzers[lang] = HebrewMorphAnalyzer()
                usable.append(lang)

            else:
                model_name = SPACY_MODEL_BY_LANG.get(lang)
                if not model_name:
                    print(f"[WARN] No spaCy model configured for '{lang}'. Skipping.")
                    continue

                if model_name not in spacy_cache:
                    morph = SpaCyMorphAnalyzer(model_name)
                    morph.load()
                    spacy_cache[model_name] = morph

                analyzers[lang] = spacy_cache[model_name]
                usable.append(lang)

        except Exception as e:
            print(f"[WARN] Could not initialize analyzer for '{lang}': {e}. Skipping.")

    return analyzers, usable


# ---------------------------------------------------------------------
# Build / load processed datasets
# ---------------------------------------------------------------------

def build_processed_dataset_for_provider(
    *,
    provider: str,
    lang_to_file: Dict[str, Path],
    base_dataset_csv: Path,
    processed_out: Path,
    rebuild: bool,
    use_multiprocessing: bool,
) -> DEvalDataset:
    """
    Creates (or loads) a processed dataset for one provider.
    The processed dataset will contain:
      - translations per language (columns: <lang>)
      - predictions per language (columns: x_gender_<lang>)
    """
    processed_out.parent.mkdir(parents=True, exist_ok=True)

    if processed_out.exists() and not rebuild:
        print(f"[{provider}] Loading processed dataset: {processed_out}")
        # Only include languages that exist in this file
        df_cols = list(pd.read_csv(processed_out, nrows=0, sep=";").columns)
        available_langs = [lang for lang in lang_to_file.keys() if lang in df_cols]
        available_preds = [lang for lang in available_langs if f"x_gender_{lang}" in df_cols]

        if not available_preds:
            raise RuntimeError(
                f"[{provider}] '{processed_out}' exists but has no x_gender columns for the discovered languages.\n"
                "Run with --rebuild-datasets 1 to regenerate it."
            )

        return DEvalDataset.from_csv(
            str(processed_out),
            text_column="text",
            sep=";",
            translation_columns={lang: lang for lang in available_langs},
            prediction_columns={lang: f"x_gender_{lang}" for lang in available_preds},
        )

    print(f"[{provider}] Building dataset from scratch (base={base_dataset_csv})")

    base_df = pd.read_csv(base_dataset_csv, sep=";")
    ds = DEvalDataset(base_df, text_column="text")

    # Add translations for this provider (only keep languages that align)
    all_languages = sorted(lang_to_file.keys())
    valid_languages: List[str] = []

    for lang in all_languages:
        translations = read_translation_list(lang_to_file[lang])
        ok = add_translations_safely(ds, lang, translations, column_name=lang, source_col="text")
        if ok:
            valid_languages.append(lang)

    if not valid_languages:
        print(f"[WARN] [{provider}] No translation files aligned with the base dataset. Skipping provider.")
        return None

    # IMPORTANT: tell DEvalDataset which translation columns exist
    ds.translation_columns = {lang: lang for lang in valid_languages}
    ds.prediction_columns = {lang: f"x_gender_{lang}" for lang in usable_languages}

    # Build analyzers ONLY for valid languages
    analyzers, usable_languages = build_analyzers(valid_languages)
    if not usable_languages:
        print(
            f"[WARN] [{provider}] No usable languages after analyzer init. "
            f"(Translations ok: {valid_languages}). Skipping provider."
        )
        return None

    # Drop languages that couldn't be analyzed (but keep their translation column in the DF)
    # The pipeline will only run on languages with analyzers configured.
    print(f"[{provider}] Usable languages for pipeline: {usable_languages}")

    # Run x-subject pipeline (creates x_gender_<lang> etc.)
    run_subject_pipeline(
        ds,
        analyzers=analyzers,
        source_column="text",
        subject_index_column="x_idx",
        output_prefix="x",
        use_multiprocessing=use_multiprocessing,
    )

    # Persist processed dataset
    ds.df.to_csv(processed_out, sep=";", index=False)
    print(f"[{provider}] Wrote processed dataset: {processed_out}")

    return ds


# ---------------------------------------------------------------------
# Analysis + plots
# ---------------------------------------------------------------------

def run_full_analysis(
    *,
    ds: DEvalDataset,
    provider: str,
    output_dir: Path,
    filter_by_sentence_style: bool,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    # Determine which languages have predictions
    langs = [
        lang for lang, pred_col in ds.prediction_columns.items()
        if pred_col in ds.df.columns
    ]
    if not langs:
        raise RuntimeError(f"[{provider}] No prediction columns found in dataset.")

    print(f"[{provider}] Languages with predictions: {langs}")

    # ---- 1) Error Analysis ----
    error_analyzer = ErrorAnalysis(ds, "x_gender")
    error_df = error_analyzer.analyze(languages=langs).T

    error_df.attrs["filename"] = f"{provider}_error_analysis"

    # Optional: show how to filter by sentence_style
    if filter_by_sentence_style and "sentence_style" in ds.df.columns:
        for style in sorted(ds.df["sentence_style"].dropna().unique()):
            style_df = error_analyzer.analyze(languages=langs, filter_col="sentence_style", filter_value=style).T
            style_df.attrs["filename"] = f"{provider}_error_analysis_sentence_style_{style}"
            save_dataframes(style_df, output_dir=output_dir)
            plot_error_analysis(style_df.T, output_dir=output_dir, filename=style_df.attrs["filename"])

    # ---- 2) Confusion Matrix Metrics ----
    cm_analyzer = ConfusionMatrix(ds, "x_gender")
    cm_df = cm_analyzer.analyze(languages=langs).T
    cm_df.attrs["filename"] = f"{provider}_confusion_metrics"

    # ---- 3) Logistic Regression (optional predictor) ----
    lr_analyzer = LogisticRegressionAnalysis(ds, "x_gender")
    lr_df = lr_analyzer.analyze(languages=langs, predictor_col="x_stereotypical")
    lr_df.attrs["filename"] = f"{provider}_logistic_regression"

    # ---- Save tables ----
    save_dataframes(error_df, cm_df, lr_df, output_dir=output_dir)

    # ---- Plots ----
    plot_error_analysis(error_df.T, output_dir=output_dir, filename=error_df.attrs["filename"])
    plot_confusion_metrics(cm_df.T, output_dir=output_dir, filename=cm_df.attrs["filename"])
    plot_logistic_regression(lr_df, output_dir=output_dir, filename=lr_df.attrs["filename"])

    print(f"[{provider}] Analysis outputs written to: {output_dir}")


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-dataset", type=str, default="DEval_dataset.csv",
                        help="Path to the base DEval dataset CSV (semicolon-separated).")
    parser.add_argument("--translations-dir", type=str, default="translations",
                        help="Folder containing translation files <lang>_<provider>.txt")
    parser.add_argument("--providers", type=str, default="all",
                        help="Comma-separated provider names (as in filenames), or 'all'.")
    parser.add_argument("--rebuild-datasets", type=int, default=0,
                        help="1 = rebuild processed datasets from translations; 0 = only load existing processed CSVs")
    parser.add_argument("--use-multiprocessing", type=int, default=0,
                        help="1 = use multiprocessing in subject pipeline; 0 = run single-process (easier for debugging)")
    parser.add_argument("--filter-by-sentence-style", type=int, default=1,
                        help="1 = also run error analysis per sentence_style if available; 0 = skip")
    args = parser.parse_args()

    base_dataset_csv = Path(args.base_dataset)
    translations_dir = Path(args.translations_dir)

    providers_map = discover_translations(translations_dir)
    requested = (
        sorted(providers_map.keys())
        if args.providers.strip().lower() == "all"
        else [p.strip().lower() for p in args.providers.split(",") if p.strip()]
    )

    processed_root = Path("processed_data")
    outputs_root = Path("outputs")
    processed_root.mkdir(exist_ok=True)
    outputs_root.mkdir(exist_ok=True)

    for provider in requested:
        if provider not in providers_map:
            print(f"[WARN] Provider '{provider}' not found in translations folder. Skipping.")
            continue

        processed_out = processed_root / f"{provider}_processed.csv"
        ds = build_processed_dataset_for_provider(
            provider=provider,
            lang_to_file=providers_map[provider],
            base_dataset_csv=base_dataset_csv,
            processed_out=processed_out,
            rebuild=bool(args.rebuild_datasets),
            use_multiprocessing=bool(args.use_multiprocessing),
        )

        if ds is None:
            continue

        run_full_analysis(
            ds=ds,
            provider=provider,
            output_dir=outputs_root / provider,
            filter_by_sentence_style=bool(args.filter_by_sentence_style),
        )


if __name__ == "__main__":
    main()
