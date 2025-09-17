import numpy as np


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

    # deve vir com as variaveis de folga e excesso
    A = np.array(
        [1,1,-1,0,0,1,0],
        [-1,1,0,-1,0,0,1],
        [0,1,0,0,1,0,0]
    )

    b = ([2,1,3])
    c = ([1,-2])
    x0 = (4,5,6)
    # 1. Montar o tableau utilizando x0 como solução inicial
    columns = len(c)
    rows = len(b)

    tableau = np.zeros((rows,columns))

    tableau[0,:] = c
