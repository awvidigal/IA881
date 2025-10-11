import numpy as np
import pandas as pd
import matrizes as mt

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

A = [0.5, 1, 1]
c = [-90, -150, 0]
b = 3

solucao = PAE(A, b, c)
otimo = [lista[-1] for lista in solucao]

x = otimo[0][:-1]
sigmaC = otimo[1]
sigmaD = otimo[2]
solucaoOtima = -otimo[3]

xOtimo = enumerate(x)
for item in xOtimo:
    print(f'x{item[0]}: {item[1]}')

print(f'sigmaC: {sigmaC}')
print(f'sigmaD: {sigmaD}')
print(f'Solucao ótima: {solucaoOtima}')