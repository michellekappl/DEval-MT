from simalign import SentenceAligner
from Dataset import WordAlignment

# making an instance of our model.
# You can specify the embedding model and all alignment settings in the constructor.
myaligner = SentenceAligner(model="google-bert/bert-base-multilingual-cased", token_type="bpe", matching_methods="mai")

src = "Der Geschäftsführer mochte die Friseurin weil ihm die angebotenen Frisuren gefielen"
tgt = "The manager liked the hairdresser because he liked the hairstyles offered"

src_sentence = src.split()
trg_sentence = tgt.split()

# The output is a dictionary with different matching methods.
# Each method has a list of pairs indicating the indexes of aligned words (The alignments are zero-indexed).
alignments = myaligner.get_word_aligns(src_sentence, trg_sentence)

WordAlignment(src, tgt, alignments["inter"])

for matching_method in alignments:
   print(matching_method)
   for alignment in alignments[matching_method]:
      print(src_sentence[alignment[0]], "->", trg_sentence[alignment[1]])
   print()

for matching_method in alignments:
   print(matching_method, ":", alignments[matching_method])

# Expected output:
# mwmf (Match): [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
# inter (ArgMax): [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
# itermax (IterMax): [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]

import simalign

source_sentence = "Sir Nils Olav III. was knighted by the norwegian king ."
target_sentence = "Nils Olav der Dritte wurde vom norwegischen König zum Ritter geschlagen ."

model = simalign.SentenceAligner()
result = model.get_word_aligns(source_sentence, target_sentence)
print(result)