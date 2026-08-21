"""Error Analysis for gender bias evaluation in MT outputs."""

from enum import Enum
import pandas as pd
from typing import List
from ..dataset import DEvalDataset
from ..morphological_analysis.gender import Gender

class ErrorType(Enum):
    M_TO_F = "m→f"
    M_TO_N = "m→n"
    M_TO_U = "m→u"
    M_TO_D = "m→d"

    F_TO_M = "f→m"
    F_TO_N = "f→n"
    F_TO_U = "f→u"
    F_TO_D = "f→d"

    N_TO_M = "n→m"
    N_TO_F = "n→f"
    N_TO_U = "n→u"
    N_TO_D = "n→d"

    U_TO_M = "u→m"
    U_TO_F = "u→f"
    U_TO_N = "u→n"
    U_TO_D = "u→d"

    D_TO_M = "d→m"
    D_TO_F = "d→f"
    D_TO_N = "d→n"
    D_TO_U = "d→u"

    @classmethod
    def from_genders(cls, gold: Gender, pred: Gender) -> 'ErrorType':
        """Create ErrorType from gold and predicted gender values."""
        gender_map = {
            Gender.MASCULINE: 'M',
            Gender.FEMININE: 'F',
            Gender.NEUTER: 'N',
            Gender.UNKNOWN: 'U',
            Gender.DIVERSE: 'D'
        }

        gold_char = gender_map.get(gold, 'U')
        pred_char = gender_map.get(pred, 'U')

        error_name = f"{gold_char}_TO_{pred_char}"

        return cls[error_name]

