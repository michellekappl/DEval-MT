from dotenv import load_dotenv
import os
from openai import OpenAI
import pandas as pd

load_dotenv()
openai_api_key=os.getenv('OPENAI_API_KEY')
client = OpenAI()

def translate_text(text,target,model_name): 
    response = client.responses.create( 
        model=model_name,
        input=f"Translate the following text into {target}: {text}\n",
    )
    return response.output_text

#TODO: to be tested
def translate_dataset(path,target,model_name):
    source_ds=pd.read_csv(path,header=0,sep=';')
    sentences_list=list(source_ds['text'])
    translations_list=[]
    file_name=f'{target}_{model_name}.txt'
    file_path=f"../test_data/translations/{file_name}"
    for sentence in sentences_list:
        translated_sentence=translate_text(sentence,target,model_name)
        translations_list.append(translated_sentence)
    with open(file_path,'w') as f:
        f.write(translations_list)
    return translations_list

# test
text = "Hello, world!" 
target_language = "es" # Spanish
models=['gpt-4o']  #TBC
translation = translate_text(text, target_language,models[0]) 
print(translation) # ¡Hola mundo!