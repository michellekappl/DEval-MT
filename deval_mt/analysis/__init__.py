"""Analysis module for DEval-MT statistical analyses."""

from .error_analysis import ErrorAnalysis
from .confusion_matrix import ConfusionMatrix
from .logistic_regression import LogisticRegressionAnalysis
from .significance import test_direction_skew, test_group_gap, test_paired_gap
from .plotting import (
   plot_error_analysis,
   plot_confusion_flow,
   plot_gender_composition,
   plot_stereotypicality,
   plot_accuracy_heatmap,
   format_significance_table,
   save_dataframes,
)
from .style_comparison import compare_accuracy_by_language

__all__ = [
   'ErrorAnalysis',
   'ConfusionMatrix',
   'LogisticRegressionAnalysis',
   'test_direction_skew',
   'test_group_gap',
   'test_paired_gap',
   'plot_error_analysis',
   'plot_confusion_flow',
   'plot_gender_composition',
   'plot_stereotypicality',
   'plot_accuracy_heatmap',
   'format_significance_table',
   'save_dataframes',
   'compare_accuracy_by_language',
]
   