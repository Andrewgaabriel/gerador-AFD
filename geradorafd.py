import sys
import pandas as pd


possibleRules = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
allRules = []




def openFile(fileName):
    """ Abre arquivo e retorna o objeto do arquivo """
    try:
        file = open(fileName, 'r')
        return file
    except:
        print('Erro ao abrir arquivo')




def getParam(arg):
    """ Retorna o parâmetro passado na linha de comando """
    return sys.argv[arg]




def getData(file):
    """ Pega o arquivo e retorna uma lista de linhas """
    data = list()
    for line in file:
        data.append(line)
    return data




def getTokens(data):
    """ Faz a busca dos tokens e retorna uma lista de tokens """
    dirtyTokens = []
    for line in data:
        if line == '\n':
            break
        else:
            dirtyTokens.append(line)
    return dirtyTokens




def getGR(data):
    """ Faz a busca das gramaticas e retorna uma lista de gramaticas """
    data.reverse()
    grs = []
    for line in data:
        if line == '\n':
            break
        else:
            grs.append(line)
    return removeQuebraLinha(grs)




def removeQuebraLinha(data):
    """ Remove quebra de linhas """
    cleaned = []
    for token in data:
        cleaned.append(token.replace('\n', ''))
    return cleaned




def parseTokens(tokens):
    """ Quebra os tokens no menor possível """
    parsed = []
    for token in tokens:
        for char in token:
            parsed.append(char)
    parsed = sorted(set(parsed))
    return parsed




def parseGR(grs):
    """ Faz o parse das gramaticas 
        e retorna uma lista:
        formato : [['<rulename>', ['<rule1>', '<rule2>', '<rule3>']], ['<rulename>', ['<rule1>', '<rule2>']]] """

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
    """ Pega os tokens presentes nas gramáticas """
    grTokens = []

    for rule in gr:
        temp = rule.split('::=')[1]
        temp = temp.split('|')

        for aux in temp:
            aux = aux.split('<')
            grTokens.append(aux[0])
            
    return sorted(set(grTokens))




def removeBlankSpace(data):
    """ remove espaços em branco """
    cleaned = []

    for token in data:
        cleaned.append(token.replace(' ', ''))

    return cleaned




def createTable(tokens, grs):
    """ Faz a criação da tabela"""

    indexes = []
    for rule in grs:
        indexes.append(rule[0])
        allRules.append(rule[0])

    indexes.append('ERR') # adiciona estado de erro
    
    table = pd.DataFrame(index=indexes, columns=tokens)

    return table



def updatePossibleRules():
    """ Faz a atualização da lista de possiveis nomes de regras """
    for rule in allRules:
        if rule not in possibleRules:
            continue
        else:
            possibleRules.remove(rule)
            
            

def removeEpsilon(data):
    """ Remove o simbolo epsilon """
    cleaned = []

    for token in data:
        if token == 'ε' or token == 'Îµ':
            continue
        else:
            cleaned.append(token)
    

    return cleaned




def virouTerminal(table, ruleName):
    """ Torna determinada regra em uma regra terminal """
    nova = '*' + ruleName
    table = table.rename(index = {ruleName:nova})
    return table



def newBlankRow(table, indexName):
    """ Adiciona uma linha em branco dado um nome de regra """
    lista = []
    
    for i in range(len(table.columns)):
        lista.append('ERR')

    table.loc[indexName] = lista
    allRules.append(indexName) # adiciona a regra na lista de regras
    
    return table



def criaRegraFinal(table, grName, terminal):
    """ Trata o caso de uma regra ter apenas um terminal
        cria-se uma regra final para o terminal """
        
    if '*' in grName:
        grName = grName.replace('*', '')
    
    updatePossibleRules()
    
    newGrName = possibleRules[0] # próximo nome de regra disponível
    
    if len(table.loc[grName, terminal]) > 1:
        table.loc[grName, terminal] += ',' + newGrName
        table = newBlankRow(table, newGrName)
        table = virouTerminal(table, newGrName)
    else:
        table.loc[grName, terminal] = newGrName
        table = newBlankRow(table, newGrName)
        table = virouTerminal(table, newGrName)
    
    updatePossibleRules()
        
    return table
        
    
        
    

def fillWithGRs(table, gramaticas):
    """ Faz o primeiro preenchimento da tabela
        Esse preenchimento é feito pelas gramáticas que foram passadas """

    print('Preenchendo tabela...', gramaticas)
    
    # Formato : [['A', [' e<A> ', ' i<A> ', '  ε']], ['S', [' e<A> ', ' i<A>']]]

    for gr in gramaticas:
        
        grName = str(gr[0])     # nome da gramatica : 'A'-> ['A', [' e<A> ', ' i<A> ', '  ε']]
        rules = gr[1]           # regras : ' e<A> ', ' i<A> ', '  ε' -> ['A', [' e<A> ', ' i<A> ', '  ε']]

        for rule in rules:

            rule = rule.replace(' ', '').replace('\n', '')

            if "ε" in rule or "Îµ" in rule: # Se tem epislon a regra em questão vira terminal

                print('Regra:', grName, 'tem epsilon')
                table = virouTerminal(table, grName)

                continue


            elif rule.find('<') == -1: # Se não tem (<) executa :: (É UM TERMINAL)
                
                terminal = rule
                table = criaRegraFinal(table, grName, terminal)
                
                continue

            else: # SE TEM SIMBOLO NÃO-TERMINAL
                
                rule = rule.replace('>', '')
                ruleSplited = rule.split('<')
                token = ruleSplited[0]
                production = str(ruleSplited[1])
                #print(token, production)
                if table.loc[grName, token] == 'nan':
                    table.loc[grName, token] = production
                else:
                    table.loc[grName, token] += ',' + production
                
        
    return ordenaTable(table)




