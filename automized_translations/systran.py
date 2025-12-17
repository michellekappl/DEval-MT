import os
import requests
from dotenv import load_dotenv

load_dotenv()

MY_ENV_VAR = os.getenv('MY_ENV_VAR')

SYSTRAN_BASE_URL = os.getenv("SYSTRAN_API_URL")
SYSTRAN_API_KEY = os.getenv("SYSTRAN_API_KEY")  

def translate_text(text: str, target: str) -> str:
    """
    Übersetzt einen String mit der Systran Translation API.
    source/target = ISO-639-1 Codes, z.B. 'en', 'de', 'pl'.
    source='auto' für automatische Spracherkennung.
    """
    # print("Input data: ", text, source, target)
    # print("systran url: ", SYSTRAN_BASE_URL)

    url = f"{SYSTRAN_BASE_URL}/translation/text/translate"

    headers = {
        "Authorization": f"Key {SYSTRAN_API_KEY}",
    }

    params = {
        "input": text,
        "source": "auto",      
        "target": target,      # z.B. "en"
        "format": "text",      
        "withInfo": "false",
        "withSource": "false",
    }

    response = requests.post(url, headers=headers, params=params)
    # print("response: ", response)

    response.raise_for_status()
    data = response.json()
    # print("response data: ", data)

    # Laut Doku steckt die Ausgabe im Feld outputs[0]["output"] :contentReference[oaicite:4]{index=4}
    outputs = data.get("outputs", [])
    if not outputs:
        raise RuntimeError(f"Keine Outputs in Antwort: {data}")

    # print("output: ", outputs[0].get("output", ""))
    return outputs[0].get("output", "")

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
    file_path = f"../test_data/translations/{file_name}"
    file = open(file_path, "w")

    for sentence in sentences:
        if provider == "systran":
            translated_sentence = translate_text(sentence, target)
            translations.append(translated_sentence)
            file.write(translated_sentence + "\n")

    return translations

    
#de = translate_text("This is a test sentence.", source="en", target="de")
#print(de)
dataset_path = "../test_data/test_data_mini.csv"

es = translate_dataset(dataset_path, "es", "systran")
print(es)