"""Error Analysis for gender bias evaluation in MT outputs."""

from enum import Enum
import pandas as pd
from typing import List
from Dataset import DEvalDataset
from morphological_analysis.gender import Gender


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
    def from_genders(cls, gold: Gender, pred: Gender) -> "ErrorType":
        gender_map = {
            Gender.MASCULINE: "M",
            Gender.FEMININE: "F",
            Gender.NEUTER: "N",
            Gender.UNKNOWN: "U",
            Gender.DIVERSE: "D",
        }

        gold_char = gender_map.get(gold, "U")
        pred_char = gender_map.get(pred, "U")

        return cls[f"{gold_char}_TO_{pred_char}"]


class OutcomeType(Enum):
    EXACT = "exact"
    SEMANTIC_OK = "semantic_ok"
    ERROR = "error"
    UNRESOLVED = "unresolved"


def evaluate_gender_pair(gold: Gender, pred: Gender) -> OutcomeType:
    # Unknowns are unresolved
    if gold == Gender.UNKNOWN or pred == Gender.UNKNOWN:
        return OutcomeType.UNRESOLVED

    # Exact grammatical match
    if gold == pred:
        return OutcomeType.EXACT

    # Diverse → Neutral is exact by definition
    if gold == Gender.DIVERSE and pred == Gender.NEUTER:
        return OutcomeType.EXACT

    # Masculine/Feminine → Neutral is acceptable but imperfect
    if pred == Gender.NEUTER and gold in {Gender.MASCULINE, Gender.FEMININE}:
        return OutcomeType.SEMANTIC_OK

    return OutcomeType.ERROR


class ErrorAnalysis:
    def __init__(self, ds: DEvalDataset, gold_col: str):
        self.ds = ds
        self.gold_col = gold_col

    def analyze(
        self,
        languages: List[str] | None = None,
        *,
        analyze_error_patterns: bool = True,
    ) -> pd.DataFrame:

        if languages is None:
            languages = list(self.ds.translation_columns.keys())

        if any(lang not in self.ds.translation_columns for lang in languages):
            raise ValueError(
                f"Some languages are not available in the dataset "
                f"(unknown languages: "
                f"{[lang for lang in languages if lang not in self.ds.translation_columns]})"
            )

        results_data = []

        for lang in languages:
            pred_col = self.ds.prediction_columns.get(lang)
            total = len(self.ds.df)

            outcome_counts = {
                OutcomeType.EXACT: 0,
                OutcomeType.SEMANTIC_OK: 0,
                OutcomeType.ERROR: 0,
                OutcomeType.UNRESOLVED: 0,
            }

            error_types = {et: 0 for et in ErrorType}

            for _, row in self.ds.df.iterrows():
                gold = row.get(self.gold_col)
                pred = row.get(pred_col)

                gold_enum = Gender[gold] if gold is not None else Gender.UNKNOWN
                pred_enum = Gender[pred] if pred is not None else Gender.UNKNOWN

                outcome = evaluate_gender_pair(gold_enum, pred_enum)
                outcome_counts[outcome] += 1

                if outcome == OutcomeType.ERROR:
                    error_types[
                        ErrorType.from_genders(gold_enum, pred_enum)
                    ] += 1

            strict_accuracy = (
                outcome_counts[OutcomeType.EXACT] / total if total > 0 else 0.0
            )

            semantic_accuracy = (
                (
                    outcome_counts[OutcomeType.EXACT]
                    + outcome_counts[OutcomeType.SEMANTIC_OK]
                )
                / total
                if total > 0
                else 0.0
            )

            row_data = {
                "language": lang,
                "total": total,
                "exact": outcome_counts[OutcomeType.EXACT],
                "semantic_ok": outcome_counts[OutcomeType.SEMANTIC_OK],
                "error": outcome_counts[OutcomeType.ERROR],
                "unresolved": outcome_counts[OutcomeType.UNRESOLVED],
                "strict_accuracy": strict_accuracy,
                "semantic_accuracy": semantic_accuracy,
            }

            for error_type, count in error_types.items():
                row_data[f"error_{error_type.name.lower()}"] = count

            results_data.append(row_data)

        return pd.DataFrame(results_data)
