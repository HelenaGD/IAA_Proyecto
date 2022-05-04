
import pandas as pd
import time
import re
import nltk
import string
from nltk.corpus import stopwords
from modelo_lenguaje import limpiar
from modelo_lenguaje import func_lemantizacion

def tokenization(tweet):
    stop = set(stopwords.words('english') + list(string.punctuation))
    the_list_of_tokens = []
    # Tokenice with nltk
    doc = [i for i in nltk.word_tokenize(tweet.lower()) if (i not in stop and not i.isdigit())]
    for token in doc:
        token = re.sub(r'[0-9]', '', token)
        the_list_of_tokens.append(token)
    return the_list_of_tokens

def carga_de_tweets():
    file_tweets = pd.read_excel(r'COV_train.xlsx', index_col=None, engine='openpyxl', sheet_name='Sheet 1', usecols="A")
    tweets  = []
    index_anterior = -1
    for index, data in file_tweets.iterrows():
        copy_of_index = index
        while(copy_of_index >= 10):
            copy_of_index = copy_of_index // 10
        tweet_limpio = limpiar(data[0])
        tweet_tokenizado = tokenization(tweet_limpio)
        tweet_lemantizado = func_lemantizacion(tweet_tokenizado)
        tweets.append(tweet_lemantizado)
        if (copy_of_index != index_anterior):
            print(f'{index}')
            print(f'{tweet_lemantizado}')
        index_anterior = copy_of_index
    return tweets

def clasificacion():
    inicio = time.time()
    print(f'Preprocesando tweets...')
    # Carga de datos
    tweets = carga_de_tweets()
    final_carga = time.time()
    print(f'{len(tweets)} tweets preprocesados. T: {round(final_carga - inicio)} s')
    print(f'Clasificando tweets...')

clasificacion()