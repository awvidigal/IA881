import numpy as np
import pandas as pd
import matrizes as mt

def PAE(A, b, c, epsilon, alfa):
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

    # 1. Reformular para enontrar sol. inicial factível usando big-M
    # 2. Calcular as estimativas duais como: wk = (AXk²AT)^-1 * AXk²c
    # 3. Calcular os custos reduzidos rk = c-AT*wk
    # 4. Verificar se os testes defolga complementar e de factibilidade dual estao dentro da tolrancia epsilon
    # 5. Calcular a direção de caminhada como dky = -Xk*rk
    # 6. Verifica se dky é menor do que zero
    # 7. Determina o tamanho do passo como sendo alfak
    # 8. Atualizar a solução final 