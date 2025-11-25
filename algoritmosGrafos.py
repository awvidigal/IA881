import numpy as np
import time

INI_DIST = 10_000
DIST = 0
PREV = 1

matrizTesteAGM = np.array(
    [
        [0,1,3,0,0,0],
        [1,0,1,3,2,0],
        [3,1,0,2,0,0],
        [0,3,2,0,-3,2],
        [0,2,0,-3,0,3],
        [0,0,0,2,3,0]
    ]
)

def dijkstra(mAdjacencia, origem = 0):
    '''
    Função que encontra a árvore de caminho mínimo utilizando o algoritmo de Dijkstra

    Parâmetros:
    -----------
    mAdjacência:
        Matriz de adjacência representando o grafo

    origem:
        Indicação do nó de origem

    Return:
    -------
    acm:
        Matriz de adjacência da árvore de caminho mínimo

    dp:
        Vetor final dist|prev para cada nó

    tempoDeExecucao:
        Tempo computacional para execução da arvore de caminhos mínimos

    iteracoes:
        Quantidade de iterações até a árvore

    relaxacoes:
        Quantidade de relaxacoes até a árvore
    '''

    # 1. Inicialização
    inicio = time.perf_counter()
    adjacencia = np.array(mAdjacencia)
    qtdVertices = adjacencia.shape[0]
    iteracoes = 0
    relaxacoes = 0

    # 1.1. criar vetor dist | prev
    dp = np.zeros((qtdVertices,2))
    
    # 1.2. criar vetor de adjacencia da arvore de caminhos minimos
    acm = np.zeros(adjacencia.shape)

    # 1.3. criar vetor de registro dos vértices já incluídos
    vertices = np.zeros(shape= qtdVertices, dtype= bool)

    # 1.4. inicialização do vetor dp
    dp[:,DIST] = INI_DIST
    dp[:,PREV] = np.nan

    dp[origem,:] = 0
    
    # 2. Inicio da busca pela arvore de caminhos minimos
    while not np.all(vertices):
        # 2.1. identificar os vertices que fazem parte da franja
        iteracoes += 1
        franja = dp[~vertices]
        indicesFranja = np.where(~vertices)[0]

        # 2.2. identificar vertice de menor dist fora da árvore
        menorDist = np.argmin(franja[:,DIST])
        menorDist = indicesFranja[menorDist]

        # 2.3. inserir o vertice na arvore
        vertices[menorDist] = True
        # acm[menorDist,:] = adjacencia[menorDist,:]

        # 2.4. Olhar para a linha correspondente na matriz de adjacencias e efetuar as relaxações
        for indice, valor in enumerate(adjacencia[menorDist,:]):
            if valor:
                distNova = valor + dp[menorDist,DIST]
                distAtual = dp[indice,DIST]

                if distNova < distAtual:
                    relaxacoes += 1
                    dp[indice,:] = distNova, menorDist+1

    for indice, valor in enumerate(dp):
        acm[int(valor[1]),indice] = adjacencia[int(valor[1]),indice]
        
    final = time.perf_counter()
    tempoDeExecucao = final - inicio
    return acm, dp, tempoDeExecucao, iteracoes, relaxacoes

