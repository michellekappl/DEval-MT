"""Top-level DEval-MT SDK package.

Users should import from this namespace for a stable API, e.g.:
   from deval_mt import DEvalDataset, run_full_pipeline
   from deval_mt import SpaCyMorphAnalyzer, Gender
   from deval_mt import AlignmentProcessor, WordAlignment

This module re-exports the main public entry points and types from the
internal modules. Subpackages may change internals without breaking the
public API presented here.
"""

# High-level SDK API
from sdk import (
   run_subject_pipeline,
   evaluate_processed_dataset,
   run_full_pipeline,
)

# Dataset convenience
from Dataset import DEvalDataset

# Morphological analysis
from morphological_analysis.base_analyzer import BaseMorphologicalAnalyzer, MorphologicalToken
from morphological_analysis.spacy_morph_analyzer import SpaCyMorphAnalyzer
from morphological_analysis.qalsadi_morph_analyzer import QalsadiMorphAnalyzer
from morphological_analysis.gender import Gender

# Alignment utilities
from alignment.alignment_processor import AlignmentProcessor
from alignment.word_alignment import WordAlignment

# Metrics helpers
from analysis import evaluate_dataset, metrics_to_dataframe

__all__ = [
   # SDK
   'run_subject_pipeline', 'evaluate_processed_dataset', 'run_full_pipeline',
   # Dataset
   'DEvalDataset',
   # Morphological analyzers
   'BaseMorphologicalAnalyzer', 'MorphologicalToken',
   'SpaCyMorphAnalyzer', 'QalsadiMorphAnalyzer', 'Gender',
   # Alignment
   'AlignmentProcessor', 'WordAlignment',
   # Metrics
   'evaluate_dataset', 'metrics_to_dataframe',
]
