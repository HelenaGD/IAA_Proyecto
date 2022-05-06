
import pandas as pd
import time
import re
import nltk
import string
from nltk.corpus import stopwords
from pyparsing import indentedBlock
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

def convertir_diccionario(fichero):
    diccionario = {}
    for index, data in fichero.iterrows():
        diccionario[index] = data[0]
    return diccionario

def carga_de_tweets():
    inicio = time.time()
    file_tweets = pd.read_excel(r'COV_train.xlsx',header=0, index_col=None, engine='openpyxl', sheet_name='Sheet 1', usecols="A")
    tweets  = []
    porcentaje_anterior = 0
    for index, data in file_tweets.iterrows():
        tweet_limpio = limpiar(data[0])
        tweet_tokenizado = tokenization(tweet_limpio)
        tweet_lemantizado = func_lemantizacion(tweet_tokenizado)
        tweets.append(tweet_lemantizado)
        porcentaje = round((index + 1) / len(file_tweets), 1) * 100
        if (porcentaje != porcentaje_anterior):
            tiempo = round(time.time() - inicio, 2)
            if (tiempo < 60):
                print(f'{porcentaje} % {tiempo} s')
            else:
                print(f'{porcentaje} % {round(tiempo / 60, 2)} min')
        porcentaje_anterior = porcentaje
    return tweets

def diccionario_modelo(fichero):
    diccionario = {}
    for line in fichero:
        line = line.split()
        diccionario[line[1]] = float(line[5])
    return diccionario

def clasificacion(tweets, fichero, fichero_resumen, tweets_originales):
    inicio = time.time()
    file_modeloP = open("modelo_lenguaje_P.txt", "r")
    file_modeloN = open("modelo_lenguaje_N.txt", "r")
    diccionario_modelo_P = diccionario_modelo(file_modeloP)
    diccionario_modelo_N = diccionario_modelo(file_modeloN)
    index = 0
    P_clase_P = 18046 / len(tweets)
    P_clase_N = 15397 / len(tweets)
    porcentaje_anterior = 0
    for tweet in tweets:
        primeros_10_caracteres = tweets_originales[index][0:10]
        PP = probability(tweet, diccionario_modelo_P) * P_clase_P
        PN = probability(tweet, diccionario_modelo_N) * P_clase_N
        if PP > PN:
            tipo = 'P'
        else:
            tipo = 'N'
        fichero.write(f'{primeros_10_caracteres},{round(PP, 2)},{round(PN, 2)},{tipo}\n')
        fichero_resumen.write(f'{tipo}\n')
        index += 1
        # Porcentaje de avance del programa
        porcentaje = round((index + 1) / len(tweets), 1) * 100
        if (porcentaje != porcentaje_anterior):
            tiempo = round(time.time() - inicio, 2)
            if (tiempo < 60):
                print(f'{porcentaje} % {tiempo} s')
            else:
                print(f'{porcentaje} % {round(tiempo / 60, 2)} min')
        porcentaje_anterior = porcentaje
        
def probability(tweet, diccionario):
    probabilidad = 1
    for word in tweet:
        if word in diccionario:
            probabilidad *= diccionario[word]
        else:
            probabilidad *= diccionario['UNK']
    return probabilidad

def main():
    inicio = time.time()
    file_clasificacion = open("clasificacion_alu0100829150.txt", "w")
    file_resumen = open("resumen_alu0100829150.txt", "w")
    file_tweets = pd.read_excel(r'COV_train.xlsx', index_col=None, engine='openpyxl', sheet_name='Sheet 1', usecols="A")
    # Guardo los tweets originales en un diccionario
    tweets_originales = convertir_diccionario(file_tweets)
    primeros_10_caracteres = tweets_originales[0][0:10] # error aquí
    print(f'Aquí: \'{primeros_10_caracteres}\'')
    print(f'Preprocesando tweets...')
    # Carga de datos
    tweets = carga_de_tweets()
    final_carga = time.time()
    print(f'{len(tweets)} tweets preprocesados. T: {round(round(final_carga - inicio, 2) / 60, 2)} min')
    print(f'Clasificando tweets...')
    clasificacion(tweets, file_clasificacion, file_resumen, tweets_originales)
    final = round((final_carga - inicio), 2) / 60
    print(f'FIN. Tiempo total: {round(final, 2)} s')
    file_clasificacion.close()
    file_resumen.close()

def eficacia():
    fichero_salida = open("resumen_alu0100829150.txt", "r")
    diccionario_resultado = convertir_diccionario(fichero_salida)
    corpus = pd.read_excel(r'COV_train.xlsx', index_col=None, engine='openpyxl', sheet_name='Sheet 1', usecols="A,B")
    aciertos = 0
    for index, data in corpus.iterrows():
        if data[1] == "Positive" & diccionario_resultado[index] == 'P':
            aciertos += 1
        if data[1] == "Negative" & diccionario_resultado[index] == 'N':
            aciertos += 1
    eficacia = round(aciertos / len(diccionario_resultado) * 100, 2)
    print(f'Aciertos: {aciertos} Eficacia: {eficacia} %')
    fichero_salida.close()

main()
eficacia