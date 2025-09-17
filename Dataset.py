import pandas as pd
import numpy as np
from typing import Callable, Optional, List

class DEvalConfig:
   ALIGNMENT_MODEL: str = "google-bert/bert-base-multilingual-cased"
   TOKEN_TYPE: str = "bpe"
   # Only a single alignment matching method is supported now for performance & simplicity.
   MATCHING_METHOD: str = "itermax"

class DEvalDataset:
   def __init__(self, df: pd.DataFrame, text_column: str):
      self.translation_columns: dict[str, str] = {}
      self.text_column = text_column
      self.path = None
      self.df = df.copy()
      self.aligned = False
      self.morph_analyzed = False
      self.prediction_columns: dict[str, str] = {}

   def clone(self) -> 'DEvalDataset':
      """Return a deep-ish copy of this dataset.

      Copies the underlying DataFrame and translation column mapping so that
      downstream pipeline steps can add columns without mutating the original
      object passed by the caller.
      """
      new = DEvalDataset(self.df.copy(deep=True), self.text_column)
      new.translation_columns = self.translation_columns.copy()
      new.path = self.path
      return new

   @classmethod
   def from_csv(cls, 
               path: str, 
               text_column: str, 
               translation_columns: dict[str, str], 
               prediction_columns: Optional[dict[str, str]] = None,
               sep: str = ","):
      df = pd.read_csv(path, sep=sep)
      instance = cls(df, text_column)
      instance.translation_columns = translation_columns
      if prediction_columns is not None:
         instance.prediction_columns = prediction_columns
      instance.path = path
      return instance

   # Access the data directly via pandas-like indexing instead of having to use the df object everytime
   def __getitem__(self, index: str) -> pd.Series:
      if not isinstance(index, str):
         raise TypeError("Index must be a string.")

      return self.df[index] if index in self.df.columns else pd.Series(dtype=float)

   def extract_subject_phrases(self, subject_pos_column: str, article_offset: int = -1):
      """
      Extracts subjects from the text column based on the position specified in the given column and offset.
      Returns a pandas Series of extracted subjects.
      """
      subjects = self.df.apply(
         lambda row: row[self.text_column].split()[row[subject_pos_column] + article_offset:row[subject_pos_column]+1], axis=1
      )
      return subjects
   
   def extract_subject_phrase_indices(self, subject_pos_column: str, article_offset: int = -1):
      """
      Extracts subject phrase indices from the position specified in the given column and offset.
      Returns a pandas Series of lists of indices.
      """
      subject_indices = self.df.apply(
         lambda row: list(range(row[subject_pos_column] + article_offset, row[subject_pos_column]+1)), axis=1
      )
      return subject_indices

   def translate(self, language: str, translation_func: Callable[[str], str], new_column_name = None) -> None:
      """
      Translates the text column (specified by ``self.text_column``) into the specified language using the provided translation function.
      If `new_column_name` is not provided, it defaults to 'translation_<language>'.
      """
      if new_column_name is None:
         new_column_name = f"translation_{language}"

      if new_column_name in self.df.columns:
         raise ValueError(f"Column '{new_column_name}' already exists in the DataFrame.")

      self.df[new_column_name] = self.df[self.text_column].apply(translation_func)
      self.translation_columns[language] = new_column_name

   def add_translations(self, language: str, translations: pd.Series | List[str], new_column_name: Optional[str] = None) -> None:
      """
      Adds externally created translations to the DataFrame under a specified column name.
      If `new_column_name` is not provided, it defaults to 'translation_<language>'.
      """
      column_name = new_column_name or f"translation_{language}"
      self.df[column_name] = translations
      self.translation_columns[language] = column_name