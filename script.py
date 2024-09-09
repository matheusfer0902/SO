class Processo:
    def __init__(self, tempoChegada, tempoExecucao):
        self.tempoChegada = tempoChegada    
        self.tempoExecucao = tempoExecucao  
        self.tempoInicio = None                
        self.tempoTermino = 0                
        self.tempoEspera = 0                 
        self.tempoRetorno = 0
        self.tempoResposta = 0             
        self.tempoRestante = tempoExecucao  

def lerArquivo(pathArquivo):
    processos = []
    with open(pathArquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas:
            tempoChegada, tempoExecucao = map(int, linha.split())
            processos.append(Processo(tempoChegada, tempoExecucao))
    return processos

def fcfs(processos):
    processos.sort(key=lambda p: p.tempoChegada)
    tempoAtual = 0
    for processo in processos:
        if tempoAtual < processo.tempoChegada:
            tempoAtual = processo.tempoChegada
        processo.tempoInicio = tempoAtual
        processo.tempoTermino = processo.tempoInicio + processo.tempoExecucao
        processo.tempoRetorno = processo.tempoTermino - processo.tempoChegada
        processo.tempoResposta = processo.tempoInicio - processo.tempoChegada
        processo.tempoEspera = processo.tempoRetorno - processo.tempoExecucao
        tempoAtual += processo.tempoExecucao
    return processos

def sjf(processos):
    processos.sort(key=lambda p: (p.tempoChegada, p.tempoExecucao))
    tempoAtual = 0
    processosExecutados = []
    while processos:
        processosProntos = [p for p in processos if p.tempoChegada <= tempoAtual]
        if processosProntos:
            processoEscolhido = min(processosProntos, key=lambda p: p.tempoExecucao)
            processos.remove(processoEscolhido)
            processoEscolhido.tempoInicio = tempoAtual
            processoEscolhido.tempoTermino = processoEscolhido.tempoInicio + processoEscolhido.tempoExecucao
            processoEscolhido.tempoRetorno = processoEscolhido.tempoTermino - processoEscolhido.tempoChegada
            processoEscolhido.tempoEspera = processoEscolhido.tempoRetorno - processoEscolhido.tempoExecucao
            processoEscolhido.tempoResposta = processoEscolhido.tempoInicio - processoEscolhido.tempoChegada
            tempoAtual += processoEscolhido.tempoExecucao
            processosExecutados.append(processoEscolhido)
        else:
            tempoAtual = min(processos, key=lambda p: p.tempoChegada).tempoChegada
    return processosExecutados

def rr(processos, quantum=2):
    filaAtiva = []  # Fila de processos prontos para execução
    filaPronto = []  # Fila de processos concluídos
    tempoAtual = 0  # Inicializa o tempo atual do sistema
    processoAtual = None  # Processo atualmente em execução
    processo = processos.copy()  # Cria uma cópia dos processos
    processo.sort(key=lambda x: x.tempoChegada)  # Ordena os processos pelo tempo de chegada
    prox = 0  # Índice para controlar os processos que estão chegando

    # Loop principal que continua até que todos os processos sejam concluídos
    while True:
        # Adiciona processos à fila de ativos se tiverem chegado
        while prox < len(processo) and processo[prox].tempoChegada <= tempoAtual:
            filaAtiva.append(processo[prox])
            prox += 1

        # Se há um processo pronto para ser executado
        if filaAtiva:
            processoAtual = filaAtiva.pop(0)  # Pega o próximo processo da fila

            # Se o processo está sendo iniciado pela primeira vez
            if processoAtual.tempoInicio is None:
                processoAtual.tempoInicio = tempoAtual
            
            # Calcula o tempo de execução baseado no quantum e no tempo restante do processo
            tempoExecutado = min(quantum, processoAtual.tempoRestante)
            processoAtual.tempoRestante -= tempoExecutado  # Atualiza o tempo restante
            tempoAtual += tempoExecutado  # Avança o tempo atual

            # Se o processo ainda não terminou, retorna para a fila
            if processoAtual.tempoRestante > 0:
                while prox < len(processo) and processo[prox].tempoChegada <= tempoAtual:
                    filaAtiva.append(processo[prox])
                    prox += 1
                filaAtiva.append(processoAtual)  # Reinsere o processo na fila de ativos
                processoAtual = None  # Libera o processo atual
            else:
                # Se o processo terminou, define o tempo de fim e adiciona à fila de prontos
                processoAtual.tempoTermino = tempoAtual
                filaPronto.append(processoAtual)

        else:
            # Se não há processos prontos, avança o tempo
            tempoAtual += 1

        # Condição de parada: quando não há mais processos na fila e todos já chegaram
        if not filaAtiva and prox >= len(processo):
            break

    # Calcula o tempo de resposta e espera para todos os processos prontos
    for processo in filaPronto:
        processo.tempoResposta = processo.tempoInicio - processo.tempoChegada
        processo.tempoEspera = processo.tempoTermino - processo.tempoChegada - processo.tempoExecucao
        processo.tempoRetorno = processo.tempoTermino - processo.tempoChegada

    return filaPronto

def calculaTempoMedio(processos):
    totalEspera = 0
    totalRetorno = 0
    totalResposta = 0

    for processo in processos:
        totalEspera += processo.tempoEspera
        totalRetorno += processo.tempoRetorno
        totalResposta += processo.tempoResposta

    esperaMedia = totalEspera / len(processos)
    retornoMedio = totalRetorno / len(processos)
    respostaMedia = totalResposta / len(processos)

    return esperaMedia, retornoMedio, respostaMedia

# Função para testar com o arquivo de entrada
pathArquivo = 'entrada.txt' 
processos = lerArquivo(pathArquivo)

# FCFS
processosFCFS = [Processo(p.tempoChegada, p.tempoExecucao) for p in processos]
processosExecutadosFCFS = fcfs(processosFCFS)
esperaMediaFCFS, retornoMedioFCFS, respostaMediaFCFS = calculaTempoMedio(processosExecutadosFCFS)

# SJF
processosSJF = [Processo(p.tempoChegada, p.tempoExecucao) for p in processos]
processosExecutadosSJF = sjf(processosSJF)
esperaMediaSJF, retornoMedioSJF, respostaMediaSJF = calculaTempoMedio(processosExecutadosSJF)

# RR 
processosRR = [Processo(p.tempoChegada, p.tempoExecucao) for p in processos]
processosExecutadosRR = rr(processosRR, quantum=2)
esperaMediaRR, retornoMedioRR, respostaMediaRR = calculaTempoMedio(processosExecutadosRR)

# Imprime os resultados
esperaMediaFCFS = str(esperaMediaFCFS).replace('.', ',')
retornoMedioFCFS = str(retornoMedioFCFS).replace('.', ',')
respostaMediaFCFS = str(respostaMediaFCFS).replace('.', ',')

esperaMediaSJF = str(esperaMediaSJF).replace('.', ',')
retornoMedioSJF = str(retornoMedioSJF).replace('.', ',')
respostaMediaSJF = str(respostaMediaSJF).replace('.', ',')

esperaMediaRR = str(esperaMediaRR).replace('.', ',')
retornoMedioRR = str(retornoMedioRR).replace('.', ',')
respostaMediaRR = str(respostaMediaRR).replace('.', ',')

print(f"FCFS: {retornoMedioFCFS} {respostaMediaFCFS} {esperaMediaFCFS}")
print(f"SJF: {retornoMedioSJF} {respostaMediaSJF} {esperaMediaSJF}")
print(f"RR: {retornoMedioRR} {respostaMediaRR} {esperaMediaRR}")
