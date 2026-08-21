from __future__ import annotations

from typing import List, Optional, Mapping
import pandas as pd

from .dataset import DEvalDataset
from .alignment import AlignmentProcessor
from .alignment.word_alignment import WordAlignment
from .morphological_analysis.base_analyzer import BaseMorphologicalAnalyzer
from .morphological_analysis.gender import Gender
from .analysis import ErrorAnalysis, ConfusionMatrix, LogisticRegressionAnalysis
from .analysis.plotting import (
    plot_error_analysis,
    plot_confusion_flow,
    plot_stereotypicality,
    format_significance_table,
    save_dataframes,
)


def run_subject_pipeline(
    dataset: DEvalDataset,
    analyzers: Mapping[str, BaseMorphologicalAnalyzer],
    *,
    source_column: str,
    subject_index_column: str,
    output_prefix: Optional[str] = None,
    languages: Optional[List[str]] = None,
    alignment_model: str = "google-bert/bert-base-multilingual-cased",
    token_type: str = "bpe",
    matching_method: str = "itermax",
    # Alignment reuse
    skip_alignment_if_present: bool = True,
    inplace: bool = True,
    # Parallelism
    use_multiprocessing: bool = True,
    max_workers: Optional[int] = None,
    # Multiple predictions and averaging
    num_predictions: int = 1,
) -> DEvalDataset:
    """Run alignment + phrase extraction + gender detection for ONE subject column.

    This function is deliberately generic; to evaluate multiple annotated
    subjects (e.g. `x_idx` and `y_idx`) call it twice with different
    `subject_index_column` and distinct `output_prefix` values (e.g. 'x', 'y').

    Parameters
    ----------
    dataset : DEvalDataset
       Dataset with source + translation columns already attached.
    source_column : str
       Name of the source text column.
    subject_index_column : str
       Column containing integer index of the (head) subject token in source.
    output_prefix : str | None
       Prefix for generated columns. If None and subject_index_column ends
       with '_idx', that prefix is derived (e.g. 'x_idx' -> 'x'). Otherwise
       defaults to 'subject'.
    skip_alignment_if_present : bool
       If True and columns alignment_<lang> already exist, re-use them.
    inplace : bool
       If False, the provided dataset is cloned first and all derived columns
       are added to the clone, leaving the original object unmodified. If True , the dataset is mutated in place.
    """
    if not inplace:
        dataset = dataset.clone()
    if languages is None:
        languages = list(dataset.translation_columns.keys())

    if output_prefix is None:
        output_prefix = (
            subject_index_column[:-4] if subject_index_column.endswith("_idx") else "subject"
        )

    # 1. Alignment (optional reuse)
    need_alignment = False
    for lang in languages:
        if f"alignment_{lang}" not in dataset.df.columns:
            need_alignment = True
            break
    if need_alignment or not skip_alignment_if_present:
        processor = AlignmentProcessor(
            alignment_model,
            token_type,
            matching_method,
            use_multiprocessing=use_multiprocessing,
            max_workers=max_workers,
        )
        alignments = processor.process_multiple(dataset, original_column=source_column)
        for lang in languages:
            col = dataset.translation_columns[lang]
            dataset.df[f"alignment_{lang}"] = [wa.serialize() for wa in alignments[col]]

    # 3. Subject phrase indices (gets indices of all words in subject phrase, e.g. with preceding article)
    # "I like the food" → [2, 3] for subject index 3 ("food") with article_offset -1
    phrase_indices_col = f"{output_prefix}_phrase_indices"

    def build_indices(row: pd.Series):
        if pd.isna(row.get(subject_index_column)):
            return []
        base = int(row[subject_index_column])

        adjectives = row.adjective
        if adjectives == "none":
            article_offset = -1
        else:
            article_offset = -2

        start = base + article_offset
        if start < 0:
            start = 0
        return list(range(start, base + 1))

    dataset.df[phrase_indices_col] = dataset.df.apply(build_indices, axis=1)

    # 4. Extract aligned phrases per language
    def extract_phrase(row, lang):
        alignment_col = f"alignment_{lang}"
        wa = WordAlignment.from_serialized(
            row[source_column], row[dataset.translation_columns[lang]], row[alignment_col]
        )
        tokens = row[dataset.translation_columns[lang]].split()
        target_indices = []
        for idx in row[phrase_indices_col]:
            target_indices.extend(wa.get_counterpart(idx))
        target_indices = sorted(set(i for i in target_indices if i >= 0))
        return " ".join(tokens[i] for i in target_indices if i < len(tokens))

    for lang in languages:
        dataset.df[f"{output_prefix}_phrase_{lang}"] = dataset.df.apply(
            lambda r: extract_phrase(r, lang), axis=1
        )

    # 5. Predict genders per language
    def predict_gender_with_votes(lang: str, phrase: str):
        """Returns tuple of (final_gender, list_of_individual_votes)"""
        if not phrase:
            return ("UNKNOWN", [])
        if lang not in analyzers:
            raise KeyError(f"No analyzer provided for language '{lang}'.")
        analyzer = analyzers[lang]

        if num_predictions == 1:
            # Single prediction
            tokens = analyzer.tokenize_sentence(phrase)
            gender = analyzer.get_phrase_gender(tokens).name if tokens else "UNKNOWN"
            return (gender, [gender])
        else:
            # Multiple predictions with majority voting
            from collections import Counter

            predictions = []
            for _ in range(num_predictions):
                tokens = analyzer.tokenize_sentence(phrase)
                gender = analyzer.get_phrase_gender(tokens).name if tokens else "UNKNOWN"
                predictions.append(gender)

            # Count votes and return the most common gender
            vote_counts = Counter(predictions)
            most_common = vote_counts.most_common(1)
            if not most_common:
                return ("UNKNOWN", predictions)

            gender, count = most_common[0]
            # If there's a tie, be conservative
            if len(vote_counts) > 1:
                second_count = vote_counts.most_common(2)[1][1] if len(vote_counts) >= 2 else 0
                if count == second_count:
                    return ("UNKNOWN", predictions)

            return (gender, predictions)

    for lang in languages:
        # Apply prediction and store both final gender and votes
        results = dataset.df[f"{output_prefix}_phrase_{lang}"].apply(
            lambda p: predict_gender_with_votes(lang, p)
        )
        dataset.df[f"{output_prefix}_gender_{lang}"] = results.apply(lambda x: x[0])
        dataset.df[f"{output_prefix}_votes_{lang}"] = results.apply(lambda x: x[1])
        dataset.prediction_columns[lang] = f"{output_prefix}_gender_{lang}"

    # 6. Return augmented dataset
    return dataset


