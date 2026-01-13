from list_translator import translate_dataset

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


# Single language, single provider
# translate_dataset("../test_data/test_data_mini.csv", "fr", "deepl")

# Multiple languages, single provider
# translate_dataset("../test_data/test_data_mini.csv", ["pt", "fr"], "microsoft")

# Single language, multiple providers
# translate_dataset("../test_data/test_data_mini.csv", "it", ["deepl", "microsoft"])

# Multiple languages, multiple providers with custom output directory
translate_dataset(
    "../DEval_dataset.csv",
    ["es"],
    "google",
    overwrite_translation=True,
    output_dir="../translations",
)
