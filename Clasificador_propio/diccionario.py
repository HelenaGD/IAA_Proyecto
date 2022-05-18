import time
# Se abren los corpus
def main():
  file_corpus_positivo = open("corpusP.txt", "r")
  file_corpus_negativo = open("corpusN.txt", "r")
  diccionario_positivo = {}
  diccionario_negativo = {}
  
  inicio = time.time()

  iterador = 0
  for line in file_corpus_positivo:
    line = line.strip('\n')
    if iterador < 2:
      iterador += 1
    else:
      diccionario_positivo[line] = 0
      
  file_corpus_positivo.close()
  file_corpus_positivo = open("corpusP.txt", "r")
  iterador = 0
  for line in file_corpus_positivo:
    line = line.strip('\n')
    if iterador < 2:
      iterador += 1
    else :
      diccionario_positivo[line] += 1
  
  final = time.time() - inicio
  print(diccionario_positivo['a'])
  print(f'Tiempo: {round(final, 2)}s')
  
main()