from list_translator import translate_dataset


# Multiple languages, multiple providers with custom output directory
#!!!!
# TBD ! input correct dataset file path in all functions-> then the file can be run as is
# and the entire dataset will be fully translated (all lang + all prov)

# Beware of langauge codes supported by each provider!
# uppercase codes for Deepl are handled within the code 
"""
| Language       | DeepL         | Microsoft | Google | ChatGPT / OpenAI | SYSTRAN |
| -------------- | -----         | --------- | ------ | ---------------- | ------- |
| Russian        | RU            | ru        | ru     | ru               | ru      |
| Ukrainian      | UK            | uk        | uk     | uk               | uk      |
| Spanish        | ES            | es        | es     | es               | es      |
| French         | FR            | fr        | fr     | fr               | fr      |
| Italian        | IT            | it        | it     | it               | it      |
| Portuguese     | PT-PT or PT-BR| pt        | pt     | pt               | pt      |
| Romanian       | RO            | ro        | ro     | ro               | ro      |
| Norwegian      | NB      !!    | nb    !!  | no     | no               | no      |
| Swedish        | SV            | sv        | sv     | sv               | sv      |
| Hebrew         | HE            | he        | iw  !! | he               | he      |
| Polish         | PL            | pl        | pl     | pl               | pl      |
| Slovenian      | SL            | sl        | sl     | sl               | sl      |
| Arabic         | AR            | ar        | ar     | ar               | ar      |
"""


#translation for unified languages
translate_dataset(
    "../test_data/test_data_mini.csv", # set dataset path
    ["ru", "uk", "es", "fr", "it", "pt", "ro", "sv", "pl", "sl", "ar"], 
    ["deepl", "microsoft", "google", "gpt-4o", "gpt-4o-mini", "systran"],
    overwrite_translation=False
)


#translation for alternate language codes 

translate_dataset(
    "../test_data/test_data_mini.csv", # set dataset path
    ["nb"], 
    ["deepl", "microsoft"],
    overwrite_translation=False
)


translate_dataset(
    "../test_data/test_data_mini.csv", # set dataset path
    ["no"], 
    ["google", "gpt-4o", "gpt-4o-mini", "systran"],
    overwrite_translation=True
)

translate_dataset(
    "../test_data/test_data_mini.csv", # set dataset path
    ["iw"], 
    ["google"],
    overwrite_translation=False
)

translate_dataset(
    "../test_data/test_data_mini.csv", # set dataset path
    ["he"], 
    ["deepl", "microsoft", "gpt-4o", "gpt-4o-mini", "systran"],
    overwrite_translation=False
)

translate_dataset(
    "../test_data/test_data_mini.csv", # set dataset path
    ["pt-pt"], 
    ["deepl"],
    overwrite_translation=True
)