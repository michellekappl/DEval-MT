import os
from google.cloud import translate_v2
from google.cloud import translate, storage
from dotenv import load_dotenv
from typing import List
import tempfile

load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def translate_text_google(text: str, target: str):
    """Translate Text from a Source language to a Target language.
    Args:
        text: The content to translate.
        source_language_code: The code of the source language.
        target_language_code: The code of the target language.
            For example: "fr" for French, "es" for Spanish, etc.
            Find available languages and codes here:
            https://cloud.google.com/translate/docs/languages#neural_machine_translation_model
    """

    # Initialize Translation client.
    client = translate_v2.Client()
    parent = f"projects/{PROJECT_ID}/locations/global"

    results = client.translate(values=text, target_language=target, source_language="de")

    return results
