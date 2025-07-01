import pandas as pd
import numpy as np
from typing import Callable, Optional, List, Tuple

class DEvalConfig:
   ALIGNMENT_MODEL: str = "google-bert/bert-base-multilingual-cased"
   TOKEN_TYPE: str = "bpe"
   MATCHING_METHODS: str = "mai"  # MWMF, Inter, IterMax

class DEvalPipeline:
   def __init__(self, dataset_path: str, config: DEvalConfig = DEvalConfig()):
      self.dataset_path = dataset_path
      self.config = config

   def load_dataset(self):
      """
      Loads the dataset from the specified path.
      """
      ds = DEvalDataset(self.dataset_path)
      self.dataset = ds
      return ds

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
      self.df = pd.read_csv(path)
      self.__translation_columns = {}

   # Access the data directly via pandas-like indexing instead of having to use the df object everytime
   def __getitem__(self, index: str) -> pd.Series:
      if not isinstance(index, str):
         raise TypeError("Index must be a string.")

      return self.df[index] if index in self.df.columns else pd.Series(dtype=float)
   
   def translate(self, language: str, translation_func: Callable[[str], str], new_column_name = None) -> None:
      """
      Translates the 'Sätze' column into the specified language using the provided translation function.
      If new_column_name is not provided, it defaults to 'translation_<language>'.
      """
      if new_column_name is None:
         new_column_name = f"translation_{language}"

      if new_column_name in self.df.columns:
         raise ValueError(f"Column '{new_column_name}' already exists in the DataFrame.")
      
      self.df[new_column_name] = self.df["Sätze"].apply(translation_func)
      self.__translation_columns[language] = new_column_name

   def add_translations(self, language: str, translations: pd.Series | List[str], new_column_name: Optional[str] = None) -> None:
      column_name = new_column_name or f"translation_{language}"
      self.df[column_name] = translations
      self.__translation_columns[language] = column_name

class LoadedDEvalPipeline(DEvalPipeline):
   def __init__(self, dataset: DEvalDataset, config: DEvalConfig = DEvalConfig()):
      super().__init__(dataset.path, config)
      self.dataset = dataset

   def translate(self, language: str, translation_func: Callable[[str], str], new_column_name: Optional[str] = None):
      """
      Translates the 'Sätze' column into the specified language using the provided translation function.
      """
      self.dataset.translate(language, translation_func, new_column_name)

class TranslatedDEvalPipeline(LoadedDEvalPipeline):
   def __init__(self, dataset: DEvalDataset, config: DEvalConfig = DEvalConfig()):
      super().__init__(dataset, config)

   def add_translations(self, language: str, translations: pd.Series | List[str], new_column_name: Optional[str] = None):
      """
      Adds translations to the dataset.
      """
      self.dataset.add_translations(language, translations, new_column_name)