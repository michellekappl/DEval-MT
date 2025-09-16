"""Minimal evaluation utilities (accuracy only).

For now we compute pure accuracy per language, given an explicit gold column
and predicted columns named by a prefix (e.g., 'subject_gender_es').

Exports:
   - evaluate_dataset(df, languages, predicted_prefix='subject_gender_', gold_columns=(...), parse_gold=..., parse_pred=...)
      -> Dict[str, Dict[str, float|int]] with keys: accuracy, correct, total
   - metrics_to_dataframe(metrics) -> tidy DataFrame (language, accuracy, total, correct)
"""
from __future__ import annotations

from typing import Dict, Iterable, List, Tuple, Optional, Callable, Any
import pandas as pd
from collections import Counter

from morphological_analysis.gender import Gender

# ------------------------------- Core Logic -------------------------------- #

def evaluate_dataset(
   df: pd.DataFrame,
   languages: Iterable[str],
   *,
   predicted_prefix: str = 'subject_gender_',
   gold_columns: Optional[Tuple[str, ...]] = None,
   parse_gold: Callable[[Any], Any],
   parse_pred: Callable[[Any], Any],
) -> Dict[str, Dict[str, float | int]]:
   """Compute pure accuracy per language.

   gold_columns must be provided as a 1-tuple, e.g., ("x_gender",).
   """
   if not gold_columns or len(gold_columns) != 1:
      raise ValueError("Provide exactly one gold column via gold_columns=(<col>,).")
   gold_col = gold_columns[0]

   if gold_col not in df.columns:
      raise ValueError(f"Gold gender column '{gold_col}' not in DataFrame.")

   results: Dict[str, Dict[str, float | int]] = {}
   for lang in languages:
      pred_col = f"{predicted_prefix}{lang}"
      if pred_col not in df.columns:
         raise ValueError(f"Missing predicted column '{pred_col}' for language '{lang}'.")

      total = 0
      correct = 0
      for _, row in df.iterrows():
         g = parse_gold(row.get(gold_col))
         if g == Gender.UNKNOWN:
            continue
         p = parse_pred(row.get(pred_col))
         total += 1
         if g == p:
            correct += 1
      acc = (correct / total) if total else 0.0
      results[lang] = {
         'accuracy': acc,
         'correct': correct,
         'total': total,
      }

   return results

# ------------------------------ Presentation ------------------------------- #

def metrics_to_dataframe(metrics: Dict[str, Dict[str, float | int]]) -> pd.DataFrame:
   """Convert simple metrics dict to DataFrame (language, accuracy, total, correct)."""
   rows = [
      {
         'language': lang,
         'accuracy': vals.get('accuracy', 0.0),
         'total': vals.get('total', 0),
         'correct': vals.get('correct', 0),
      }
      for lang, vals in metrics.items()
   ]
   return pd.DataFrame(rows)

__all__ = [
   'evaluate_dataset',
   'metrics_to_dataframe',
]
