from dotenv import load_dotenv
import os
from openai import OpenAI
import pandas as pd
import requests
import json

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()
URL = "https://api.openai.com/v1/chat/completions"
headers = {"Authorization": f"Bearer {openai_api_key}", "Content-Type": "application/json"}

languages = {
    "es": "Spanisch",
    "fr": "Französisch",
    "it": "Italienisch",
    "ru": "Russisch",
    "uk": "Ukrainisch",
    "sv": "Schwedisch",
    "no": "Norwegisch",
    "ar": "Arabisch",
    "he": "Hebräisch",
}


def translate_text_gpt(text, target, model_name):
    target_lang = languages.get(target)
    prompt = f"Übersetze nach {target_lang}. Gib nur die Übersetzung aus:\n{text}"

    response = client.responses.create(
        model=model_name,
        input=prompt,
    )
    translated_text = response.output_text
    return translated_text

def translate_dataset_gpt(path, target, model_name):
    source_ds = pd.read_csv(path, header=0, sep=";")
    sentences_list = list(source_ds["text"])
    translations_list = []
    file_name = f"{target}_{model_name}.txt"
    file_path = f"test_data/translations/{file_name}"

    with open(file_path, "w", encoding="utf-8") as f:
        for i, sentence in enumerate(sentences_list):
            sentence = sentence.strip()
            # print(sentence)
            if not isinstance(sentence, str) or sentence.strip() == "":
                translated_sentence = ""
            else:
                translated_sentence = translate_text_gpt(sentence, target, model_name)
                # translated_sentence=translate_text_openrouter(sentence,target,model_name)

            translations_list.append(translated_sentence)
            f.write(str(translated_sentence) + "\n")

    translations_list = pd.DataFrame(translations_list)
    return translations_list