def temRegraNova(table):
    """ Verifica se foram criadas novas regras """
    for index in table.index:
        for token in table.columns:
            if len(table.loc[index, token]) > 1 and table.loc[index, token] not in allRules:
                return True
            else:
                continue           
    



def ordenaTable(table):
    """ Ordena a tabela e deixa a tabela 'limpa' """
    for index in table.index:
        for token in table.columns:
            if ',' in table.loc[index, token]:
                table.loc[index, token] = table.loc[index, token].replace('-,', '')
                table.loc[index, token] = quebraEordena(table.loc[index, token])
            else:
                continue
    return table




def removeNan(table):
    """ Remove os 'nan's da tabela """
    for index in table.index:
        for token in table.columns:
            if table.loc[index, token] == 'nan':
                table.loc[index, token] = '-'
    return table



def quebraEordena(string):
    """ Usada para ordenar cada regra composta """
    
    string = string.split(',')
    string = sorted(set(string))
    newString = ','.join(string)
    
    return newString




def determiniza(afnd, tokens):
    """ Faz a determinização da tabela """

    afd = pd.DataFrame(columns=tokens) # cria a tabela vazia que será a AFD
    
    afd = afd[allTokens].astype(str)

    newRules = [] # Guarda as novas regras

    # VERIFICA SE FORAM CRIADAS NOVAS REGRAS
    
    for index in afnd.index:
        for token in afnd.columns:
            if len(afnd.loc[index, token]) > 1 and afnd.loc[index, token] not in allRules: # se é uma regra composta e não está na lista de regras
                
                newRules.append(quebraEordena(afnd.loc[index, token])) # guarda as novas regras
                allRules.append(quebraEordena(afnd.loc[index, token])) # adiciona no vetor global de regras
                afd.loc[index, token] = afnd.loc[index, token]
            else:
                afd.loc[index, token] = quebraEordena(afnd.loc[index, token])

    
    newRules = sorted(set(newRules))

    for rule in newRules: # Percorre o vetor de novas regras

        dados = dict()

        toSearch = rule.split(',')

        for ruleT in toSearch: # Percorre cada regra das novas regras

            for index in afd.index: # Percorre cada linha da tabela

                if ruleT == index:  # Se a regra for igual a linha da tabela

                    for token in afd.columns: # Percorre a coluna da tabela

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
    """ ADICIONA OS ESTADOS DE ERRO E AS CHAVES """
    
    for index in table.index:
        for token in table.columns:
            if ',' in table.loc[index, token]:
                table.loc[index, token] = '[' + table.loc[index, token].replace(',', '') + ']'
            elif '-' in afd.loc[index, token]:
                afd.loc[index, token] = 'ERR'


    return table




def carregaTokens(afnd, tokens):
    print('Carregando tokens...')
    return afnd



# Pega os dados do arquivo de entrada e coloca em um vetor
allData = getData(openFile(getParam(1)))


# Cria um vetor com todos os tokens
tokens = getTokens(allData)               


# Parseia os tokens e cria uma espécie de alfabeto da linguagem
parsedTokens = parseTokens(removeQuebraLinha(tokens))


# Pega os vetor gerado e coloca as regras em um vetor
grs = getGR(allData)


# Pega os tokens presentes nas regras e coloca em um vetor
tokensFromGRS = getGRStokens(grs)         


# Faz uma junção dos tokens (das regras e os fornecidos na entrada) -> forma um alfabeto total da linguagem
allTokens = removeBlankSpace(parsedTokens) + removeBlankSpace(tokensFromGRS) 
allTokens = sorted(set(allTokens))
allTokens = removeEpsilon(allTokens)



# Pega o vetor gerado e coloca as regras parseadas em um vetor
parsedGRs = parseGR(grs)                  


# cria a tabela (dataframe) para o AFND
afnd = createTable(allTokens, parsedGRs)    
afnd = afnd[allTokens].astype(str)

# preenche a tabela com as regras
afnd = fillWithGRs(afnd, parsedGRs)         
afnd = removeNan(afnd)# remove os 'nan's


# função para carregar os tokens na afd
afnd = carregaTokens(afnd, tokens)          






# DETERMINIZAÇÃO --------------------------------------------------------------




# determiniza o afnd + remove os 'nan' + ordena a tabela e normaliza
afd = determiniza(afnd, allTokens)           
afd = removeNan(afd)                        
afd = ordenaTable(afd)                      





# verifica se há novas regras geradas a partir das regras já determinizadas
time = 1
while temRegraNova(afd):                
    afd = determiniza(afd, allTokens)   # determiniza o afnd
    afd = ordenaTable(afd)              # ordena a tabela e normaliza
    print(f'\n ITERAÇÃO {time} \n\n',afd)                          # printa a tabela a cada etapa
    time += 1                            # incrementa o tempo de execução





# printa a tabela afnd final
print('--------------------------------AFND--------------------------------')
afnd = cleanTable(afnd)
print(afnd)
print('------------------------------------------------------------------')




# printa a tabela afd final
print('--------------------------------AFD--------------------------------')
afd = cleanTable(afd)
print(afd)
print('------------------------------------------------------------------')




# salva a tabela afnd em um arquivo .csv
afnd.to_csv('afnd.csv', index=True, header=True)
afd.to_csv('afd.csv', index=True, header=True)









# TODO: fazer minimização do AFD (i.e eliminar inalcançáveis e mortos)




# PARA ALTERAR O NOME DO INDICE DA TABELA
# df  =  df.rename(index = {'antigo':'novo'})



print('allrules',allRules)

""" 
print(afd)
afd = newBlankRow(afd, 'x')
print(afd)
print('allrules',allRules)
updatePossibleRules() """