def evaluate_processed_dataset(
    dataset: DEvalDataset,
    gold_col: str = "x_gender",
    *,
    predictor_col: Optional[str] = "x_stereotypical",
    filter_col: Optional[str] = None,
    filter_value=None,
    plot_dir: Optional[str] = None,
    output_dir: Optional[str] = None,
    filename_prefix: str = "",
) -> dict[str, pd.DataFrame]:
    """Run the standard analysis suite (error rates, confusion matrix, and
    optionally a stereotype-congruence logistic regression) on a dataset
    that has ALREADY been through `run_subject_pipeline` -- no alignment or
    gender prediction happens here, only evaluation of existing predictions
    against `gold_col`.

    This is the analysis half of what `run_full_pipeline` does in one call;
    use it directly when predictions already exist (e.g. loaded from a
    `*_processed.csv`) and only the analysis needs to be (re)computed.

    Parameters
    ----------
    dataset : DEvalDataset
        Dataset with prediction_columns already populated (e.g. by
        `run_subject_pipeline`, or loaded via `DEvalDataset.from_csv` with
        `prediction_columns` supplied).
    gold_col : str
        Column holding the gold label to score predictions against.
    predictor_col : str | None
        Column to regress prediction-correctness on (e.g. stereotype-
        congruence). Pass None to skip the logistic regression (e.g. if no
        such predictor exists in this dataset).
    filter_col, filter_value
        Optional row filter applied identically to every analysis (e.g.
        `filter_col="sentence_style", filter_value=1`).
    plot_dir : str | None
        If given, render the full plot suite into this directory:
        `error_analysis.png` (per-language table + error-type heatmap),
        `confusion_flow.png` (gold->predicted Sankey ribbons per language),
        and, if `predictor_col` was given, `stereotypicality.png`
        (LOWESS-smoothed accuracy vs. `predictor_col`), via
        `deval_mt.analysis.plotting`.
    output_dir : str | None
        If given, save the three result DataFrames as `error_analysis.csv`,
        `confusion_matrix.csv`, and (if computed) `logistic_regression.csv`
        in this directory -- one file each, via `save_dataframes`.
    filename_prefix : str
        Prepended to every filename this call writes (plots and CSVs) --
        e.g. `"gpt-4o_"`, so multiple calls (different models, or different
        scopes on the same model) can share one `plot_dir`/`output_dir`
        without overwriting each other.

    Returns
    -------
    dict with keys "error_analysis", "confusion_matrix", and (if
    `predictor_col` is not None) "logistic_regression", each a DataFrame.
    The logistic regression DataFrame includes a "significance" column
    (*/**/*** on p_value).
    """
    results: dict[str, pd.DataFrame] = {
        "error_analysis": ErrorAnalysis(dataset, gold_col).analyze(
            filter_col=filter_col, filter_value=filter_value
        ),
        "confusion_matrix": ConfusionMatrix(dataset, gold_col).analyze(
            filter_col=filter_col, filter_value=filter_value
        ),
    }
    if predictor_col is not None:
        results["logistic_regression"] = format_significance_table(
            LogisticRegressionAnalysis(dataset, gold_col).analyze(
                predictor_col=predictor_col, filter_col=filter_col, filter_value=filter_value
            )
        )

    if plot_dir is not None or output_dir is not None:
        df = dataset.df
        if filter_col is not None:
            df = df[df[filter_col] == filter_value]

    if plot_dir is not None:
        plot_error_analysis(results["error_analysis"], output_dir=plot_dir, filename=f"{filename_prefix}error_analysis.png")
        plot_confusion_flow(
            df, gold_col, dataset.prediction_columns, output_dir=plot_dir, filename=f"{filename_prefix}confusion_flow.png"
        )
        if "logistic_regression" in results:
            plot_stereotypicality(
                df,
                gold_col,
                predictor_col,
                dataset.prediction_columns,
                output_dir=plot_dir,
                filename=f"{filename_prefix}stereotypicality.png",
            )
    if output_dir is not None:
        for key, filename in (
            ("error_analysis", "error_analysis"),
            ("confusion_matrix", "confusion_matrix"),
            ("logistic_regression", "logistic_regression"),
        ):
            if key in results:
                results[key].attrs["filename"] = f"{filename_prefix}{filename}"
        save_dataframes(*results.values(), output_dir=output_dir)

    return results


