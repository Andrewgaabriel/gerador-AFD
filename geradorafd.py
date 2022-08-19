import sys


""" -----------------Abrindo arquivo de log------------------------------------------------------- """
def openFile(fileName):
    try:
        file = open(fileName, 'r')
        return file
    except:
        print('Erro ao abrir arquivo')
""" -------------------------------------------------------------------------------------------- """




""" -----------------------Função para imprimir conteúdo de um vetor/lista/arquivo--------------- """
def printFile(file):
    for line in file:
        print(line)

""" -------------------------------------------------------------------------------------------- """




""" --------------------Função que pega o nome do arquivo de entrada------------------------------ """
def getParam(arg):
    return sys.argv[arg]

""" -------------------------------------------------------------------------------------------- """




""" ----------------Pega os dados do arquivo e coloca em um vetor-------------------------------- """
def getData(file):
    data = list()
    for line in file:
        data.append(line)
    return data
""" -------------------------------------------------------------------------------------------- """




file = openFile(getParam(1))                    # Abre o arquivo de entrada
#printFile(file)                                # Imprime o conteúdo do arquivo
allData = getData(file)                         # Pega os dados do arquivo e coloca em um vetor
printFile(allData)                              # Imprime o conteúdo do vetor


file.close()                                    # Fecha o arquivo de entrada