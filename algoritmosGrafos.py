import numpy as np

INI_DIST = 10_000
DIST = 0
PREV = 1

def dijkstra(mAdjacencia, origem):
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

    qtdVertices = mAdjacencia.shape(0)

    # criar vetor dist | prev
    dp = np.zeros((qtdVertices,2))
    
    # criar vetor acm
    acm = np.zeros(mAdjacencia)

    # inicializar vetor dp
    dp[:,DIST] = INI_DIST
    dp[:,PREV('prev')] = np.nan

    dp[0,DIST] = 0
    
    while(True):
        # inserir vertice de menor dist
        menorDist = np.argmin(dp[:,DIST])
        
        if (acm[menorDist,:] == 0).all():
            acm[menorDist,:] = mAdjacencia[menorDist,:]

            for arco in acm[menorDist,:]:
                if arco:
                    pass

    # relaxar o vértices ligados a ele
    # atualizar acm
    # verificar se todos os vértices já foram inseridos
    pass