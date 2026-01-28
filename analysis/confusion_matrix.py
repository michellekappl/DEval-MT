"""Confusion Matrix Analysis for gender bias evaluation."""

import pandas as pd
from typing import Dict, List, Any
import numpy as np
from Dataset import DEvalDataset
from morphological_analysis.gender import Gender


class ConfusionMatrix:
    """Generate and analyze confusion matrices for gender predictions."""

    def __init__(self, ds: DEvalDataset, gold_col: str):
        self.ds = ds
        self.gold_col = gold_col

    def __generate_matrix(self, language: str,df:pd.DataFrame) -> pd.DataFrame:
        """Generate a confusion matrix for gender predictions for a specific language."""
        pred_col = self.ds.prediction_columns.get(language)

        if pred_col is None:
            raise ValueError(f"No prediction column found for language: {language}")

        if self.gold_col not in self.ds.df.columns or pred_col not in self.ds.df.columns:
            raise ValueError("Specified columns not found in DataFrame")

        # Get unique gender values
        gold_values = df[self.gold_col].dropna().unique()
        pred_values = df[pred_col].dropna().unique()
        all_genders = sorted(set(gold_values) | set(pred_values))

        # Initialize matrix
        matrix = pd.DataFrame(0, index=all_genders, columns=all_genders)

        # Fill matrix
        for _, row in df.iterrows():
            gold = row.get(self.gold_col)
            pred = row.get(pred_col)

            if gold is not None and pred is not None:
                if gold in all_genders and pred in all_genders:
                    matrix.loc[gold, pred] += 1
        #print(matrix)
        return matrix

    def __calculate_metrics(self, language: str,df:pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """Calculate precision, recall, and F1-score for each gender class for a specific language."""
        matrix = self.__generate_matrix(language,df)
        metrics = {}

        for gender in matrix.index:
            # True Positives, False Positives, False Negatives
            tp = matrix.loc[gender, gender]
            fp = matrix[gender].sum() - tp
            fn = matrix.loc[gender].sum() - tp

            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

            metrics[str(gender)] = {
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'support': tp + fn
            }

        return metrics

    def analyze(self, languages: List[str] | None = None,filter_col:str|None=None,filter_value=None) -> pd.DataFrame:
        """Analyze confusion matrix metrics for multiple languages and return as DataFrame."""
        df=self.ds.df
        if filter_col is not None:
            df=df[df[filter_col]==filter_value]
        if languages is None:
            languages = list(self.ds.translation_columns.keys())

        if any(lang not in self.ds.translation_columns for lang in languages):
            raise ValueError(f"Some languages are not available in the dataset (unknown languages: {[lang for lang in languages if lang not in self.ds.translation_columns]})")

        results_data = []

        for lang in languages:
            try:
                metrics = self.__calculate_metrics(lang,df)

                # Create a row for this language
                row_data: Dict[str, Any] = {'language': lang}

                if filter_col is not None:
                    row_data[filter_col]=filter_value

                # Add metrics for each gender class
                for gender, gender_metrics in metrics.items():
                    row_data[f'{gender}_precision'] = gender_metrics['precision']
                    row_data[f'{gender}_recall'] = gender_metrics['recall']
                    row_data[f'{gender}_f1_score'] = gender_metrics['f1_score']
                    row_data[f'{gender}_support'] = gender_metrics['support']

                results_data.append(row_data)

            except Exception as e:
                # Handle cases where metrics can't be calculated for a language
                row_data: Dict[str, Any] = {'language': lang, 'error': str(e)}
                results_data.append(row_data)

        return pd.DataFrame(results_data)
