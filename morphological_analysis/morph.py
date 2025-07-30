import spacy
from gender import Gender

# Load the English model (you can change it to another language model as needed)
nlp = spacy.load("en_core_web_sm")

# Your sentence
sentence = "She was running quickly to catch the bus."

# Process the sentence
doc = nlp(sentence)

# Print morphological analysis
print(f"{'Token':<15}{'POS':<10}{'Morphological Features'}")
print("-" * 50)
for token in doc:
   print(f"{token.text:<15}{token.pos_:<10}{token.morph}")

def get_phrase_gender(phrase: str) -> Gender:
   """
   Extract the gender of the subject pronoun in a phrase.
   
   Returns:
      Gender: The grammatical gender (MASCULINE, FEMININE, NEUTER, or UNKNOWN)
   """
   doc = nlp(phrase)
   for token in doc:
      if token.dep_ == "nsubj" and token.pos_ == "PRON":
         gender_value = token.morph.get("Gender", [])
         if gender_value:
            gender_str = gender_value[0].lower()
            # Map spaCy gender values to our enum
            if gender_str in ["masc", "masculine"]:
               return Gender.MASCULINE
            elif gender_str in ["fem", "feminine"]:
               return Gender.FEMININE
            elif gender_str in ["neut", "neuter"]:
               return Gender.NEUTER
   return Gender.UNKNOWN