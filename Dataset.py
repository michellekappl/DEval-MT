import pandas as pd
import numpy as np
from typing import Callable, Optional, List, Tuple
from simaligntest import SentenceAligner
from tqdm import tqdm

class DEvalConfig:
   ALIGNMENT_MODEL: str = "google-bert/bert-base-multilingual-cased"
   TOKEN_TYPE: str = "bpe"
   MATCHING_METHODS: str = "mai"  # MWMF, Inter, IterMax

class WordAlignment:
   def __init__(self, source: str, target: str, alignments: List[Tuple[int, int]]):
      self.source = source
      self.target = target
      self.alignments = alignments

   def __repr__(self):
      return f"WordAlignment (\"{self.source}\" -> \"{self.target}\", Alignments: {self.alignments}"

class DEvalDataset:
   def __init__(self, path: str):
      self.path = path
      self.df = pd.read_csv(path, on_bad_lines='skip')
      self.translation_columns = {}
      self.word_aligner = SentenceAligner(model=DEvalConfig.ALIGNMENT_MODEL, token_type=DEvalConfig.TOKEN_TYPE, matching_methods=DEvalConfig.MATCHING_METHODS)

   # Access the data directly via pandas-like indexing instead of having to use the df object everytime
   def __getitem__(self, index: str) -> pd.Series:
      if not isinstance(index, str):
         raise TypeError("Index must be a string.")

      return self.df[index] if index in self.df.columns else pd.Series(dtype=float)
   
   def translate(self, language: str, translation_func: Callable[[str], str], new_column_name = None) -> None:
      """
      Translates the 'Sätze' column into the specified language using the provided translation function.
      If `new_column_name` is not provided, it defaults to 'translation_<language>'.
      """
      if new_column_name is None:
         new_column_name = f"translation_{language}"

      if new_column_name in self.df.columns:
         raise ValueError(f"Column '{new_column_name}' already exists in the DataFrame.")
      
      self.df[new_column_name] = self.df["Sätze"].apply(translation_func)
      self.translation_columns[language] = new_column_name

   def add_translations(self, language: str, translations: pd.Series | List[str], new_column_name: Optional[str] = None) -> None:
      """
      Adds externally created translations to the DataFrame under a specified column name.
      If `new_column_name` is not provided, it defaults to 'translation_<language>'.
      """
      column_name = new_column_name or f"translation_{language}"
      self.df[column_name] = translations
      self.translation_columns[language] = column_name

   def calculate_word_alignments(self, language: str, pbar: tqdm, source_column: str = "Sätze") -> None:
      target_column = self.translation_columns.get(language)
      if not target_column:
         raise ValueError(f"No translations found for language: {language}")

      if source_column not in self.df.columns or target_column not in self.df.columns:
         raise ValueError(f"Source ({source_column}) or target column ({target_column}) does not exist in the DataFrame.")

      alignments = []
      for _, row in tqdm(self.df.iterrows()):
         src_sentence = row[source_column].split()
         trg_sentence = row[target_column].split()
         alignment_result = self.word_aligner.get_word_aligns(src_sentence, trg_sentence)
         alignments.append(alignment_result["inter"])

      self.df["word_alignments"] = alignments
