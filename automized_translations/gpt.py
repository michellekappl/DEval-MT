from dotenv import load_dotenv
import os
from openai import OpenAI
import pandas as pd

load_dotenv()
openai_api_key=os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)

def translate_text(text,target,model_name): 
    #print(f'testing: translating {text} to {target}')
    response = client.responses.create( 
        model=model_name,
        #TODO: find an optimal prompt
        input=('You are a translation engine.'
            f"Translate the following text into {target}: {text}."
            'Output ONLY the translated sentence.'),
    )
    return response.output[0].content[0].text.strip()

def translate_dataset(path,target,model_name):
    source_ds=pd.read_csv(path,header=0,sep=';')
    sentences_list=list(source_ds['text'])
    translations_list=[]
    file_name=f'{target}_{model_name}.txt'
    file_path=f"test_data/translations/{file_name}"
    for sentence in sentences_list:
        if not isinstance(sentence,str) or sentence.strip()=='':
            translations_list.append('')
            continue
        translated_sentence=translate_text(sentence,target,model_name)
        translations_list.append(translated_sentence)
    with open(file_path,'w',encoding='utf-8') as f:
        for tr in translations_list:
            f.write(tr+'\n')
    return translations_list

# text = "Hello, world!"
target_language = "es" # Spanish
models=['gpt-4o']  #TBC
source_path='test_data/test_data.csv'
translation=translate_dataset(source_path,target_language,models[0])
#translation = translate_text(text, target_language,models[0]) 
#print(translation) # ¡Hola mundo!