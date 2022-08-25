from os import rename
import sys
import pandas as pd


ESTADOFINAL = 'Z' # PROVISÓRIO ?
allRules = []




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
            #parsedTokens = parseTokens(tokens)
    return parseTokens(removeQuebraLinha(dirtyTokens))




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
            rule = rule.replace(' ','')

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
    indexes.append('*' + ESTADOFINAL) # adiciona estado final
    
    table = pd.DataFrame(index=indexes, columns=tokens)

    return table



def removeEpsilon(data):
    cleaned = []

    for token in data:
        if token == 'ε' or token == 'Îµ':
            continue
        else:
            cleaned.append(token)

    return cleaned



def fillWithGRs(table, grs):
    for gr in grs:
        ruleName = str(gr[0])   # nome da regra
        rules = gr[1]           # regras em si

        for rule in rules:
            rule = rule.replace(' ', '').replace('\n', '')


            if "ε" in rule or "Îµ" in rule: 
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
                
        
    return ordenaTable(table)




def temRegraNova(table):
    for index in table.index:
        for token in table.columns:
            if len(table.loc[index, token]) > 1 and table.loc[index, token] not in allRules:
                return True
            else:
                continue           
    



def ordenaTable(table):
    for index in table.index:
        for token in table.columns:
            if ',' in table.loc[index, token]:
                table.loc[index, token] = table.loc[index, token].replace('-,', '')
                table.loc[index, token] = quebraEordena(table.loc[index, token])
            else:
                continue
    return table




def removeNan(table):
    for index in table.index:
        for token in table.columns:
            if table.loc[index, token] == 'nan':
                table.loc[index, token] = '-'
    return table




def printTable(table):
    for index in table.index:
        for token in table.columns:
            print('linha :', index, 'coluna: ',token, 'valor: ', table.loc[index, token])




def quebraEordena(string):
    string = string.split(',')
    string = sorted(set(string))
    newString = ','.join(string)
    return newString




def determiniza(afnd, tokens):

    afd = pd.DataFrame(columns=tokens)
    afd = afd[allTokens].astype(str)

    newRules = []

    # VERIFICA SE FORAM CRIADAS NOVAS REGRAS
    
    for index in afnd.index:
        for token in afnd.columns:
            if len(afnd.loc[index, token]) > 1 and afnd.loc[index, token] not in allRules: # SE TEM VÁRIAS REGRAS
                
                newRules.append(quebraEordena(afnd.loc[index, token]))
                allRules.append(quebraEordena(afnd.loc[index, token])) #adiciona no vetor global de regras
                afd.loc[index, token] = afnd.loc[index, token]
            else:
                afd.loc[index, token] = quebraEordena(afnd.loc[index, token])

    
    newRules = sorted(set(newRules))

    for rule in newRules: # Percorre o vetor de novas regras

        dados = dict()
        
        #rule = '[' + rule.replace(',', '') + ']'

        toSearch = rule.split(',')

        for ruleT in toSearch: # Percorre cada regra da nova regra

            for index in afd.index: # Percorre cada linha da tabela

                if ruleT == index:  # Se a regra for igual a linha da tabela

                    for token in afd.columns: # Percorre cada coluna da tabela

                        if afd.loc[index, token] == 'nan': # se for 'nan', não faz nada
                            continue

                        else:

                            if dados.get(token) == None: # se ja não existe nada no dicionário
                                dados[token] = afd.loc[index, token] # simplesmente adiciona o token no dicionário

                            elif dados.get(token) != None: # se ja existe algum token no dicionário

                                if afd.loc[index, token] not in dados[token]: # se o token que eu quero adicionar não está no dicionário
                                    dados[token] += ',' + afd.loc[index, token] # adiciona o token no dicionário

                                else:
                                    continue

        for token in dados:
            rule = rule.replace('-,', '').replace(',', '')
            afd.loc[rule, token] = dados[token]

    return afd




def cleanTable(table):
    for index in table.index:
        for token in table.columns:
            if ',' in table.loc[index, token]:
                table.loc[index, token] = '[' + table.loc[index, token].replace(',', '') + ']'


    return table




allData = getData(openFile(getParam(1)))  # Pega os dados do arquivo de entrada e coloca em um vetor
tokens = getTokens(allData)               # Pega os vetor gerado e coloca os tokens em um vetor
grs = getGR(allData)                      # Pega os vetor gerado e coloca as regras em um vetor
tokensFromGRS = getGRStokens(grs)         # Pega os tokens presentes nas regras e coloca em um vetor
allTokens = removeBlankSpace(tokens) + removeBlankSpace(tokensFromGRS) # Faz uma junção dos tokens (das regras e os fornecidos na entrada)
allTokens = sorted(set(allTokens))        # Remove as duplicatas e ordena
parsedGRs = parseGR(grs)                  # Pega o vetor gerado e coloca as regras parseadas em um vetor
allTokens = removeEpsilon(allTokens)      # Remove o epsilon das gramáticas


afnd = createTable(allTokens, parsedGRs)    # cria a tabela (dataframe) para o AFND
afnd = afnd[allTokens].astype(str)          # altera o tipo de dados para string
afnd = fillWithGRs(afnd, parsedGRs)         # preenche a tabela com as regras
afnd = removeNan(afnd)                      # remove os 'nan'
print(afnd)                                 # printa a tabela


afd= determiniza(afnd, allTokens)           # determiniza o afnd
afd = afd[allTokens].astype(str)            # altera o tipo de dados para string
afd = removeNan(afd)                        # remove os 'nan'
afd = ordenaTable(afd)                      # ordena a tabela e normaliza


while temRegraNova(afd):                # função que verifica se há novas regras geradas a partir das regras já determinizadas
    afd = determiniza(afd, allTokens)   # determiniza o afnd
    afd = ordenaTable(afd)              # ordena a tabela e normaliza
    print(afd)                          # printa a tabela a cada etapa
    print("\nAFD\n")





print('--------------------------------AFND--------------------------------')
afnd = cleanTable(afnd)
print(afnd)
print('------------------------------------------------------------------')


print('--------------------------------AFD--------------------------------')
afd = cleanTable(afd)
print(afd)
print('------------------------------------------------------------------')


afnd.to_csv('afnd.csv', index=True, header=True)
afd.to_csv('afd.csv', index=True, header=True)



# TODO: fazer minimização do AFD (i.e eliminar inalcançáveis e mortos)

