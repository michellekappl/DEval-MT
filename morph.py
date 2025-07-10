#python -m spacy download fr_core_news_sm
#python -m spacy download it_core_news_sm
#python -m spacy download nb_core_news_sm
#python -m spacy download pl_core_news_sm
#python -m spacy download pt_core_news_sm
#python -m spacy download ro_core_news_sm
#python -m spacy download ru_core_news_sm
#python -m spacy download sl_core_news_sm
#python -m spacy download es_core_news_sm
#python -m spacy download sv_core_news_sm
#python -m spacy download uk_core_news_sm

import spacy


def morph_func(text, identifier):
    if identifier== "es": #Spanish
        nlp = spacy.load("es_core_news_sm")

    elif identifier== "sv": #Swedish
        nlp = spacy.load("sv_core_news_sm")

    elif identifier== "fr": #French
        nlp = spacy.load("fr_core_news_sm")

    elif identifier== "it": #Italian
        nlp = spacy.load("it_core_news_sm")

    elif identifier== "ru": #Russian
        nlp = spacy.load("ru_core_news_sm")

    elif identifier== "pt": #Portuguese
        nlp = spacy.load("pt_core_news_sm")

    elif identifier== "pl": #Polish
        nlp = spacy.load("pl_core_news_sm")

    elif identifier== "uk": #Ukrainian
        nlp = spacy.load("uk_core_news_sm")

    elif identifier== "ro": #Romanian
        nlp = spacy.load("ro_core_news_sm")

    elif identifier== "nb": #Norwegian
        nlp = spacy.load("nb_core_news_sm")

    elif identifier== "sl": #Slovenian
        nlp = spacy.load("sl_core_news_sm")
    
    elif identifier== "de": #German
        nkp= spacy.load("de_core_news_sm")
    
    doc= nlp(text)

    result= ""

    for token in doc:
        if(f"{token.morph.get('Gender')}"!= "[]"):
            gender= f"{token.morph.get('Gender')}"[2:-2]
            result+= f"{token.text} → {gender}\n"
    
    return result


text= "La niña come una manzana."
identifier= "es"

morph= morph_func(text, identifier)

print(morph)


