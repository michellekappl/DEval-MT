from __future__ import annotations

from typing import List, Optional, Mapping
import pandas as pd

from Dataset import DEvalDataset
from alignment import AlignmentProcessor
from alignment.word_alignment import WordAlignment
from morphological_analysis.base_analyzer import BaseMorphologicalAnalyzer
from morphological_analysis.gender import Gender
from analysis import ErrorAnalysis, ConfusionMatrix, LogisticRegressionAnalysis

def run_subject_pipeline(
   dataset: DEvalDataset,
   analyzers: Mapping[str, BaseMorphologicalAnalyzer],
   *,
   source_column: str,
   subject_index_column: str,
   output_prefix: Optional[str] = None,
   languages: Optional[List[str]] = None,
   alignment_model: str = 'google-bert/bert-base-multilingual-cased',
   token_type: str = 'bpe',
   matching_method: str = 'itermax',
   # Subject window logic
   article_offset: int = 0,
   # Alignment reuse
   skip_alignment_if_present: bool = True,
   inplace: bool = True,
   # Parallelism
   use_multiprocessing: bool = True,
   max_workers: Optional[int] = None,
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
   article_offset : int
      Negative values include preceding tokens (e.g., an article). 0 means
      only the subject token.
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
      output_prefix = subject_index_column[:-4] if subject_index_column.endswith('_idx') else 'subject'

   # 1. Alignment (optional reuse)
   need_alignment = False
   for lang in languages:
      if f'alignment_{lang}' not in dataset.df.columns:
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
         dataset.df[f'alignment_{lang}'] = [wa.serialize() for wa in alignments[col]]

   # 3. Subject phrase indices (gets indices of all words in subject phrase, e.g. with preceding article)
   # "I like the food" → [2, 3] for subject index 3 ("food") with article_offset -1
   phrase_indices_col = f'{output_prefix}_phrase_indices'
   def build_indices(row: pd.Series):
      if pd.isna(row.get(subject_index_column)):
         return []
      base = int(row[subject_index_column])
      start = base + article_offset
      if start < 0:
         start = 0
      return list(range(start, base + 1))
   dataset.df[phrase_indices_col] = dataset.df.apply(build_indices, axis=1)

   # 4. Extract aligned phrases per language
   def extract_phrase(row, lang):
      alignment_col = f'alignment_{lang}'
      wa = WordAlignment.from_serialized(row[source_column], row[dataset.translation_columns[lang]], row[alignment_col])
      tokens = row[dataset.translation_columns[lang]].split()
      target_indices = []
      for idx in row[phrase_indices_col]:
         target_indices.extend(wa.get_counterpart(idx))
      target_indices = sorted(set(i for i in target_indices if i >= 0))
      return ' '.join(tokens[i] for i in target_indices if i < len(tokens))

   for lang in languages:
      dataset.df[f'{output_prefix}_phrase_{lang}'] = dataset.df.apply(lambda r: extract_phrase(r, lang), axis=1)

   # 5. Predict genders per language
   def predict_gender(lang: str, phrase: str):
      if not phrase:
         return 'unknown'
      if lang not in analyzers:
         raise KeyError(f"No analyzer provided for language '{lang}'.")
      analyzer = analyzers[lang]
      tokens = analyzer.tokenize_sentence(phrase)
      return analyzer.get_phrase_gender(tokens).name if tokens else 'unknown'

   for lang in languages:
      dataset.df[f'{output_prefix}_gender_{lang}'] = dataset.df[f'{output_prefix}_phrase_{lang}'].apply(lambda p: predict_gender(lang, p))
      dataset.prediction_columns[lang] = f'{output_prefix}_gender_{lang}'

   # 6. Return augmented dataset
   return dataset

__all__ = [
   'run_subject_pipeline',
   'ErrorAnalysis',
   'ConfusionMatrix',
   'LogisticRegressionAnalysis',
]
