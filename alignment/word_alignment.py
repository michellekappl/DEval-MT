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
   
   def serialize(self) -> str:
      """
      Serialize the alignment to a string format.
      Each alignment pair is represented as "source_index-target_index".
      Pairs are separated by spaces.
      """
      return " ".join(f"{src}-{trg}" for src, trg in self.alignments)

   @classmethod
   def from_serialized(cls, source: str, target: str, serialized: str) -> 'WordAlignment':
      """
      Create a WordAlignment object from a serialized string.
      Args:
         source (str): The source sentence.
         target (str): The target sentence.
         serialized (str): The serialized alignment string.
      Returns:
         WordAlignment: The constructed WordAlignment object.
      """
      alignments = []
      if serialized.strip():
         for pair in serialized.split():
            src_idx, trg_idx = map(int, pair.split('-'))
            alignments.append((src_idx, trg_idx))
      return cls(source, target, alignments)

   def __repr__(self):
      return f"WordAlignment (\"{self.source}\" \n \"{self.target}\" \n\n Alignments: {self.alignments})"