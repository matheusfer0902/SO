class Processo:
    def __init__(self, tempo_chegada, tempo_execucao):
        self.tempo_chegada = tempo_chegada    
        self.tempo_execucao = tempo_execucao  
        self.tempo_inicio = -1                
        self.tempo_termino = 0                
        self.tempo_espera = 0                 
        self.tempo_retorno = 0             
        self.tempo_restante = tempo_execucao  

def ler_processos_arquivo(nome_arquivo):
    processos = []
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas:
            tempo_chegada, tempo_execucao = map(int, linha.split())
            processos.append(Processo(tempo_chegada, tempo_execucao))
    return processos

def fcfs(processos):
    processos.sort(key=lambda p: p.tempo_chegada)
    tempo_atual = 0
    for processo in processos:
        if tempo_atual < processo.tempo_chegada:
            tempo_atual = processo.tempo_chegada
        processo.tempo_inicio = tempo_atual
        processo.tempo_termino = processo.tempo_inicio + processo.tempo_execucao
        processo.tempo_retorno = processo.tempo_termino - processo.tempo_chegada
        processo.tempo_espera = processo.tempo_retorno - processo.tempo_execucao
        tempo_atual += processo.tempo_execucao
    return processos

def sjf(processos):
    processos.sort(key=lambda p: (p.tempo_chegada, p.tempo_execucao))
    tempo_atual = 0
    processos_executados = []
    while processos:
        processos_disponiveis = [p for p in processos if p.tempo_chegada <= tempo_atual]
        if processos_disponiveis:
            processo_selecionado = min(processos_disponiveis, key=lambda p: p.tempo_execucao)
            processos.remove(processo_selecionado)
            processo_selecionado.tempo_inicio = tempo_atual
            processo_selecionado.tempo_termino = processo_selecionado.tempo_inicio + processo_selecionado.tempo_execucao
            processo_selecionado.tempo_retorno = processo_selecionado.tempo_termino - processo_selecionado.tempo_chegada
            processo_selecionado.tempo_espera = processo_selecionado.tempo_retorno - processo_selecionado.tempo_execucao
            tempo_atual += processo_selecionado.tempo_execucao
            processos_executados.append(processo_selecionado)
        else:
            tempo_atual = min(processos, key=lambda p: p.tempo_chegada).tempo_chegada
    return processos_executados

def rr(processos, quantum=2):
    tempo_atual = 0
    fila = []
    processos_executados = []
    processos.sort(key=lambda p: p.tempo_chegada)  

    while processos or fila:
        while processos and processos[0].tempo_chegada <= tempo_atual:
            fila.append(processos.pop(0))  

        if fila:
            processo_atual = fila.pop(0)

            # Marca o tempo de início apenas na primeira vez que o processo começa a ser executado
            if processo_atual.tempo_inicio == -1:
                processo_atual.tempo_inicio = tempo_atual 

            tempo_executado = min(processo_atual.tempo_restante, quantum)
            processo_atual.tempo_restante -= tempo_executado
            tempo_atual += tempo_executado

            # Se o processo terminou
            if processo_atual.tempo_restante == 0:
                processo_atual.tempo_termino = tempo_atual
                processo_atual.tempo_retorno = processo_atual.tempo_termino - processo_atual.tempo_chegada
                processo_atual.tempo_espera = processo_atual.tempo_retorno - processo_atual.tempo_execucao
                processos_executados.append(processo_atual)
            else:
                fila.append(processo_atual)  # Reinsere o processo na fila se ainda não terminou

        else:
            tempo_atual = processos[0].tempo_chegada if processos else tempo_atual  # Avança no tempo

    return processos_executados

def calcular_tempos_medios(processos):
    total_espera = 0
    total_retorno = 0
    total_resposta = 0

    for processo in processos:
        total_espera += processo.tempo_espera
        total_retorno += processo.tempo_retorno
        total_resposta += processo.tempo_inicio - processo.tempo_chegada

    n = len(processos)
    espera_media = total_espera / n
    retorno_medio = total_retorno / n
    resposta_media = total_resposta / n

    return espera_media, retorno_medio, resposta_media


nome_arquivo = 'entrada.txt' 
processos = ler_processos_arquivo(nome_arquivo)

# FCFS
processos_fcfs = [Processo(p.tempo_chegada, p.tempo_execucao) for p in processos]
processos_executados_fcfs = fcfs(processos_fcfs)
espera_media_fcfs, retorno_medio_fcfs, resposta_media_fcfs = calcular_tempos_medios(processos_executados_fcfs)

# SJF
processos_sjf = [Processo(p.tempo_chegada, p.tempo_execucao) for p in processos]
processos_executados_sjf = sjf(processos_sjf)
espera_media_sjf, retorno_medio_sjf, resposta_media_sjf = calcular_tempos_medios(processos_executados_sjf)

# RR 
processos_rr = [Processo(p.tempo_chegada, p.tempo_execucao) for p in processos]
processos_executados_rr = rr(processos_rr, quantum=2)
espera_media_rr, retorno_medio_rr, resposta_media_rr = calcular_tempos_medios(processos_executados_rr)

espera_media_fcfs = str(espera_media_fcfs).replace('.', ',')
retorno_medio_fcfs = str(retorno_medio_fcfs).replace('.', ',')
resposta_media_fcfs = str(resposta_media_fcfs).replace('.', ',')

espera_media_sjf = str(espera_media_sjf).replace('.', ',')
retorno_medio_sjf = str(retorno_medio_sjf).replace('.', ',')
resposta_media_sjf = str(resposta_media_sjf).replace('.', ',')

espera_media_rr = str(espera_media_rr).replace('.', ',')
retorno_medio_rr = str(retorno_medio_rr).replace('.', ',')
resposta_media_rr = str(resposta_media_rr).replace('.', ',')

print(f"FCFS: {retorno_medio_fcfs} {resposta_media_fcfs} {espera_media_fcfs}")
print(f"SJF: {retorno_medio_sjf} {resposta_media_sjf} {espera_media_sjf}")
print(f"RR: {retorno_medio_rr} {resposta_media_rr} {espera_media_rr}")
