from algoritmosGrafos import prim, kruskal, matrizTesteAGM
from entradasGrafos import mapaEUA, redeOtica


agm, custoArvore, iteracoes, execucao = kruskal(matrizTesteAGM)
agm, custoArvore, iteracoes, execucao = prim(redeOtica)


print ('# ########################## PRIM #############################')
print('\nRede Otica')
print('____ _____\n')

print('Arcos:')
for indice,valor in enumerate(agm):
    print(f'({valor[0]},{valor[1]})')

print('\n')

print(f'Custo total da arvore: {custoArvore}\n')
print(f'Tempo de execução: {execucao:.6f} segundos')
print(f'Quantidade de iterações: {iteracoes}')

