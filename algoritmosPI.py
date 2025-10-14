from ctypes.wintypes import DWORD
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
            np.linalg.inv(A@X2@(A.T)) @ A@X2@c
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
            print('Problema ilimitado ou com múltiplas soluções ótimas')
            return retorno

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
        
def DAE(A, b, c, w0 = [], s0 = [], epsilon = 1e-3, alfa = 0.95):
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

    w:
        vetor que contem os valores das variaveis de w1 a wn

    x:
        vetor de estimativas primais

    sigmaC:
        teste de folga complementar

    solucaoOtima:
        valor da função objetivo no ponto ótimo

    '''  
    # 1. Preparação do problema
    A = np.array(A)
    b = np.array(b).reshape(-1,1)
    c = np.array(c)
    
    if A.ndim == 1:
        A = A.reshape(1, -1)

    k = 0
    dw  = []
    ds  = []
    x   = []
    sigmaC = []
    solucaoOtima = []
    # 1.1. Formular o problema dual
    # 1.1.1. Inicializando os vetores w e s com a solucao inicial factivel
    if not w0 or not s0:
        w0, s0 = solucaoInicialDAE(A, b, c)
    
    w = [np.array(w0)]
    s = [np.array(s0)]

    solucao = [w,s]
    retorno = [s, sigmaC, solucao]

    # 2. Inicio das iterações
    while True:
        # 2.1. Calcular as direcoes dw[k] = (AS[k]^-2)^-1@b e ds[k] = -A.T@dw[k]
        S = np.diag(s[k])
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
            return s, w, x, sigmaC
        
        # 2.3. Calcular a estimativa primal x[k] = -S[k]^-2@ds[k] e o gap de dualidade
        x.append(
            -SInv2@ds[k]
        )

        sigmaC.append(
            c@x[k] - b.reshape(1,-1)@w[k]
        )

        # 2.4. Verificar se x[k] >= 0 e sigmaC <= epsilon. Condição de parada
        if (x[k] >= 0).all() and sigmaC[k] <= epsilon:
            print('Solucão ótima encontrada')
            return s, w, x, sigmaC, solucaoOtima
        
        # 2.5. Determinar o tamanho do passo betaK
        dsNegIndex = [[indice, valor] for indice, valor in enumerate(ds[k]) if valor < 0]
        dsNeg = [valor[1] for valor in dsNegIndex]
        siNeg = [s[k][indice[0]].item() for indice in dsNegIndex]

        dsNeg = np.array(dsNeg)
        siNeg = np.array(siNeg)

        betaK = np.min(alfa*(siNeg/-dsNeg))

        # 2.6. Atualizar a solução (w[k+1], s[k+1])
        w.append(w[k] + betaK * dw[k])
        s.append(s[k] + betaK * ds[k].flatten())
        # w = np.append(w, w[k] + betaK * dw[k])
        # s = np.append(s, s[k] + betaK * ds[k])
        solucaoOtima.append(b.T@w[k])

        k += 1

def solucaoInicialDAE(A, b, c, epsilon = 1e-3, alfa = 0.95):
    '''
    Função que busca o valor inicial factível para o algoritmo DAE utilizando a técnica do Big-M
        
    min c'x         !->  max b'w             !->  max b'w + Mwa
    s.a. Ax = b     !->  s.a. A'w + s = c    !->  s.a. A'w + pwa + s = c
    x >= 0          !->  s >= 0              !->  s >= 0

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
    w0:
        solução inicial factível para w

    s0:
        solução inicial factível para s
    '''

    A = np.array(A)
    b = np.array(b)
    c = np.array(c)

    # 1. Preparação
    # 1.1. Alterando o vetor b para incluir o bigM
    b = np.append(b, M)

    # 1.2. Criando o vetor p
    p = [1 if valor <= 0 else 0 for valor in c]

    # 1.3. Inicializando vetor w0
    w0 = np.zeros(shape= A.shape[0] + 1)

    # 1.4. Definindo variavel artificial inicial
    cBarra = np.max(np.abs(c))
    teta = 2
    w0[-1] = -teta*cBarra

    # 1.5. Variaveis de folga iniciais
    s   = np.zeros(shape= c.shape)
    s0  = c + teta*cBarra*p

    # 2. Executa DAE
    s0, w0, _, _, _ = DAE(A, b, c, w0, s0)

    return [w0,s0]

def PDAE(A, b, c, x0 = [], w0 = [], s0 = [], epsilon = 1e-3, alfa = 0.99, sigmaMu = 0.85):
    '''
    Função que busca o valor inicial factível para o algoritmo PDAE
        
    min c'x         
    s.a. Ax = b
    x >= 0

    Parâmetros
    ----------
    A: 
        matriz relacionada às restrições

    b: 
        vetor de igualdade das restrições

    c: 
        vetor de coeficientes da função objetivo

    x0:
        solução inicial para x

    w0:
        solução inicial para w

    s0:
        solução inicial para s
    
    epsilon: 
        valor de precisão que define qual a tolerância para os critérios de parada

    alfa: 
        limitador de passo

    sigmaMu:
        limitador da penalidade associada a barreira logarítmica

    Retorno
    -------
    x:
        valores ótimos de x

    w:
        valores ótimos de w

    mu:
        valore ótimo de mu
    
    sigmaP:
        factibilidade primal

    sigmaD:
        fatibilidade dual

    solPrimal:
        solucão ótima primal

    solDual:
        solução ótima dual
    '''

    # 1. Preparação do problema
    A = np.array(A)
    b = np.array(b)
    c = np.array(c)

    if A.ndim == 1:
        A = A.reshape(1, -1)

    k = 0

    mu  = []
    t   = []
    u   = []
    v   = []
    p   = []
    dx  = []
    dw  = []
    ds  = []

    sigmaP = []
    sigmaD = []

    n = c.size

    if not x0:
        x0 = np.ones(shape= c.shape)

    if not w0:
        w0 = np.zeros(shape= c.shape)

    if not s0:
        s0 = np.ones(shape= c.shape)

    e = np.ones(shape= x.shape)
    
    x = np.array[[x0]]
    w = np.array[[w0]]
    s = np.array[[s0]]
    
    # 2. Início das iterações
    while True:    
        # 2.1. Calculando:
        X = np.diag(x[k])
        S = np.diag(s[k])
        
        # 2.1.1. mu[k] = sigmaMu(x[k]).T s[k]/n  (n é o tamanho de x = tamanho de c)
        mu.append(
            (sigmaMu@x[k].reshape(1,-1)@s[k].reshape(-1,1))/n
        )
        
        # 2.1.2. t[k] = b - Ax[k]
        t.append(
            b - A@x[k]
        )

        # 2.1.3. u[k] = c - A.Tw[k] - s[k]
        u.append(
            c - A.T@w[k] - s[k]
        )
        
        # 2.1.4. v[k] = mu[k]e - XSe
        v.append(
            mu[k]@e - X@S@e
        )

        # 2.1.5. p[k] = X^-1v[k]
        p.append(
            np.linalg.inv(X)@v[k]
        )

        # 2.2. Factibilidades
        # 2.2.1. Primal: sigmaP = norm(t) / (norm(b) + 1)
        sigmaP.append(
            np.linalg.norm(t[k], ord=1)
        )

        # 2.2.2. Dual: sigmaD = norm(u) / (norm(c) + 1)
        # 2.3. Comparar mu[k] e as factibilidades com o valor de epsilon
        # 2.4. Calcular as direçoes dx dw e ds
        # 2.5. Verificar a factibilidade do problema primal
        # 2.6. Calcular os passos betaP e betaD
        # 2.7. Atualização das soluções

        k += 1
