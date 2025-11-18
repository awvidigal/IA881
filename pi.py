from algoritmosPI import PAE, DAE, PDAE

import numpy as np

M = 1000

# A = [0.5, 1, 1]
# c = [-90, -150, 0]
# b = 3

# A = [1, 1]
# b = [1]
# c = [-2, 1]

A = [
    [1,0,0,1/4,-8,-1,10],
    [0,1,0,1/2,-12,-1/2,3],
    [0,0,1,0,0,1,0]
]

c = [0,0,0,-3/4,22,-1/2,5]
b = [0,0,1]

solucao = PAE(A, b, c)
otimo = [lista[-1] if lista else 0 for lista in solucao]

x = otimo[0][:-1]
sigmaC = otimo[1]
sigmaD = otimo[2]
solucaoOtima = -otimo[3]

xOtimo = enumerate(x)

print('Solução Algoritmo PAE')
for item in xOtimo:
    print(f'x{item[0]}: {item[1]}')

print(f'sigmaC: {sigmaC}')
print(f'sigmaD: {sigmaD}')
print(f'Solucao ótima: {solucaoOtima}')
print(' ')

solucao = DAE(A, b, c, [-250], [35,100,250])
otimo = [lista[-1] for lista in solucao]
s = otimo[0]
w = otimo[1]
x = otimo[2]
sigmaC = otimo[3]
solucaoOtima = otimo[4]

sOtimo = enumerate(s)
wOtimo = enumerate(w)
xOtimo = enumerate(x)

print('Solução algoritmo DAE')
for item in sOtimo:
    print(f's{item[0]}: {item[1]}')

for item in wOtimo:
    print(f'w{item[0]}: {item[1]}')

for item in xOtimo:
    print(f'x{item[0]}: {item[1]}')

print(f'SigmaC: {sigmaC}')
print(f'Solucao ótima: {solucaoOtima}')