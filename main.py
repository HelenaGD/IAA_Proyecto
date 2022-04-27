import pandas as pd
import re

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

def main():
    corpus = pd.read_excel(r'COV_train.xlsx', index_col=None, engine='openpyxl', sheet_name='Sheet 1', usecols="A,B")

    corpus_positivo = []
    corpus_negativo = []

    for index, data in corpus.iterrows():
        if (data[1] == "Positive"):
            tweet_limpio = limpiar(data[0])
            corpus_positivo.append(tweet_limpio)
        elif (data[1] == "Negative"):
            tweet_limpio = limpiar(data[0])
            corpus_negativo.append(tweet_limpio)

    cabecera_corpus_positivo = (f'Numero de documentos del corpus: {len(corpus_positivo)}')
    # 18046
    cabecera_corpus_negativo = (f'Numero de documentos del corpus: {len(corpus_negativo)}')
    # 15397

    # Numero de palabras del corpus
    palabras_corpus_positivo = 0
    palabras_corpus_negativo = 0
    for tweet in corpus_positivo:
        word = len(tweet.split(' '))
        palabras_corpus_positivo += word
    for tweet in corpus_negativo:
        word = len(tweet.split(' '))
        palabras_corpus_negativo += word
    print(f'Corpus positivo: {palabras_corpus_positivo}')
    print(f'Corpus negativo: {palabras_corpus_negativo}')

main()

def pruebas():
    tweet = "Esta...es..una..prueba"
    print(tweet)
    tweet_limpio = limpiar(tweet)
    print(tweet_limpio)

#pruebas()