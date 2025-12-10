from systran_translate import translate_text_systran
from google_translate import translate_text_google
from gpt_translate import translate_text_gpt

def translate_dataset(path_to_dataset, target: str, provider: str):
    """
    Dataset is a .csv file with the last col containing the full sentence
    """
    sentences = []

    with open(path_to_dataset, 'r') as file:
        rows = file.readlines()
        for i, row in enumerate(rows):
            if i == 0:  # first row only contains the table headers
                continue

            sentence = row.rstrip('\n').split(';')[-1]
            sentences.append(sentence)

    translations = []

    file_name = target + "_" + provider + ".txt"
    file_path = f"test_data/translations/{file_name}"
    file = open(file_path, "w", encoding='utf-8')

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
            case 'gpt-4o'|'gpt-4o-mini':
                translated_sentence = translate_text_gpt(sentence,target,provider)
                translations.append(translated_sentence)
                file.write(translated_sentence + "\n")
            case _:
                return "No such Translation Provider. The available Translation Providers are: systran, google and gpt-4o/gpt-4o-mini."

    return translations

dataset_path = "test_data/test_data.csv"

print("systran translation: \n")
es_systran = translate_dataset(dataset_path, "es", "systran")
print(es_systran)

print("google translation: \n")
es_google = translate_dataset(dataset_path, "es", "google")
print(es_google)

# print("chatgpt translation: \n")
es_gpt = translate_dataset(dataset_path, "es", "gpt-4o-mini")
print(es_gpt)