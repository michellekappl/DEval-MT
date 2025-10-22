from enum import Enum

class Gender(Enum):
   """Enumeration for grammatical genders.

   Added DIVERSE to represent non-binary / gender-neutral forms (e.g. German
   neopronoun "dey"). Most current morphological analyzers will not surface this value.
   It can be used for annotation / evaluation so users can explicitly label such cases. 
   If an analyzer cannot determine it, it should fall back to UNKNOWN.
   """
   MASCULINE = "Gender.MASCULINE"
   FEMININE = "Gender.FEMININE"
   NEUTER = "Gender.NEUTER"
   DIVERSE = "Gender.DIVERSE"   # non-binary / inclusive forms
   UNKNOWN = "Gender.UNKNOWN"