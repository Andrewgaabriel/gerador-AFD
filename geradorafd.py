from importlib.resources import contents
import sys




def openFile(fileName):
    """Recebe o nome do arquivo e retorna o arquivo
    Args:
        fileName (str): nome do arquivo
    Returns:
        file: arquivo aberto
    """
    
    try:
        file = open(fileName, 'r')
        return file
    
    except IOError:
        print("Arquivo não encontrado")
        sys.exit()
        
        
        
def printFile(file):
    """Recebe o arquivo e imprime o conteúdo
    Args:
        file (file): arquivo aberto
    """
    
    for line in file:
        print(line)


def getParameters():
    """Recebe os parâmetros passados pelo usuário
    Returns:
        fileName (str): nome do arquivo
    """
    
    if len(sys.argv) == 2:
        fileName = sys.argv[1]
        return fileName
    else:
        print("Uso: geradorafd.py <nomeDoArquivo>")
        sys.exit()
        
        
        
def getFileContent(file):
    """Receve o arquivo e retorna o conteúdo
    Args:
        file (file): arquivo aberto
    Returns:
        contents (vetor): conteúdo do arquivo

    """
    contents = []
    for line in file:
        contents.append(line)
    return contents



