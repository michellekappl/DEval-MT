"""High-level SDK facade for streamlined pipeline usage.

This wraps the current prototype steps (see test.py) into a minimal, opinionated
API while still allowing customization (custom analyzers, model names, etc.).

Alignment note: only the 'itermax' matching method is currently supported for
performance and simplicity. The parameter is still exposed for future‑proofing.

Primary entrypoints:
   - evaluate_processed_dataset(...): runs metrics on an already processed dataframe
   - run_full_pipeline(...): convenience = build + evaluate

The functions return pandas DataFrames / dicts so users can further analyze.
"""
from __future__ import annotations

from typing import Iterable, List, Optional, Mapping
import pandas as pd

from Dataset import DEvalDataset
from alignment import AlignmentProcessor
from alignment.word_alignment import WordAlignment
from morphological_analysis.base_analyzer import BaseMorphologicalAnalyzer
from analysis import evaluate_dataset, metrics_to_dataframe
from morphological_analysis.gender import Gender

# NOTE: Analyzers passed to SDK functions must already be fully initialized
# (e.g., spaCy models loaded). The SDK will not auto-load analyzers.

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
) -> pd.DataFrame:
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
   # Note: The gold gender column is not used during processing; it's only
   # used at evaluation time. See run_full_pipeline/evaluate_processed_dataset.
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
      return str(analyzer.get_phrase_gender(tokens)) if tokens else 'unknown'

   for lang in languages:
      dataset.df[f'{output_prefix}_gender_{lang}'] = dataset.df[f'{output_prefix}_phrase_{lang}'].apply(lambda p: predict_gender(lang, p))

   # 6. Return augmented dataframe copy
   return dataset.df.copy()

def evaluate_processed_dataset(
   df: pd.DataFrame,
   languages: Iterable[str],
   *,
   gold_gender_column: str,
   output_prefix: str = 'subject',
):
   """Evaluate processed dataframe against an explicit gold gender column."""
   # Default parsers preserving prior behavior
   def _parse_gold(v):
      if pd.isna(v):
         return Gender.UNKNOWN
      s = str(v).strip().lower()
      return {'m': Gender.MASCULINE, 'f': Gender.FEMININE, 'd': getattr(Gender, 'DIVERSE', Gender.UNKNOWN)}.get(s, Gender.UNKNOWN)

   def _parse_pred(v):
      if v is None or (isinstance(v, float) and pd.isna(v)):
         return Gender.UNKNOWN
      s = str(v).strip().lower()
      if s in {'', 'unknown', 'none'}:
         return Gender.UNKNOWN
      if s.startswith('gender.'):
         tail = s.split('.', 1)[1]
         return {
            'masculine': Gender.MASCULINE,
            'feminine': Gender.FEMININE,
            'diverse': getattr(Gender, 'DIVERSE', Gender.UNKNOWN),
            'unknown': Gender.UNKNOWN,
         }.get(tail, Gender.UNKNOWN)
      return {'m': Gender.MASCULINE, 'f': Gender.FEMININE, 'd': getattr(Gender, 'DIVERSE', Gender.UNKNOWN)}.get(s, Gender.UNKNOWN)

   metrics = evaluate_dataset(
      df,
      languages,
      gold_columns=(gold_gender_column,),
      predicted_prefix=f'{output_prefix}_gender_',
      parse_gold=_parse_gold,
      parse_pred=_parse_pred,
   )
   return metrics, metrics_to_dataframe(metrics)

def run_full_pipeline(
   dataset: DEvalDataset,
   analyzers: Mapping[str, BaseMorphologicalAnalyzer],
   *,
   source_column: str,
   subject_index_column: str,
   subject_gender_column: str,
   output_prefix: Optional[str] = None,
   languages: Optional[List[str]] = None,
   inplace: bool = True,
   **kwargs,
):
   """End-to-end convenience for a single subject annotation set.

   Example (x & y subjects evaluated separately):
      df_x, metrics_x, metrics_df_x = run_full_pipeline(ds, source_column='text', subject_index_column='x_idx', subject_gender_column='x_gender', output_prefix='x')
      df_y, metrics_y, metrics_df_y = run_full_pipeline(ds, source_column='text', subject_index_column='y_idx', subject_gender_column='y_gender', output_prefix='y', languages=['es','fr'])
   """
   processed_df = run_subject_pipeline(
      dataset,
      source_column=source_column,
      subject_index_column=subject_index_column,
      output_prefix=output_prefix,
      languages=languages,
      analyzers=analyzers,
   inplace=inplace,
      **kwargs,
   )
   langs = languages or list(dataset.translation_columns.keys())
   prefix = output_prefix or (subject_index_column[:-4] if subject_index_column.endswith('_idx') else 'subject')
   metrics, metrics_df = evaluate_processed_dataset(processed_df, langs, gold_gender_column=subject_gender_column, output_prefix=prefix)
   return processed_df, metrics, metrics_df

__all__ = [
   'run_subject_pipeline',
   'evaluate_processed_dataset',
   'run_full_pipeline',
]
