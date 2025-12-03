from dotenv import load_dotenv
import os
from openai import OpenAI
import pandas as pd
import requests
import json

load_dotenv()
openai_api_key=os.getenv('OPENAI_API_KEY')
openrouter_api_key=os.getenv('OPENROUTER_API_KEY')

client = OpenAI(api_key=openai_api_key)
URL = "https://api.openai.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {openai_api_key}",
    "Content-Type": "application/json"
}
languages = ["es", "it", "fr", "ru", "uk", "ar", "he"]
models=['gpt-4o','gpt-4o-mini']  #TBC

def translate_text(text,target,model_name): 
    # #print(f'testing: translating {text} to {target}')
    # response = client.responses.create( 
    #     model=model_name,
    #     input=('You are a translation engine.'
    #         f"Translate the following text into {target}: {text}."
    #         'Output ONLY the translated sentence.'),
    # )
    # return response.output[0].content[0].text.strip()

    data = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": f"You are a Machine Translation Tool and shall not output any other text than the translated text. Translate the text to {target}."},
            {"role": "user", "content": text}
        ],
        "temperature": 0.3
    }
    response = requests.post(URL, headers=headers, json=data)
    response_json = response.json()
    translated_text = response_json["choices"][0]["message"]["content"]
    return translated_text

# not working
# def translate_text_openrouter(text,target,model_name):
#     response = requests.post(
#         url="https://openrouter.ai/api/v1/chat/completions",
#         headers={
#             "Authorization": f"Bearer {openrouter_api_key}",
#             "Content-Type": "application/json",
#             # "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
#             # "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
#         },
#         data=json.dumps({
#             "model": "openai/gpt-4o-mini", # Optional
#             "messages": [
#                 #{"role": "system", "content": f"You are a Machine Translation Tool and shall not output any other text than the translated text. Translate the text to {target}."},
#                 {"role": "user","content": f'You are a Machine Translation Tool and shall not output any other text than the translated text. Translate the text to {target}: {text}'}
#             ]
#         })
#     )
#     data = response.json()
#     print(data['choices'][0]['message']['content'])

def translate_dataset(path,target,model_name):
    source_ds=pd.read_csv(path,header=0,sep=';')
    sentences_list=list(source_ds['text'])
    translations_list=[]
    file_name=f'{target}_{model_name}.txt'
    file_path=f"test_data/translations/{file_name}"
    for sentence in sentences_list:
        sentence=sentence.strip()
        #print(sentence)
        if not isinstance(sentence,str) or sentence.strip()=='':
            translations_list.append('')
            continue
        translated_sentence=translate_text(sentence,target,model_name)
        # translated_sentence=translate_text_openrouter(sentence,target,model_name)
        # print(translated_sentence)
        translations_list.append(translated_sentence)
    with open(file_path,'w',encoding='utf-8') as f:
        for tr in translations_list:
            f.write(str(tr)+'\n')
    translations_list=pd.DataFrame(translations_list)
    return translations_list

# Following for test
#target_language = languages[0] # Spanish
source_path='test_data/test_data.csv'
translation=translate_dataset(source_path,languages[0],models[0])
# test=translate_text_openrouter('Der Chirurg versichert der Försterin, dass ihre Vorschläge bereits berücksichtigt wurden.',
#                                               'es',
#                                               models[0])
#print(test)