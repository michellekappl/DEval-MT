from typing import Tuple, List
from alignment import AlignmentProcessor
import pandas as pd
import spacy

# Load spaCy models
nlp_es = spacy.load("es_core_news_sm")
nlp_fr = spacy.load("fr_core_news_sm")

data = pd.read_csv("data_huge.csv", sep=";", na_values=["none"])


lang = "es"  # Default language, can be changed to "fr" for French
phrase = "al diseñador de moda moderna"  # Example phrase, can be changed as needed

def get_phrase_gender(lang, phrase):
   if lang == "es":
      doc = nlp_es(phrase)
   elif lang == "fr":
      doc = nlp_fr(phrase)
   else:
      raise ValueError("Unsupported language")

   # Collect all gender information from tokens
   genders = []
   
   for token in doc:
      gender = token.morph.get("Gender", [])
      if gender:
         genders.append(gender[0])
   
   # Return the most frequent gender, or "Unknown" if no gender found
   if not genders:
      return "Unknown"
   
   # Count occurrences of each gender manually
   gender_counts = {}
   for gender in genders:
      gender_counts[gender] = gender_counts.get(gender, 0) + 1
   
   # Return the most common gender
   return max(gender_counts.keys(), key=lambda x: gender_counts[x])

def get_gender(lang: str, phrase: str) -> str:
   if lang == "es":
      doc = nlp_es(phrase)
   elif lang == "fr":
      doc = nlp_fr(phrase)
   else:
      raise ValueError("Unsupported language")
   
   genders = [
      token.morph.get("Gender", ["unknown"])[0]
      for token in doc
   ]

   # if all genders are the same, return it, otherwise return "mixed"
   if len(set(genders)) == 1:
      return genders[0]
   else:
      print(f"mixed ({phrase}): {genders}")
      return "mixed"

df = pd.read_csv("data_huge.csv", sep=";", na_values=["none"])

es_originals = df["text"].tolist()
fr_originals = df["text"].tolist()

es_translations = pd.read_csv("translations/es.txt", sep="\t", header=None)[0].tolist()
fr_translations = pd.read_csv("translations/fr.txt", sep="\t", header=None)[0].tolist()

def get_subject(sentence:str, idx: int, modified: bool):
   if not modified:
      subject = sentence.split()[idx - 1] + " " + sentence.split()[idx]
   else:
      subject = sentence.split()[idx - 2] + " " + sentence.split()[idx]

   return subject.strip()

if __name__ == "__main__":
   processor = AlignmentProcessor("bert", "bpe", "itermax")
   results = processor.process_multiple(
      sources=[es_originals, fr_originals],
      targets=[es_translations, fr_translations]
   )

   es_alignments = results[0]
   fr_alignments = results[1]

   for idx, (row_idx, sentence) in enumerate(df.iterrows()):
      words = sentence["text"].split()
      modified = sentence["modified"]
      x_ids = [sentence["x_idx"] - (2 if modified == "x" else 1), sentence["x_idx"]]
      y_ids = [sentence["y_idx"] - (2 if modified == "y" else 1), sentence["y_idx"]]

      # Get the aligned words for this sentence
      es_aligned = es_alignments[idx]
      fr_aligned = fr_alignments[idx]

      es_x_ids = [word for i in x_ids for word in es_aligned.get_counterpart(i)]
      es_y_ids = [word for i in y_ids for word in es_aligned.get_counterpart(i)]
      fr_x_ids = [word for i in x_ids for word in fr_aligned.get_counterpart(i)]
      fr_y_ids = [word for i in y_ids for word in fr_aligned.get_counterpart(i)]

      original_gender_x = "Masc" if sentence["x_gender"] == "m" else "Fem"
      original_gender_y = "Masc" if sentence["y_gender"] == "m" else "Fem"
      es_gender_x = get_phrase_gender("es", " ".join([es_aligned.target.split()[i] for i in es_x_ids]))
      es_gender_y = get_phrase_gender("es", " ".join([es_aligned.target.split()[i] for i in es_y_ids]))
      fr_gender_x = get_phrase_gender("fr", " ".join([fr_aligned.target.split()[i] for i in fr_x_ids]))
      fr_gender_y = get_phrase_gender("fr", " ".join([fr_aligned.target.split()[i] for i in fr_y_ids]))

      if es_gender_x != original_gender_x or es_gender_y != original_gender_y or fr_gender_x != original_gender_x or fr_gender_y != original_gender_y:
         if es_gender_x != original_gender_x:
            print(f"Row {row_idx} has gender mismatch in Spanish (x): {original_gender_x} → {es_gender_x}")
         if es_gender_y != original_gender_y:
            print(f"Row {row_idx} has gender mismatch in Spanish (y): {original_gender_y} → {es_gender_y}")
         if fr_gender_x != original_gender_x:
            print(f"Row {row_idx} has gender mismatch in French (x): {original_gender_x} → {fr_gender_x}")
         if fr_gender_y != original_gender_y:
            print(f"Row {row_idx} has gender mismatch in French (y): {original_gender_y} → {fr_gender_y}")
      else:
         print(f"Row {row_idx} is consistent.")

      print()


   # x_subjects = df.apply(lambda row: get_subject(row["text"], row["x_idx"], row["modified"] == "x"), axis=1).tolist()
   # y_subjects = df.apply(lambda row: get_subject(row["text"], row["y_idx"], row["modified"] == "y"), axis=1).tolist()


get_phrase_gender("es", "el diseñador de moda")  # Example usage