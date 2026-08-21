import os
import requests
from dotenv import load_dotenv

load_dotenv()

MY_ENV_VAR = os.getenv('MY_ENV_VAR')

SYSTRAN_BASE_URL = os.getenv("SYSTRAN_API_URL")
SYSTRAN_API_KEY = os.getenv("SYSTRAN_API_KEY")  

def translate_text_systran(text: str, target: str) -> str:
    """
    Übersetzt einen String mit der Systran Translation API.
    source/target = ISO-639-1 Codes, z.B. 'en', 'de', 'pl'.
    source='auto' für automatische Spracherkennung.
    """
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

    response.raise_for_status()
    data = response.json()

    outputs = data.get("outputs", [])
    if not outputs:
        raise RuntimeError(f"Keine Outputs in Antwort: {data}")

    return outputs[0].get("output", "")