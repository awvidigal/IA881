from algoritmosPI import PAE, DAE, PDAE

import numpy as np

M = 1000

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

print('Solução Algoritmo PAE')
print(f'sigmaC: {sigmaC}')
print(f'sigmaD: {sigmaD}')
print(f'Solucao ótima: {solucaoOtima}')

solucao = DAE(A, b, c,)
otimo = [lista[-1] for lista in solucao]