class ErrorAnalysis:
    """Per-language accuracy and error-type breakdown for gender predictions
    against a gold column."""

    def __init__(self, ds: DEvalDataset, gold_col: str):
        self.ds = ds
        self.gold_col = gold_col

    def analyze(self, languages: List[str] | None = None, *, analyze_error_patterns: bool = True,filter_col:str|None=None,filter_value=None) -> pd.DataFrame:
        """Compute accuracy and error-type counts per language.

        Parameters
        ----------
        languages : list[str] | None
            Languages to analyze. Defaults to every language registered in
            `self.ds.translation_columns`.
        analyze_error_patterns : bool
            If True, include per-error-type count columns (`error_m_to_f`,
            etc.) in the output, not just totals/accuracy.
        filter_col, filter_value
            If given, restrict to rows where `filter_col == filter_value`
            before analyzing, and echo `filter_col` as a column on the result.

        Returns
        -------
        One row per language, with `language`, `sentence_style`, `total`,
        `correct`, `accuracy`, `true_error_count`, `unknown_count`, and (if
        `analyze_error_patterns`) one `error_*` column per `ErrorType`.
        """
        df=self.ds.df
        if filter_col is not None:
            df=df[df[filter_col]==filter_value]

        if languages is None:
            languages = list(self.ds.translation_columns.keys())

        if any(lang not in self.ds.translation_columns for lang in languages):
            raise ValueError(f"Some languages are not available in the dataset (unknown languages: {[lang for lang in languages if lang not in self.ds.translation_columns]})")

        results_data = []

        for lang in languages:
            pred_col = self.ds.prediction_columns.get(lang)

            if pred_col is None or pred_col not in df.columns:
                results_data.append({"language": lang, "total": len(df), "correct": 0, "accuracy": 0.0, "true_error_count": len(df), "unknown_count": 0})
                continue

            prediction_correct = df[
                ((df[self.gold_col] == df[pred_col]) & (df[pred_col] != 'UNKNOWN')) |  # Exact matches (excluding UNKNOWN preds)
                ((df[self.gold_col] == 'DIVERSE') & (df[pred_col] == 'NEUTER'))  # analyzers can't predict DIVERSE, so NEUTER is the closest achievable signal and counts as correct
            ]
            total = len(df)
            correct = len(prediction_correct)
            accuracy = correct / total if total > 0 else 0.0
            unknown_count = 0

            error_types = {
                ErrorType.M_TO_F: 0,
                ErrorType.M_TO_U: 0,
                ErrorType.F_TO_M: 0,
                ErrorType.F_TO_U: 0,
                ErrorType.D_TO_M: 0,
                ErrorType.D_TO_F: 0,
                ErrorType.D_TO_U: 0,
                ErrorType.M_TO_N: 0,
                ErrorType.F_TO_N: 0,
            }
            for _, row in df.iterrows():
                gold = row.get(self.gold_col)
                pred = row.get(pred_col)

                # Skip if gold is UNKNOWN (can't evaluate errors without known gold standard)
                if gold == "UNKNOWN":
                    continue

                # Skip DIVERSE -> NEUTER as it's considered correct
                if gold == "DIVERSE" and pred == "NEUTER":
                    continue

                # Count any non-exact match as an error, including UNKNOWN predictions
                if gold is not None and pred is not None and gold != pred:
                    error_types[ErrorType.from_genders(Gender[gold], Gender[pred])] += 1
                    if pred == "UNKNOWN":
                        unknown_count +=1
            # Create a row for this language
            row_data = {
                "language": lang,
                "sentence_style": filter_value,
                "total": total,
                "correct": correct,
                "accuracy": accuracy,
                "true_error_count": total - correct - unknown_count,
                "unknown_count": unknown_count,
            }

            if filter_col is not None:
                row_data[filter_col] = filter_value

            if analyze_error_patterns:
                for error_type, count in error_types.items():
                    row_data[f"error_{error_type.name.lower()}"] = count

            results_data.append(row_data)

        return pd.DataFrame(results_data)

    @staticmethod
    def grouped(
        dataset: DEvalDataset,
        gold_col: str,
        scope: str,
        *,
        sentence_style=None,
        group_col: str | None = None,
        group_labels: dict | None = None,
        plot_group=None,
        plot_dir: str | None = None,
        filename_prefix: str = "",
    ) -> List[pd.DataFrame]:
        """Run `analyze()` once per value of `group_col` (or once, ungrouped,
        if `group_col` is None), tagging every resulting row-set so multiple
        calls -- across scopes, across a study's whole evaluation -- can be
        concatenated into one consolidated error-analysis table instead of one
        file per scope/group.

        Every returned row gets:
          - "scope": the `scope` argument (e.g. "names", "romantic").
          - "sentence_style": the `sentence_style` argument, written as-is
            (overrides whatever `analyze()` itself would set here -- it isn't
            used to filter; filter `dataset` yourself first if needed).
          - "pairing": `group_labels[value]`, if grouped.

        Parameters
        ----------
        dataset, gold_col : as for `ErrorAnalysis`.
        scope : str
            Label for this evaluation's rows, e.g. "names", "romantic".
        group_col, group_labels : str, {raw_value: label}
            If given, run one `analyze()` pass per `group_labels` entry,
            filtering `dataset.df[group_col] == raw_value`. If `group_col` is
            None, runs once over the whole dataset (no "pairing" column).
        plot_group : label | None
            If given (and `plot_dir` is given), render the full plot suite
            (`error_analysis.png` + `confusion_flow.png`, from
            `deval_mt.analysis.plotting`) for the group whose label matches
            this value -- or, if `group_col` is None, any truthy value plots
            the whole (ungrouped) dataset.
        plot_dir : str | None
            Directory to render plots into.
        filename_prefix : str
            Prepended to every plot filename this call writes.

        Returns
        -------
        list of DataFrames (one per group, or one if ungrouped) -- concatenate
        these (and other scopes/calls) into one consolidated error_analysis.csv.
        """
        from .plotting import plot_error_analysis, plot_confusion_flow

        groups = [(None, None)] if group_col is None else list(group_labels.items())

        rows = []
        for raw_value, label in groups:
            sub_ds = dataset
            if group_col is not None:
                sub_ds = DEvalDataset(dataset.df[dataset.df[group_col] == raw_value], dataset.text_column)
                sub_ds.translation_columns = dataset.translation_columns
                sub_ds.prediction_columns = dataset.prediction_columns

            err = ErrorAnalysis(sub_ds, gold_col).analyze()

            should_plot = plot_dir is not None and (group_col is None or label == plot_group)
            if should_plot:
                plot_error_analysis(err, output_dir=plot_dir, filename=f"{filename_prefix}error_analysis.png")
                plot_confusion_flow(
                    sub_ds.df, gold_col, sub_ds.prediction_columns, output_dir=plot_dir,
                    filename=f"{filename_prefix}confusion_flow.png",
                )

            if sentence_style is not None:
                err["sentence_style"] = sentence_style
            if label is not None:
                err["pairing"] = label
            err["scope"] = scope
            rows.append(err)

        return rows
