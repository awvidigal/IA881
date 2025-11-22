import numpy as np

INI_DIST = 10_000
DIST = 0
PREV = 1

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
    '''

    # 1. Inicialização
    adjacencia = np.array(mAdjacencia)
    qtdVertices = adjacencia.shape[0]

    # 1.1. criar vetor dist | prev
    dp = np.zeros((qtdVertices,2))
    
    # 1.2. criar vetor de adjacencia da arvore de caminhos miinimos
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
        franja = dp[~vertices]
        indicesFranja = np.where(~vertices)[0]

        # 2.2. identificar vertice de menor dist fora da árvore
        menorDist = np.argmin(franja[:,DIST])
        menorDist = indicesFranja[menorDist]

        # 2.3. inserir o vertice na arvore
        vertices[menorDist] = True
        acm[menorDist,:] = adjacencia[menorDist,:]
        
        # 2.4. buscar as colunas que possuem mais de um valor
        for indiceColuna, valor in enumerate(acm[menorDist,:]):
            mascaraColuna = acm[:,indiceColuna] != 0
            distNova = valor + dp[menorDist,DIST]

            if np.sum(mascaraColuna) > 1:
                distAtual = dp[indiceColuna,DIST]                

                if distNova < distAtual:
                    acm[:,indiceColuna] = 0
                    acm[menorDist,indiceColuna] = valor

                    dp[indiceColuna,:] = distNova, menorDist+1

                else:
                    mascaraColuna[menorDist] = False
                    melhorPrev = np.where(mascaraColuna)[0]
                    melhorDist = acm[melhorPrev,indiceColuna]
                    acm[:,indiceColuna] = 0
                    acm[melhorPrev,indiceColuna] = melhorDist
                    

            elif valor:
                dp[indiceColuna,:] = distNova, menorDist+1

    return acm