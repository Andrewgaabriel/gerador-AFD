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



""" -------------------Função que pega os tokens sujos------------------ """
def getTokens(data):
    dirtyTokens = []

    for line in data:
        if line == '\n':
            break
        else:
            dirtyTokens.append(line)
    
    

    return removeQuebraLinha(dirtyTokens)
""" -------------------------------------------------------------------------------------------- """

""" -------------------Função que pega os tokens sujos------------------ """
def getGR(data):
    data.reverse()
    grs = []

    for line in data:
        if line == '\n':
            break
        else:
            grs.append(line)
    
    

    return removeQuebraLinha(grs)
""" -------------------------------------------------------------------------------------------- """




def removeQuebraLinha(data):
    cleaned = []

    for token in data:
        cleaned.append(token.replace('\n', ''))

    return cleaned



def parseTokens(tokens):
    parsed = []

    for token in tokens:
        for char in token:
            parsed.append(char)
    
    #remove as duplicatas e ordena
    parsed = sorted(set(parsed))
    #parsed = list(set(parsed))

    return parsed


def parseGR(grs):
    parsedGRs = []

    
    for gr in grs:

        completedRule = []

        dirtyRuleName = gr.split('::=')[0]
        ruleName = dirtyRuleName.replace('<','').replace('>','')

        dirtyRules = gr.split('::=')[1]
        rules = dirtyRules.split('|')

        completedRule.append(ruleName)
        completedRule.append(rules)

        parsedGRs.append(completedRule)

    return parsedGRs






print("TRATAMENTO DE ARQUIVO\n")
allData = getData(openFile(getParam(1)))        # Pega os dados do arquivo e coloca em um vetor
printFile(allData)                              # Imprime o conteúdo do vetor
print("FIM DO TRATAMENTO DE ARQUIVO\n\n")


print("TRATAMENTO DE TOKENS\n")
tokens = getTokens(allData)                     # Pega os tokens sujos
printFile(tokens)                               # Imprime o conteúdo do vetor
print("\nPARSEA OS TOKENS\n\n")
parsedTokens = parseTokens(tokens)              # Parseia os tokens
printFile(parsedTokens)                         # Imprime o conteúdo do vetor
print("\nFIM DO TRATAMENTO DE TOKENS\n\n")



print("TRATAMENTO DE GR\n")
grs = getGR(allData)                            # Pega os GRs
printFile(grs)                                  # Imprime o conteúdo do vetor
print("\nPARSEA OS GRs\n\n")
parsedGRs = parseGR(grs)                    # Parseia os GRs
printFile(parsedGRs)                            # Imprime o conteúdo do vetor
print("\nFIM DO TRATAMENTO DE GR")
print(parsedGRs)