import sys
from this import d
import pandas as pd



ESTADOFINAL = 'D' # PROVISÓRIO ?


def openFile(fileName):
    try:
        file = open(fileName, 'r')
        return file
    except:
        print('Erro ao abrir arquivo')




def printFile(file):
    for line in file:
        print(line)




def getParam(arg):
    return sys.argv[arg]



def getData(file):
    data = list()
    for line in file:
        data.append(line)
    return data


def getTokens(data):
    dirtyTokens = []
    for line in data:
        if line == '\n':
            break
        else:
            dirtyTokens.append(line)
    
    return removeQuebraLinha(dirtyTokens)


def getGR(data):
    data.reverse()
    grs = []
    for line in data:
        if line == '\n':
            break
        else:
            grs.append(line)
    
    return removeQuebraLinha(grs)




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
    
    parsed = sorted(set(parsed))

    return parsed


def parseGR(grs):
    parsedGRs = []
    
    for gr in grs:
        completedRule = []

        dirtyRuleName = gr.split('::=')[0]
        ruleName = dirtyRuleName.replace('<','').replace('>','')

        dirtyRules = gr.split('::=')[1]
        rules = dirtyRules.split('|')

        for rule in rules:
            rule = rule.replace(' ','s')

        ruleName = ruleName.replace(' ','')

        completedRule.append(ruleName)
        completedRule.append(rules)

        parsedGRs.append(completedRule)

    return parsedGRs


def getGRStokens(gr):
    grTokens = []

    for rule in gr:
        temp = rule.split('::=')[1]
        temp = temp.split('|')

        for aux in temp:
            aux = aux.split('<')
            grTokens.append(aux[0])
            
    return sorted(set(grTokens))



def removeBlankSpace(data):
    cleaned = []

    for token in data:
        cleaned.append(token.replace(' ', ''))

    return cleaned



def createTable(tokens, grs):

    indexes = []
    for rule in grs:
        indexes.append(rule[0])
    indexes.append('*' + ESTADOFINAL)
    
    table = pd.DataFrame(index=indexes, columns=tokens)

    return table



def removeEpsilon(data):
    cleaned = []

    for token in data:
        if token != 'ε':
            cleaned.append(token)

    return cleaned



def fillWithGRs(table, grs):
    for gr in grs:
        ruleName = str(gr[0])   # nome da regra
        rules = gr[1]           # regras em si

        for rule in rules:
            rule = rule.replace(' ', '').replace('\n', '')


            if "ε" in rule: 
                #IMPLEMENTAR TRATAMENTO DE QND OCORRER EPSILON
                continue


            elif rule.find('<') == -1: # SE TEM (<) RETORNA != -1
                token = rule
                table.loc[ruleName, token] += ',' + ESTADOFINAL

            else: # SE TEM SIMBOLO NÃO-TERMINAL
                rule = rule.replace('>', '')
                ruleSplited = rule.split('<')
                token = ruleSplited[0]
                production = str(ruleSplited[1])
                #print(token, production)
                if table.loc[ruleName, token] == 'nan':
                    table.loc[ruleName, token] = production
                else:
                    table.loc[ruleName, token] += ',' + production
                
        
    return table


def determiniza(afnd, tokens):
    afd = pd.DataFrame(columns=tokens)
    #implementar aqui a determinização da afnd





allData = getData(openFile(getParam(1)))        # Pega os dados do arquivo e coloca em um vetor
#printFile(allData)                              # Imprime o conteúdo do vetor

tokens = getTokens(allData)                     # Pega os tokens sujos
#printFile(tokens)                               # Imprime o conteúdo do vetor

parsedTokens = parseTokens(tokens)              # Parseia os tokens
#printFile(parsedTokens)                         # Imprime o conteúdo do vetor

grs = getGR(allData)                            # Pega os GRs
#printFile(grs)                                  # Imprime o conteúdo do vetor

tokensFromGRS = getGRStokens(grs)                    # Pega os tokens do GRs
#printFile(tokensFromGRS)                              # Imprime o conteúdo do vetor


#parsedTokens =removeBlankSpace(parsedTokens)
#tokensFromGRS =removeBlankSpace(tokensFromGRS)

allTokens = removeBlankSpace(parsedTokens) + removeBlankSpace(tokensFromGRS)         # Merge dos tokens
allTokens = sorted(set(allTokens))             # Remove as duplicatas e ordena
#printFile(allTokens)                              # Imprime o conteúdo do vetor

parsedGRs = parseGR(grs)                    # Parseia os GRs
#printFile(parsedGRs)                            # Imprime o conteúdo do vetor


allTokens = removeEpsilon(allTokens)


afnd = createTable(allTokens, parsedGRs)
print(afnd)
afnd = afnd[allTokens].astype(str)
afnd = fillWithGRs(afnd, parsedGRs)
print(afnd)



print(allTokens)
print(parsedGRs)




# TODO: IMPLEMENTAR A TABELA (CRIAR FUNÇÕES GENÉRICAS PARA FZR ESSAS TAREFAS)
# TODO: TRANSFORMAR O AFND PARA O AFD
# TODO: FAZER A MINIMIZAÇÃO DO AFD
# TODO: GERAR O ARQUIVO DE SAIDA

 