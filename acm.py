from algoritmosGrafos   import dijkstra, bellmanFord 
from entradasGrafos     import mapaEUA, redeOtica

saidasRede = [7,14,21]
saidasMapa = [10, 20, 30, 40, 50, 60, 70]

print ('# ########################## DIJKSTRA #############################')

acm, dp, tempo, iteracoes, relaxacoes = dijkstra(redeOtica)
print('\nRede Otica')
print('____ _____\n')

print(f'Tempo de execução: {tempo:.6f} segundos')
print(f'Quantidade de iterações: {iteracoes}')
print(f'Quantidade de relaxações: {relaxacoes}\n')
for valor in saidasRede:
    print(f'Nó: {valor}')
    print(f'dist[{valor}]: {dp[valor-1,0]} | prev[{valor}]: {dp[valor-1,1]}\n')

acm, dp, tempo, iteracoes, relaxacoes = dijkstra(mapaEUA)
print('\nMapa Rodoviario')
print('____ __________\n')

print(f'Tempo de execução: {tempo:.6f} segundos')
print(f'Quantidade de iterações: {iteracoes}')
print(f'Quantidade de relaxações: {relaxacoes}\n')
for valor in saidasMapa:
    print(f'Nó: {valor}')
    print(f'dist[{valor}]: {dp[valor-1,0]} | prev[{valor}]: {dp[valor-1,1]}\n')


print ('# ########################## BELLMAN-FORD #############################')

acm, dp, tempo, iteracoes, relaxacoes = bellmanFord(redeOtica)
print('\nRede Otica')
print('____ _____\n')

print(f'Tempo de execução: {tempo:.6f} segundos')
print(f'Quantidade de iterações: {iteracoes}')
print(f'Quantidade de relaxações: {relaxacoes}\n')
for valor in saidasRede:
    print(f'Nó: {valor}')
    print(f'dist[{valor}]: {dp[valor-1,0]} | prev[{valor}]: {dp[valor-1,1]}\n')

acm, dp, tempo, iteracoes, relaxacoes = dijkstra(mapaEUA)
print('\nMapa Rodoviario')
print('____ __________\n')

print(f'Tempo de execução: {tempo:.6f} segundos')
print(f'Quantidade de iterações: {iteracoes}')
print(f'Quantidade de relaxações: {relaxacoes}\n')
for valor in saidasMapa:
    print(f'Nó: {valor}')
    print(f'dist[{valor}]: {dp[valor-1,0]} | prev[{valor}]: {dp[valor-1,1]}\n')