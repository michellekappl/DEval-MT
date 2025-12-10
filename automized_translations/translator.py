from systran_translate import translate_text_systran
from google_translate import translate_text_google
import csv

def translate_dataset(path_to_dataset, target: str, provider: str):
    """
    Dataset is a .csv file with a column header "text" containing the sentences to translate
    """
    sentences = []

    with open(path_to_dataset, 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            sentence = row['text']
            sentences.append(sentence)

    translations = []

    file_name = target + "_" + provider + ".txt"
    file_path = f"../test_data/translations/{file_name}"
    file = open(file_path, "w")

    for sentence in sentences:
        match provider:
            case "systran":
                translated_sentence = translate_text_systran(sentence, target)
                translations.append(translated_sentence)
                file.write(translated_sentence + "\n")
            case "google":
                translated_sentence = translate_text_google(sentence, target).translations[0].translated_text
                translations.append(translated_sentence)
                file.write(translated_sentence + "\n")
            case _:
                return "No such Translation Provider. The available Translation Providers are: systran, google, deepl and chatgpt"

    return translations

dataset_path = "../test_data/test_data_mini.csv"

print("systran translation: \n")
es_systran = translate_dataset(dataset_path, "es", "systran")
print(es_systran)

print("google translation: \n")
es_google = translate_dataset(dataset_path, "es", "google")
print(es_google)