def run_full_pipeline(
    dataset: DEvalDataset,
    analyzers: Mapping[str, BaseMorphologicalAnalyzer],
    *,
    source_column: str,
    subject_index_column: str,
    gold_col: str = "x_gender",
    predictor_col: Optional[str] = "x_stereotypical",
    **pipeline_kwargs,
) -> tuple[DEvalDataset, dict[str, pd.DataFrame]]:
    """Convenience wrapper: `run_subject_pipeline` followed immediately by
    `evaluate_processed_dataset` on its output. Accepts the same keyword
    arguments as `run_subject_pipeline` (passed through via `pipeline_kwargs`,
    e.g. `output_prefix`, `languages`, `num_predictions`).

    Returns
    -------
    (dataset, analysis_results) -- the augmented dataset (with alignment,
    phrase, and gender-prediction columns added) and the dict returned by
    `evaluate_processed_dataset`.
    """
    dataset = run_subject_pipeline(
        dataset,
        analyzers,
        source_column=source_column,
        subject_index_column=subject_index_column,
        **pipeline_kwargs,
    )
    results = evaluate_processed_dataset(dataset, gold_col, predictor_col=predictor_col)
    return dataset, results


__all__ = [
    "run_subject_pipeline",
    "evaluate_processed_dataset",
    "run_full_pipeline",
    "ErrorAnalysis",
    "ConfusionMatrix",
    "LogisticRegressionAnalysis",
]
