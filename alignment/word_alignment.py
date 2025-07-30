from typing import List, Tuple

class WordAlignment:
   def __init__(self, source: str, target: str, alignments: List[Tuple[int, int]]):
      self.source = source
      self.target = target
      self.alignments = alignments

   def get_counterpart(self, source_index: int) -> List[int]:
      """
      Get the target index or indices corresponding to a source index.
      If the source index is not aligned, return -1.
      """
      ret = []
      for src_idx, trg_idx in self.alignments:
         if src_idx == source_index:
            ret.append(trg_idx)
      return ret

   def get_source_counterpart(self, target_index: int) -> List[int]:
      """
      Get the source index or indices corresponding to a target index.
      If the target index is not aligned, return -1.
      """
      ret = []
      for src_idx, trg_idx in self.alignments:
         if trg_idx == target_index:
            ret.append(src_idx)
      return ret

   def __repr__(self):
      return f"WordAlignment (\"{self.source}\" \n \"{self.target}\" \n\n Alignments: {self.alignments})"