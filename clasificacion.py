
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
    inicio = time.time()
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
            tiempo = time.time() - inicio
            print(f'{index}, {round(tiempo, 2)} s')
        index_anterior = copy_of_index
    return tweets

def clasificacion(tweets, fichero):
    file_tweets = pd.read_excel(r'COV_train.xlsx', index_col=None, engine='openpyxl', sheet_name='Sheet 1', usecols="A")
    file_modeloP = "modelo_lenguaje_P.txt"
    file_modeloN = "modelo_lenguaje_N.txt"
    index = 0
    P_clase_P = 18046 / 33443
    P_clase_N = 15397 / 33443
    for tweet in tweets:
        primeros_10_caracteres = file_tweets[0][0:9] # error aquí
        PP = probability(tweet, file_modeloP) * P_clase_P
        PN = probability(tweet, file_modeloN) * P_clase_N
        if PP > PN:
            tipo = PP
        else:
            tipo = PN
        fichero.write(f'{primeros_10_caracteres},{PP},{PN},{tipo}')


def probability(tweet, nombre_fichero):
    fichero = open(nombre_fichero, "r")
    probabilidad = 1
    PUNK = -1
    for word in tweet:
        for line in fichero:
            copy_of_line = line.split(' ')
            palabra = copy_of_line[1]
            if (palabra == word):
                probabilidad *= copy_of_line[5]
                continue
            if (word < palabra):
                probabilidad *= PUNK
                continue
    fichero.close()
    return probabilidad
            


def main():
    inicio = time.time()
    file_clasificacion = open("clasificacion_alu0100829150.txt", "w")
    print(f'Preprocesando tweets...')
    # Carga de datos
    tweets = carga_de_tweets()
    final_carga = time.time()
    print(f'{len(tweets)} tweets preprocesados. T: {round(final_carga - inicio) / 60} s')
    print(f'Clasificando tweets...')
    clasificacion(tweets, file_clasificacion)
    final = round(time.time() - final_carga, 2) / 60
    print(f'FIN. Tiempo total: {final} s')

main()