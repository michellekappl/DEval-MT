import os
from google.cloud import translate_v3
from google.cloud import translate, storage
from dotenv import load_dotenv
from typing import List
import tempfile

load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def translate_text_google(text: str, target: str) -> translate_v3.TranslationServiceClient:
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
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{PROJECT_ID}/locations/global"

    mime_type = "text/plain"

    # Translate text from the source to the target language.
    response = client.translate_text(
        contents=[text],
        parent=parent,
        mime_type=mime_type,
        target_language_code=target,
    )

    return response

def write_texts_to_tmp_file(data: dict):
    # for batch translation we have to use a .txt file and give the path
    # batch tanslation with google is not possible via a dictionary
    tmp = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8")
    with tmp as f:
        for t in data:
            # Zeilenumbrüche entfernen, damit jede Zeile ein Text ist
            f.write(t.replace("\n", " ") + "\n")
    return tmp.name

def upload_to_gcs(local_path: str, bucket_name: str, blob_name: str) -> str:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(local_path)
    return f"gs://{bucket_name}/{blob_name}"


def batch_translate_text(
    texts: List[str],
    bucket_name: str,
    project_id: str,
    output_prefix: str = "path/to/save/results/",
    timeout: int = 180,
) -> translate.TranslateTextResponse:
    # 1) Texte in temp-Datei schreiben
    local_input_file = write_texts_to_tmp_file(texts)

    # 2) temp-Datei in GCS hochladen
    blob_name = "path/to/your/file.txt"
    input_uri = upload_to_gcs(local_input_file, bucket_name, blob_name)

    # temp-Datei lokal wieder löschen (optional, aber sauber)
    os.remove(local_input_file)

    # 3) Batch-Übersetzung wie im Google-Beispiel
    client = translate.TranslationServiceClient()
    location = "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    gcs_source = {"input_uri": input_uri}
    input_config = {
        "gcs_source": gcs_source,
        "mime_type": "text/plain",
    }

    gcs_destination = {"output_uri_prefix": f"gs://{bucket_name}/{output_prefix}"}
    output_config = {"gcs_destination": gcs_destination}

    operation = client.batch_translate_text(
        request={
            "parent": parent,
            "source_language_code": "en",
            "target_language_codes": ["ja"],
            "input_configs": [input_config],
            "output_config": output_config,
        }
    )

    response = operation.result(timeout=timeout)
    return response