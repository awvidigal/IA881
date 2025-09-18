import numpy as np
import pandas as pd

MAX_ITERATIONS = 20


def simplex(A: list, b: list, c: list, x0: list):
    '''
    Parametros:
    -----------

    A: 
        deve ser a matriz preparada de forma que Ax = b
    
    x0:
        deve conter os indices das variaveis basicas paraa solução inicial
    '''
    
    # 1. montar o algoritmo para problemas onde a solução inicial é dada
    # 2. montar o algoritmo para enconrar a solução factivel inicial
    # 3. implementar prevenção a ciclagem
    # 4. mostrar o grafico com a regiao factivel e a sequencia de pontos utilizados durante a solução do problema

    # Matrizes de teste
    A = np.array([
        [1,-2,1,0,0],
        [-2,1,0,1,0],
        [5,3,0,0,1]    
    ])

    b = np.array([0,4,15])
    c = np.array([1,3])
    x0 = np.array([2,3,4])


    # 1. Montar o tableau utilizando x0 como solução inicial
    
    # 1.1. Ajuste do vetor c
    aColumns = A.shape[1]
    cColumns = c.shape[0]

    if aColumns > cColumns:
        c = np.pad(c, (0, aColumns - cColumns), 'constant')

    # 1.2. Ajuste do vetor b
    b = np.hstack([0,b])
    b = b.reshape(-1,1)

    # 1.3. Montando o tableau
    tableau = np.vstack([-c, A])
    tableau = np.hstack([tableau, b])

    # 1.4. Adicionando índices de linhas e colunas
    columns = np.arange(0, aColumns, 1)
    indexCol = ['x' + str(value) for value in columns]
    indexCol.append('LD')

    indexRow = ['x' + str(value) for value in x0]
    indexRow.insert(0,'z')

    tableau = pd.DataFrame(
        data= tableau,
        index= indexRow,
        columns= indexCol
    )

    for iterations in range(MAX_ITERATIONS):
        # verifica se há valores positivos na linha zdo tableau
        isOptimal = (tableau.loc['z'] < 0).any()

        if isOptimal:
            # identifica a variavel que entra na base
            baseIn = tableau.loc['z'].idxmin()            
            
            # prepara para o teste de bloqueio, considerando apenas valores positivos na coluna
            filterValues = tableau[baseIn] > 0
            tableauCopy = tableau[filterValues].copy()
            
            baseOut = (tableauCopy['LD'] / tableauCopy[baseIn]).idxmin()




    
    

