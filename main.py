import pandas as pd
import re
import nltk
import string
import time
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

def nltk_pos_tagger(nltk_tag):
  etiqueta = nltk_tag[0][1]
  if etiqueta.startswith('J'):
    return wordnet.ADJ
  elif etiqueta.startswith('V'):
    return wordnet.VERB
  elif etiqueta.startswith('N'):
    return wordnet.NOUN
  elif etiqueta.startswith('R'):
    return wordnet.ADV
  else:          
    return None

def limpiar(tweet):
    # remove links
    tweet_limpio = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', tweet, flags=re.MULTILINE)
    # remove the numbers
    # ints
    tweet_limpio = re.sub(r'/^\d+\s|\s\d+\s|\s\d+$/', ' ', tweet_limpio, flags=re.MULTILINE)
    # floats with '.'
    tweet_limpio = re.sub(r'(\d*\.\d+)|(\d+\.[0-9 ]+)', ' ', tweet_limpio, flags=re.MULTILINE)
    # floats with ','
    tweet_limpio = re.sub(r'(\d*\,\d+)|(\d+\,[0-9 ]+)', ' ', tweet_limpio, flags=re.MULTILINE)
    # remove users
    tweet_limpio = re.sub(r'(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)', ' ', tweet_limpio, flags=re.MULTILINE)
    # remove hastahgs
    tweet_limpio = re.sub(r'(#[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)', ' ', tweet_limpio, flags=re.MULTILINE)
    # remove '...' with blank spaces
    tweet_limpio = re.sub(r'/.+', ' ', tweet_limpio, flags=re.MULTILINE)
    # remove line breakers
    tweet_limpio = ' '.join(tweet_limpio.splitlines())
    #remove multiple spaces
    tweet_limpio = ' '.join(tweet_limpio.split())
    return tweet_limpio

def tokenization(corpus):
    stop = set(stopwords.words('english') + list(string.punctuation))
    the_list_of_tokens = []
    for text in corpus:
        # Tokenice with nltk
        doc = [i for i in nltk.word_tokenize(text.lower()) if (i not in stop and not i.isdigit())]
        for token in doc:
            token = re.sub(r'[0-9]', '', token)
            the_list_of_tokens.append(token)
    return the_list_of_tokens

def func_lemantizacion(lista_de_tokens):
    lista_final = []
    lemmantizer = WordNetLemmatizer()
    for word in lista_de_tokens:
        nltk_tag = nltk_pos_tagger(nltk.tag.pos_tag([word]))
        lista_final.append(lemmantizer.lemmatize(word))
    
    lista_final.sort()
    return lista_final

def escribir(lista, archivo):
    # Numero de palabras del corpus
    palabras_corpus = f'Numero de palabras del corpus: {len(lista)}\n'
    archivo.write(palabras_corpus)
    for token in lista:
        archivo.write(f'{token}\n')
    archivo.close();

def corpus_inicial():
    inicio = time.time()
    print(f'Cargando datos...')
    corpus = pd.read_excel(r'COV_train.xlsx', index_col=None, engine='openpyxl', sheet_name='Sheet 1', usecols="A,B")
    file_positivos = open("corpusP_inicial.txt", "w")
    file_negativos = open("corpusN_inicial.txt", "w")

    corpus_positivo = []
    corpus_negativo = []

    for index, data in corpus.iterrows():
        if (data[1] == "Positive"):
            tweet_limpio = limpiar(data[0])
            corpus_positivo.append(tweet_limpio)
        elif (data[1] == "Negative"):
            tweet_limpio = limpiar(data[0])
            corpus_negativo.append(tweet_limpio)

    cabecera_corpus_positivo = (f'Numero de documentos (tweets) del corpus: {len(corpus_positivo)}\n')
    file_positivos.write(cabecera_corpus_positivo)
    # 18046
    cabecera_corpus_negativo = (f'Numero de documentos (tweets) del corpus: {len(corpus_negativo)}\n')
    file_negativos.write(cabecera_corpus_negativo)
    # 15397
    limpieza = time.time()
    tiempo = round(limpieza - inicio, 2)
    print(f'Lectura realizada. T: {tiempo}s')

    print(f'Realizando la tokenizacion...')
    # Tokenizacion de las palabras de los tweets
    the_list_of_tokens_negativos = tokenization(corpus_negativo)
    the_list_of_tokens_positivos = tokenization(corpus_positivo)
    tokenizacion = time.time()
    tiempo = round(tokenizacion - limpieza, 2)
    print(f'Tokenizacion realizada. T: {tiempo} s')
    print(f'Realizando la lemantizacion...')
    # Lemantizacion de los tweets
    lista_final_negativos = func_lemantizacion(the_list_of_tokens_negativos)
    lista_final_positivos = func_lemantizacion(the_list_of_tokens_positivos)
    lemantizacion = time.time()
    tiempo = round(lemantizacion - tokenizacion, 2)
    print(f'Lemantizacion realizada. T: {tiempo} s')
    escribir(lista_final_positivos, file_positivos)
    escribir(lista_final_negativos, file_negativos)

def main():
    corpus_inicial()

main()

def pruebas():
    tweet = "Esta...es..una..prueba"
    print(tweet)
    tweet_limpio = limpiar(tweet)
    print(tweet_limpio)

#pruebas()