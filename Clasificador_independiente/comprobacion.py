def main():
    fichero_mio = open('original.txt', 'r')
    fichero_profesor = open('fichero_profesor.txt', 'r')
    dic_1 = {}
    dic_2 = {}

    index = 0
    for line in fichero_mio:
        line = line.strip('\n')
        dic_1[index] = line
        index += 1
    
    index = 0
    for line in fichero_profesor:
        line = line.strip('\n')
        dic_2[index] = line
        index += 1

    index = 0
    correctas = 0
    incorrectas = 0
    for value in dic_1.values():
        if (value == dic_2[index]):
            correctas += 1
            continue
        else:
            incorrectas += 1
            continue
        index += 1
    
    print(f'Correctas: {correctas}')
    print(f'Incorrectas: {incorrectas}')

main()
