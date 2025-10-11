from re import X
import numpy as np

M = 1000

def PAE(A, b, c, epsilon = 1e-3, alfa = 0.95):
    '''
    Função que executa o algoritmo Primal Afim Escala para otimização do problema de otimização
    
    min c'x
    s.a. Ax = b
    x >= 0

    Utilizando o método de pontos interiores.
    
    Parâmetros
    ----------
    A: 
        matriz relacionada às restrições

    b: 
        vetor de igualdade das restrições

    c: 
        vetor de coeficientes da função objetivo

    epsilon: 
        valor de precisão que define qual a tolerância para entender se chegamos na solução ótima

    alfa: 
        limitador de passo

    Retorno
    -------
    x:
        vetor que contem os valores das variáveis de x1 a xn

    sigmaC:
        teste de folga complementar

    sigmaD:
        teste de factibilidade dual

    solucao:
        valor ótimo encontrado
    '''

    A = np.array(A)
    b = np.array(b)
    c = np.array(c)

    if A.ndim == 1:
        A = A.reshape(1, -1)

    e = np.ones(A.shape[1])
    
    k = 0

    x = []
    w = []
    r = []
    d = []
    sigmaD  = []
    sigmaC  = []
    solucao = []

    retorno = [x, sigmaC, sigmaD, solucao]

    # 1. Reformular para encontrar sol. inicial factível usando big-M
    # 1.2. Alterando os vetores A e c
    c = np.append(c, M)
    c = c.reshape(-1,1)

    apendiceA = b - A@e
    A = np.append(A, apendiceA.reshape(-1, 1), axis= 1)  

    # 1.3. Inicializando os valores de x com 1
    x.append(np.ones(shape= A.shape[1]))
    
    b = b.reshape(-1,1)  

    while True:
        # 2. Calcular as estimativas duais como: wk = (AXk²AT)^-1 * AXk²c    
        # 2.1. Cálculo de Xk
        X = np.diag(x[k])
        X2 = np.diag(x[k]**2)
        # 2.2. Cálculo de wk
        w.append(
            np.linalg.inv(A@(X@X)@(A.T)) @ A@(X@X)@c
        )

        # 3. Calcular os custos reduzidos rk = c-AT*wk
        r.append(
            c - (A.T@w[k])
        )

        # 4. Verificar se os testes defolga complementar e de factibilidade dual estao dentro da tolrancia epsilon
        # 4.1. Verificando valores não negativos em r
        rNeg = []
        cNeg = []
        # rPosIndex = [
        #     (indice, valor)
        #     for indice, valor in enumerate(r[k])
        #     if valor > 0
        # ]

        rNegIndex = []
        # teste = enumerate(r[k])
        # for item in teste:
        #     print(item)
        for indice, valor in enumerate(r[k]):
            if valor < 0:
                rNegIndex.append([indice, valor]) 

        if not rNegIndex:
            break # o que acontece se for tudo positivo? problema infactivel?

        else:
            rNeg = [valor[1] for valor in rNegIndex]
            cNeg = [c[valor[0]].item() for valor in rNegIndex]
        
        # 4.1. Testando a factibilidade dual
        rNeg = np.array(rNeg)
        cNeg = np.array(cNeg)
        sigmaD.append(
            np.linalg.norm(rNeg, ord=1) / (np.linalg.norm(cNeg) + 1)
        )

        # 4.2. Testando a folga complementar
        solucao.append(c.T @ x[k].reshape(-1,1))
        sigmaC.append(
            abs(solucao[k] - (b @ w[k]))
        )

        if sigmaC[k] < epsilon and sigmaD[k] < epsilon:
            return retorno
        
        # 5. Calcular a direção de caminhada como dky = -Xk*rk
        else:
            d.append(-X @ r[k])

        # 6. Verifica se dky é menor do que zero
        if (d[k] >= 0).all():
            for value in d[k]:
                print(value)
            print('Solucao ilimitada ou existem múltiplas solucoes')
            return retorno
        
        # 7. Determina o tamanho do passo como sendo alfak
        else:
            dPos = [valor for valor in d[k] if valor < 0]
            dPos = np.array(dPos)
            alfak = min(alfa / (-dPos))

        # 8. Atualizar a solução final (valores das variáveis)
        # x = np.append(x, x[k] + alfak * X @ d[k])
        x.append(x[k] + alfak * X @ d[k].flatten())
        k += 1  

        if k == 100:
            print('Deu erraduuuu')
            return retorno
        
def DAE(A, b, c, w0, s0, epsilon = 1e-3, alfa = 0.95):
    '''
    Função que executa o algoritmo Dual Afim Escala para otimização do problema de otimização
    
    min c'x
    s.a. Ax = b
    x >= 0

    Utilizando o método de pontos interiores.
    
    Parâmetros
    ----------
    A: 
        matriz relacionada às restrições

    b: 
        vetor de igualdade das restrições

    c: 
        vetor de coeficientes da função objetivo

    w0:
        solucao inicial factivel w

    s0:
        solucao incial factivel s

    epsilon: 
        valor de precisão que define qual a tolerância para entender se chegamos na solução ótima

    alfa: 
        limitador de passo

    Retorno
    -------
    s:
        vetor que contem os valores das variáveis de s1 a sn

    sigmaC:
        teste de folga complementar

    solucao:
        valor ótimo da função objetivo
    '''  
    # 1. Preparação do problema
    A = np.array(A)
    b = np.array(b)
    c = np.array(c)
    
    if A.ndim == 1:
        A = A.reshape(1, -1)

    k = 0
    dw  = []
    ds  = []
    x   = []
    sigmaC = []
    # 1.1. Formular o problema dual
    # 1.1.1. Inicializando os vetores w e s com a solucao inicial factivel
    w = np.array(w0)
    s = np.array(s0)

    solucao = [w,s]
    retorno = [s, sigmaC, solucao]

    # 2. Inicio das iterações
    while True:
        # 2.1. Calcular as direcoes dw[k] = (AS[k]^-2)^-1@b e ds[k] = -A.T@dw[k]
        S = np.diag(s)
        SInv2 = np.linalg.inv(S)@np.linalg.inv(S)
        dw.append(
            np.linalg.inv(A@SInv2@A.T)@b
        )

        ds.append(
            -A.T@dw[k]
        )

        # 2.2. Verificar se ds[k] >=0. Dual ilimitado, caso sim
        if (ds[k] >= 0).all():
            print('Problema dual ilimitado ou múltiplas soluções ótimas')
            return retorno
        
        # 2.3. Calcular a estimativa primal x[k] = -S[k]^-2@ds[k]
        x.append(
            -SInv2@ds[k]
        )

        # 2.4. Verificar se x[k] >= 0 e sigmaC <= epsilon. Condição de parada
        if x[k] >= 0 and sigmaC <= epsilon:
            print('Solucão ótima encontrada')
            return retorno
        
        # 2.5. Determinar o tamanho do passo betaK
        betaK = min(alfa)
        
        # 2.6. Atualizar a solução (w[k+1], s[k+1])

    
    pass

def PDAE(A, b, c, epsilon = 1e-3, alfa = 0.95):
    
    pass