def bellmanFord(mAdjacencia, ordem = 0):
    '''
    Função que encontra a árvore de caminho mínimo utilizando o algoritmo de bellman-ford

    Parâmetros:
    -----------
    mAdjacência:
        Matriz de adjacência representando o grafo

    ordem:
        Ordem de relaxação das arestas

    Return:
    -------
    acm:
        Matriz de adjacência da árvore de caminho mínimo

    dp:
        Vetor final dist|prev para cada nó

    tempoDeExecucao:
        Tempo computacional para execução da arvore de caminhos mínimos

    iteracoes:
        Quantidade de iterações até a árvore

    relaxacoes:
        Quantidade de relaxacoes até a árvore
    '''

    # 1. Inicialização
    inicio = time.perf_counter()
    adjacencia = np.array(mAdjacencia)
    iteracoes = 0
    relaxacoes = 0

    # 1.1. criar vetor dist | prev
    dp = np.zeros((adjacencia.shape[0],2))
    dp[:,DIST] = INI_DIST
    dp[:,PREV] = np.nan
    dp[0,:] = 0

    # 1.2. criar matriz de adjacencia da arvore de caminhos minimos
    acm = np.zeros(adjacencia.shape)

    contador = 0 # contagem de iterações sem alteração
    alteraDp = True

    # 2. Montagem da árvore de caminhos mínimos
    while True:
        if not alteraDp:
            contador += 1
            if contador == 2:
                break
        
        iteracoes += 1
        alteraDp = False
        for indice, valor in np.ndenumerate(adjacencia):
            
            if valor:
                novaDist = valor + dp[indice[0],DIST]
                atualDist = dp[indice[1],DIST]
                
                if novaDist < atualDist:
                    relaxacoes += 1
                    dp[indice[1],:] = novaDist, indice[0]+1
                    alteraDp = True
                    contador = 0

    for indice, valor in enumerate(dp):
        acm[int(valor[1]),indice] = adjacencia[int(valor[1]),indice]

    final = time.perf_counter()
    tempoDeExecucao = final - inicio
    return acm, dp, tempoDeExecucao, iteracoes, relaxacoes

def prim(mAdjacencia, origem = 0):
    '''
    Função que encontra a árvore geradora minima utilizando o algoritmo de prim

    Parâmetros:
    -----------
    mAdjacência:
        Matriz de adjacência representando o grafo

    origem:
        Nó inicial para o processo guloso

    Return:
    -------
    agm:
        Matriz de adjacência da árvore de caminho mínimo

    tempoDeExecucao:
        Tempo computacional para execução da arvore de caminhos mínimos

    iteracoes:
        Quantidade de iterações até a árvore
    '''

    # 1. Inicializacao
    inicio = time.perf_counter()
    adjacencia = np.array(mAdjacencia)
    
    vertices    = np.zeros((adjacencia.shape[0],2)) # indice representa o vertice, coluna zero representa o predecessor e coluna um representa o valor do arco
    franja      = np.ones(adjacencia.shape[0])  # indice representa o vertice. True se estiver na franja, False c.c.
    agm         = np.zeros(adjacencia.shape)    # matriz de adjacencia da arvore geradora minima
    

    franja[origem] = False

    # 2. Inicio do processo
    while np.count_nonzero(vertices) < vertices.shape - 1:
        # Olhar para a linha de cada item no vértice e selecionar o menor valor, filtrando-se as colunas que já estão na árvore
        
        mascaraMatriz = franja # mascara para filtrar as colunas da matriz que não estão conectadas na árvore
        matrizFiltrada = adjacencia[:, mascaraMatriz] # matriz sem as colunas que já estao na arvore
        indicesAdjacencia = np.where(mascaraMatriz)[0]
        menorArco = INI_DIST    # inicializa com um valor muito grande para manter sempre o menor valor na busca
        
        for indice, valor in enumerate(vertices[:,0]):
            if (valor) or (not valor and indice == origem):
                # Busca do arco com menor valor que liga os vertices da árvore à franja
                if np.min(matrizFiltrada[indice,:]) < menorArco:
                    menorArco = np.argmin(matrizFiltrada[indice,:])
                    noDestino = indicesAdjacencia[menorArco]
                    noOrigem = indice

            vertices[noDestino, 0] = noOrigem
            vertices[noOrigem, 1] = menorArco
                
                 
        # Adicionar a coluna correspondente no vetor vertices
        # Adicionar o arco na matriz agm
    
    # 2.1. Encontrar os arcos que ligam a arvore atual à franja
    # 2.2. Selecionar o de menor custo
    # 2.3. Inserir o novo nó na árvore