import numpy as np
import pandas as pd

MAX_ITERATIONS  = 200
BASEIN_COLOR    = 'green!10'
BASEOUT_COLOR   = 'red!10'

def verificaTablauPreparado(tableau):
    '''
    Parametros:
    -----------
        tableau:
            Dataframe que representa o tableau inicial


    Return:
    -------
        True: se está na forma preparada
        False: caso contrário
    '''

    columnsLabels   = tableau.columns
    rowsLabels      = tableau.index
    
    base = rowsLabels.tolist()
    base.remove('z')

    # isPrepared = True

    for var in base:
        if tableau.loc['z', var]:
            return False

    for index in rowsLabels:
        if index != 'z':
            if tableau.loc[index, index] != 1:
                return False

            for var in base:
                if index != var:
                    if tableau.loc[index, var]:
                        return False
    
    return True

def preparaTableau(tableau):
    '''
    Parametros:
    -----------
        tableau:
            Dataframe que representa o tableau inicial


    Return:
    -------
        tableau:
            Dataframe contendo o tableau na forma preparada
    '''
    columnsLabels   = tableau.columns
    rowsLabels      = tableau.index
    dictColumns     = {rotulo: indice for indice, rotulo in enumerate(columnsLabels)}

    base = rowsLabels.tolist()
    base.remove('z')


    for var in base:
        if tableau.loc[var,var] > 1:
            tableau.loc[var] = tableau.loc[var] / tableau.loc[var,var]

        for row in tableau.itertuples():
            if row.Index != var:
                if row[dictColumns[var] + 1]:
                    multValue = -row[dictColumns[var] + 1]
                    tableau.loc[row.Index] = tableau.loc[row.Index] + (multValue * tableau.loc[var])

    return tableau


def simplex(A: list, b: list, c: list, x0: list):
    '''
    Parametros:
    -----------

    A: 
        deve ser a matriz preparada de forma que Ax = b
    
    x0:
        deve conter os indices das variaveis basicas para a solução inicial
    '''
    
    # 1. montar o algoritmo para problemas onde a solução inicial é dada
    # 2. montar o algoritmo para enconrar a solução factivel inicial
    # 3. implementar prevenção a ciclagem
    # 4. mostrar o grafico com a regiao factivel e a sequencia de pontos utilizados durante a solução do problema

    # Matrizes de teste
    A = np.array([
        [-2,0,3,1,0,0,0,0],
        [2,1,2,0,1,0,0,0],
        [0,-1,3,0,0,1,0,0],
        [3,3,0,0,0,0,1,0],
        [1,-1,-3,0,0,0,0,1]    
    ])

    b = np.array([6,7,7,8,9])
    c = np.array([-2,0,-3])
    x0 = np.array([4,5,6,7,8])


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
    tableau = np.vstack([c, A])
    tableau = np.hstack([tableau, b])

    # 1.4. Adicionando índices de linhas e colunas
    columns = np.arange(0, aColumns, 1)
    indexCol = ['x' + str(value+1) for value in columns]
    indexCol.append('LD')
    labelBase = ['x' + str(value+1) for value in x0]

    indexRow = ['x' + str(value) for value in x0]
    indexRow.insert(0,'z')
    
    tableau = pd.DataFrame(
        data= tableau,
        index= indexRow,
        columns= indexCol
    )

    dictColumns = {rotulo:indice for indice, rotulo in enumerate(tableau.columns)}

    # 1.5. Colocando o tableau na forma preparada
    if not verificaTablauPreparado(tableau):
        tableau = preparaTableau(tableau)

    # 1.6. Resolvendo o tableau
    for iterations in range(MAX_ITERATIONS):
        # verifica se há valores positivos na linha z do tableau
        notOptimal = (tableau.loc['z'] < 0).any()

        if notOptimal:
            # identifica a variavel que entra na base
            baseIn = tableau.loc['z'].idxmin()            
            
            # prepara para o teste de bloqueio, considerando apenas valores positivos na coluna
            filterValues = tableau[baseIn] > 0
            
            if (filterValues == False).all():
                print('O problema é ilimitado')
                break
            
            tableauCopy = tableau[filterValues].copy()
            
            baseOut = (tableauCopy['LD'] / tableauCopy[baseIn]).idxmin()

            # deixa '1' na celula da nova variavel q entrou
            if tableau.loc[baseOut, baseIn] > 1:
                tableau.loc[baseOut] = tableau.loc[baseOut] / tableau.loc[baseOut, baseIn]

            # transforma a coluna da variavel que entrou em uma coluna da matriz identidade
            indexBaseIn = tableau.columns.get_loc(baseIn)
            for row in tableau.itertuples():
                if row.Index != baseOut:
                    if row[indexBaseIn + 1]:
                        multValue = -row[indexBaseIn + 1]
                        tableau.loc[row.Index] = tableau.loc[row.Index] + (multValue * tableau.loc[baseOut])

            # atualiza o label de linha da variavel q entrou
            tableau.rename(
                index= {baseOut: baseIn},
                inplace= True
            )

            # formatando a saida em latex
            baseFormat = ['c'] * (len(tableau.columns) + 1)
            baseFormat[0] = 'l'
            colorCol = f'>{{\\columncolor{{{BASEIN_COLOR}}}}}c' 
            baseFormat[indexBaseIn] = colorCol
            latexFormat = ' '.join(baseFormat)

            latex = tableau.to_latex(
                column_format= latexFormat,
                booktabs = False,
                escape= False
            )

            rowColor = f'\\rowcolor{{{BASEOUT_COLOR}}}'
            
            latex = latex.replace(
                baseOut,
                f'\n{rowColor} {baseOut}'
            )







    
    

