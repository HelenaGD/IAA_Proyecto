from monkeylearn import MonkeyLearn
import pandas as pd
import time

def carga_de_tweets():
  print(r'Cargando tweets...')
  file_tweets = pd.read_excel(r'COV_test_g1.xlsx',header=0, index_col=None, engine='openpyxl', sheet_name='Sheet 1', usecols="A")
  tweets = []
  porcentaje_anterior = 0
  inicio = time.time()
  for index, data in file_tweets.iterrows():
    tweets.append(data[0])
    porcentaje = round((index + 1) / len(file_tweets), 1) * 100
    if (porcentaje != porcentaje_anterior):
      tiempo = round(time.time() - inicio, 2)
      if (tiempo < 60):
        print(f'{porcentaje} % {tiempo} s')
      else:
        print(f'{porcentaje} % {round(tiempo / 60, 2)} min')
    porcentaje_anterior = porcentaje
  print(f'Tweets cargados.')
  return tweets

def main():
  ml = MonkeyLearn('f34fb1afccdc3f8807d7afaa90bb89d6d9cafa97')
  model_id = 'cl_cV7J5uJg'
  data = carga_de_tweets()
  print(f'Clasificando tweets...')
  inicio = time.time()
  result = ml.classifiers.classify(model_id, data)
  print(result.body)

main()
