import numpy as np
import pandas as pd
import matrizes as mt

from itertools import combinations

MAX_ITERATIONS  = 200
BASEIN_COLOR    = 'green!10'
BASEOUT_COLOR   = 'red!10'
M_VALUE         = 100

def verificaTableauPreparado(tableau):
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
        if tableau.loc[var,var] != 1:
            tableau.loc[var] = tableau.loc[var] / tableau.loc[var,var]

        for rowIndex in tableau.index:
            if rowIndex != var and rowIndex != 'z':
                pivotValue = tableau.loc[rowIndex, var]
                if pivotValue != 0:
                    multValue = -pivotValue
                    tableau.loc[rowIndex] = tableau.loc[rowIndex] + (multValue * tableau.loc[var])

        if tableau.loc['z', var] != 0:
            multValue = -tableau.loc['z', var]
            tableau.loc['z'] = tableau.loc['z'] + (tableau.loc[var] * multValue)            

    return tableau

def bigM(tableau):
    '''
    Parametros:
    -----------

    tableau:
        matriz contendo o tableau sem solucao inicial factivel

    
    Return:
    -------

    bigMTableau:
        df montado com colunas big-M adicionadas
    '''
    qtdVarAux       = tableau.shape[0] - 1
    qtdCols         = tableau.shape[1]
    # indexCols       = ['x' + str(value + 1) for value in np.arange(0, qtdCols, 1)]
    newColumns      = np.arange(0, qtdVarAux, 1)
    indexNewCols    = ['M' + str(value+1) for value in newColumns]

    ldColumn = tableau['LD']
    tableau = tableau.drop(columns= ['LD'])
    
    for i in range(len(indexNewCols)):
        bigMCol = np.zeros(qtdVarAux + 1)
        bigMCol[0] = -M_VALUE
        bigMCol[i + 1] = 1
        tableau[indexNewCols[i]] = bigMCol

    tableau['LD'] = ldColumn

    bigMIndex = np.append('z', indexNewCols)

    tableau = tableau.set_axis(bigMIndex, axis= 0)
    
    return tableau

def localizaBaseInicial(tableau):
    '''
    Parametros:
    -----------

    A:
        matriz A de restrições. (Ax = b)

    
    Return:
    -------
    tableau:
        df alterado com as tags das variaveis de base nas linhas

    '''
    A = tableau.drop('z')

    a_columns = A.shape[1]
    a_rows = A.shape[0]

    # filtro de conteudo. desconsidera colunas que contenham valores diferentes de 0 ou 1
    colsBool = A.apply(lambda col: col.isin([0,1])).all(axis= 0)
    contentFiltered = A.loc[:, colsBool]

    # filtro de soma nas colunas. desconsidera colunas cuja soma seja diferente de 1
    filterColumns = contentFiltered.sum() == 1
    colsSumFilter = contentFiltered.loc[:, filterColumns]
    basePossibilities = colsSumFilter.columns

    if len(colsSumFilter) == a_rows and colsSumFilter.shape[1] >= a_rows:
        # realizar combinações entre as colunas verificando se a soma das linhas tambem é 1
        for x0 in combinations(basePossibilities, a_rows):
            iPos = colsSumFilter[list(x0)]

            # filtro de linha. cada linha deve somar 1
            if (iPos.sum(axis= 1) == 1).all():
                x0 = iPos.idxmax(axis=1).tolist()
                indexRows = ['z'] + x0
                tableau = tableau.set_axis(indexRows, axis= 0)
                return tableau

    
    else:
        return False

def simplex(A: list, b: list, c: list, x0: list = None):
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
    # A = np.array([
    #     [-2,0,3,1,0,0,0,0],
    #     [2,1,2,0,1,0,0,0],
    #     [0,-1,3,0,0,1,0,0],
    #     [3,3,0,0,0,0,1,0],
    #     [1,-1,-3,0,0,0,0,1]    
    # ])

    # b = np.array([6,7,7,8,9])
    # c = np.array([-2,0,-3])
    # x0 = np.array([4,5,6,7,8])


    # 1. Montar o tableau utilizando x0 como solução inicial
    # isPrepared = False
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

    tableau = pd.DataFrame(
        data= tableau,
        columns= indexCol
    )
    renameZ = {0: 'z'}
    tableau.rename(index= renameZ, inplace= True)
    
    # aqui deve verificar se existe x0. se não existe, tentar identificar a base
    # se nao conseguir, aplicar Big-M
    if not x0:
        baseResult = localizaBaseInicial(tableau)
        
        if baseResult is False:
            tableau = bigM(tableau)
            # isPrepared = True

        else:
            tableau = baseResult
        
        indexRow = tableau.index.tolist()
    
    else:      
        labelBase = ['x' + str(value+1) for value in x0]
        indexRow = ['x' + str(value) for value in x0]
        indexRow.insert(0,'z')
    
        tableau = pd.DataFrame(
            data= tableau,
            index= indexRow,
            columns= indexCol
        )

    print(tableau)
    print('\n')

    dictColumns = {rotulo:indice for indice, rotulo in enumerate(tableau.columns)}

    # 1.5. Colocando o tableau na forma preparada
    if not verificaTableauPreparado(tableau):
        tableau = preparaTableau(tableau)

    print('Tableau preparado:')
    print(tableau)
    print('\n')
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
                print('O problema é ilimitado\n')
                break
            
            tableauCopy = tableau[filterValues].copy()
            
            baseOut = (tableauCopy['LD'] / tableauCopy[baseIn]).idxmin()

            # deixa '1' na celula da nova variavel q entrou
            if tableau.loc[baseOut, baseIn] != 1:
                tableau.loc[baseOut] = tableau.loc[baseOut] / tableau.loc[baseOut, baseIn]

            # transforma a coluna da variavel que entrou em uma coluna da matriz identidade
            indexBaseIn = tableau.columns.get_loc(baseIn)
            for rowIndex in tableau.index:
                if rowIndex != baseOut:
                    pivotValue = tableau.loc[rowIndex, baseIn]
                    if pivotValue != 0:
                        multValue = -pivotValue
                        tableau.loc[rowIndex] = tableau.loc[rowIndex] + (multValue * tableau.loc[baseOut])

            # atualiza o label de linha da variavel q entrou
            tableau.rename(
                index= {baseOut: baseIn},
                inplace= True
            )

            print(f'Iteração {iterations + 1}:')
            print(tableau)
            print('\n')

            # formatando a saida em latex
                # baseFormat = ['c'] * (len(tableau.columns) + 1)
                # baseFormat[0] = 'l'
                # colorCol = f'>{{\\columncolor{{{BASEIN_COLOR}}}}}c' 
                # baseFormat[indexBaseIn] = colorCol
                # latexFormat = ' '.join(baseFormat)

                # latex = tableau.to_latex(
                #     column_format= latexFormat,
                #     booktabs = False,
                #     escape= False
                # )

                # rowColor = f'\\rowcolor{{{BASEOUT_COLOR}}}'
                
                # latex = latex.replace(
                #     baseOut,
                #     f'\n{rowColor} {baseOut}'
                # )

A = [mt.A1, mt.A2, mt.A3, mt.A4, mt.A5, mt.A6]
b = [mt.b1, mt.b2, mt.b3, mt.b4, mt.b5, mt.b6]
c = [mt.c1, mt.c2, mt.c3, mt.c4, mt.c5, mt.c6]
x0 = [mt.base1, mt.base2, mt.base3, mt.base4, mt.base5, mt.base6]

for i in range(len(A)):
    simplex(
        A= A[i],
        b= b[i],
        c= c[i]
    )
