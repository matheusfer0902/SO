# Lê a sequência de referência de páginas e o número de quadros do arquivo
def LerArquivoEntrada(CaminhoArquivo):
    with open(CaminhoArquivo, 'r') as Arquivo:
        Linhas = Arquivo.readlines()
    Dados = [int(Linha.strip()) for Linha in Linhas] # Remove qualquer espaço em branco
    return Dados

def FifoSubstituicaoPaginas(Quadros, SequenciaReferencia):
    Memoria = []
    FaltasPagina = 0
    for Pagina in SequenciaReferencia:
        if Pagina not in Memoria: # Verifica se tem paginas faltando
            FaltasPagina += 1
            if len(Memoria) < Quadros:
                Memoria.append(Pagina)
            else:
                Memoria.pop(0)
                Memoria.append(Pagina)
    return FaltasPagina

def OtmSubstituicaoPaginas(Quadros, SequenciaReferencia):
    Memoria = []
    FaltasPagina = 0
    for i, Pagina in enumerate(SequenciaReferencia):
        if Pagina not in Memoria: # Verifica se tem paginas faltando
            FaltasPagina += 1
            if len(Memoria) < Quadros:
                Memoria.append(Pagina)
            else:
                # Encontra a página que será utilizada mais tarde na sequência
                UsoMaisDistante = -1
                IndiceSubstituicao = -1
                for j in range(len(Memoria)):
                    try:
                        ProximoUso = SequenciaReferencia[i + 1:].index(Memoria[j])
                    except ValueError:
                        ProximoUso = float('inf') 
                    if ProximoUso > UsoMaisDistante: # Define a flag mais do uso mais distante
                        UsoMaisDistante = ProximoUso
                        IndiceSubstituicao = j
                Memoria[IndiceSubstituicao] = Pagina
    return FaltasPagina

def LruSubstituicaoPaginas(Quadros, SequenciaReferencia):
    Memoria = []
    UltimaUtilizacao = {}
    FaltasPagina = 0
    for i, Pagina in enumerate(SequenciaReferencia):
        if Pagina not in Memoria:
            FaltasPagina += 1
            if len(Memoria) < Quadros:
                Memoria.append(Pagina)
            else:
                # Encontra a página menos recentemente usada
                PaginaLru = min(Memoria, key=lambda p: UltimaUtilizacao.get(p, -1))
                Memoria[Memoria.index(PaginaLru)] = Pagina
        UltimaUtilizacao[Pagina] = i
    return FaltasPagina

CaminhoArquivo = 'Projeto 2/entrada2.txt'
    
Dados = LerArquivoEntrada(CaminhoArquivo)
    
# Extrai o número de quadros e a sequência de referência de páginas
Quadros = Dados[0]
SequenciaReferencia = Dados[1:]
    
FaltasFifo = FifoSubstituicaoPaginas(Quadros, SequenciaReferencia)
FaltasOtm = OtmSubstituicaoPaginas(Quadros, SequenciaReferencia)
FaltasLru = LruSubstituicaoPaginas(Quadros, SequenciaReferencia)
    
print(f"FIFO {FaltasFifo}")
print(f"OTM {FaltasOtm}")
print(f"LRU {FaltasLru}")