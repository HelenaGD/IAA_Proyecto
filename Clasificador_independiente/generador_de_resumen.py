import pandas as pd
import time

def carga_de_resultados(file_salida):
  file_resultados = pd.read_excel(r'processed_batch_FINAL.xlsx',header=0, index_col=None, engine='openpyxl', sheet_name='Sheet 1', usecols="A,B")
  for index, data in file_resultados.iterrows():
    #primeros_10_caracteres = data[0][0:10]
    if ( data[1] == "Positive"):
      clasificacion = "P"
    elif ( data[1] == "Negative"):
      clasificacion = "N"
    file_salida.write(f'{clasificacion}\n')

def main():
  print('\n-----CLASIFICACION---')
  inicio = time.time()
  file_resumen = open('resumen_alu0100829150.txt', 'w')
  carga_de_resultados(file_resumen)
  final = round((time.time() - inicio), 2)
  print(f'Tiempo: {final}')

main()
