from list_translator import translate_dataset

# Single language, single provider
translate_dataset("../test_data/test_data_mini.csv", "fr", "deepl")

# Multiple languages, single provider
translate_dataset("../test_data/test_data_mini.csv", ["pt", "fr"], "microsoft")

# Single language, multiple providers
translate_dataset("../test_data/test_data_mini.csv", "it", ["deepl", "microsoft"])

# Multiple languages, multiple providers with custom output directory
translate_dataset(
    "../test_data/test_data_mini.csv", 
    ["es", "fr"], 
    ["deepl", "microsoft"],
    overwrite_translation=True
)