class Processo:
    def __init__(self, tempoChegada, tempoExecucao):
        self.tempoChegada = tempoChegada    
        self.tempoExecucao = tempoExecucao  
        self.tempoInicio = -1                
        self.tempoTermino = 0                
        self.tempoEspera = 0                 
        self.tempoRetorno = 0             
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
            tempoAtual += processoEscolhido.tempoExecucao
            processosExecutados.append(processoEscolhido)
        else:
            tempoAtual = min(processos, key=lambda p: p.tempoChegada).tempoChegada
    return processosExecutados

def rr(processos, quantum=2):
    tempoAtual = 0
    fila = []
    processosExecutados = []
    processos.sort(key=lambda p: p.tempoChegada)  

    while processos or fila:
        while processos and processos[0].tempoChegada <= tempoAtual:
            fila.append(processos.pop(0))  

        if fila:
            processoAtual = fila.pop(0)

            # Marca o tempo de início apenas na primeira vez que o processo começa a ser executado
            if processoAtual.tempoInicio == -1:
                processoAtual.tempoInicio = tempoAtual 

            tempo_executado = min(processoAtual.tempoRestante, quantum)
            processoAtual.tempoRestante -= tempo_executado
            tempoAtual += tempo_executado

            # Se o processo terminou
            if processoAtual.tempoRestante == 0:
                processoAtual.tempoTermino = tempoAtual
                processoAtual.tempoRetorno = processoAtual.tempoTermino - processoAtual.tempoChegada
                processoAtual.tempoEspera = processoAtual.tempoRetorno - processoAtual.tempoExecucao
                processosExecutados.append(processoAtual)
            else:
                fila.append(processoAtual)  # Reinsere o processo na fila se ainda não terminou

        else:
            tempoAtual = processos[0].tempoChegada if processos else tempoAtual  # Avança no tempo

    return processosExecutados

def calculaTempoMedio(processos):
    totalEspera = 0
    totalRetorno = 0
    totalResposta = 0

    for processo in processos:
        totalEspera += processo.tempoEspera
        totalRetorno += processo.tempoRetorno
        totalResposta += processo.tempoInicio - processo.tempoChegada

    esperaMedia = totalEspera / len(processos)
    retornoMedio = totalRetorno / len(processos)
    respostaMedia = totalResposta / len(processos)

    return esperaMedia, retornoMedio, respostaMedia


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
