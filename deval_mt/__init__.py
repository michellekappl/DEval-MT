"""Top-level DEval-MT SDK package.

Users should import from this namespace for a stable API, e.g.:
   from deval_mt import DEvalDataset, run_full_pipeline
   from deval_mt import SpaCyMorphAnalyzer, HebrewMorphAnalyzer, Gender
   from deval_mt import AlignmentProcessor, WordAlignment

This module re-exports the main public entry points and types from the
internal modules. Subpackages may change internals without breaking the
public API presented here.
"""

# High-level SDK API
from .sdk import (
   run_subject_pipeline,
   evaluate_processed_dataset,
   run_full_pipeline,
)

# Dataset convenience
from .dataset import DEvalDataset

# Morphological analysis
from .morphological_analysis.base_analyzer import BaseMorphologicalAnalyzer, MorphologicalToken
from .morphological_analysis.spacy_morph_analyzer import SpaCyMorphAnalyzer
from .morphological_analysis.qalsadi_morph_analyzer import QalsadiMorphAnalyzer
from .morphological_analysis.hebrew_morph_analyzer import HebrewMorphAnalyzer
from .morphological_analysis.gender import Gender

# Alignment utilities
from .alignment.alignment_processor import AlignmentProcessor
from .alignment.word_alignment import WordAlignment

# Analysis / statistics helpers
from .analysis import (
   ErrorAnalysis,
   ConfusionMatrix,
   LogisticRegressionAnalysis,
   test_direction_skew,
   test_group_gap,
   test_paired_gap,
   plot_error_analysis,
   plot_confusion_flow,
   plot_gender_composition,
   plot_stereotypicality,
   plot_accuracy_heatmap,
   format_significance_table,
   save_dataframes,
   compare_accuracy_by_language,
)

__all__ = [
   # SDK
   'run_subject_pipeline', 'evaluate_processed_dataset', 'run_full_pipeline',
   # Dataset
   'DEvalDataset',
   # Morphological analyzers
   'BaseMorphologicalAnalyzer', 'MorphologicalToken',
   'SpaCyMorphAnalyzer', 'QalsadiMorphAnalyzer', 'HebrewMorphAnalyzer', 'Gender',
   # Alignment
   'AlignmentProcessor', 'WordAlignment',
   # Analysis / statistics
   'ErrorAnalysis', 'ConfusionMatrix', 'LogisticRegressionAnalysis',
   'test_direction_skew', 'test_group_gap', 'test_paired_gap',
   'plot_error_analysis', 'plot_confusion_flow', 'plot_gender_composition', 'plot_stereotypicality',
   'plot_accuracy_heatmap', 'format_significance_table', 'save_dataframes', 'compare_accuracy_by_language',
]
