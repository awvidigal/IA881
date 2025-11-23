import numpy as np
import entradasGrafos as eg
from algoritmosGrafos import dijkstra, bellmanFord 
from entradasGrafos import mapaEUA, redeOtica

saidasRede = [7,14,21]
saidasMapa = [10, 20, 30, 40, 50, 60, 70]

print ('# ########################## DIJKSTRA #############################')

acm, dp = dijkstra(redeOtica)
print('\nRede Otica')
print('____ _____\n')
for valor in saidasRede:
    print(f'Nó: {valor}')
    print(f'dist[{valor}]: {dp[valor-1,0]} | prev[{valor}]: {dp[valor-1,1]}\n')

acm, dp = dijkstra(mapaEUA)
print('\nMapa Rodoviario')
print('____ __________\n')
for valor in saidasMapa:
    print(f'Nó: {valor}')
    print(f'dist[{valor}]: {dp[valor-1,0]} | prev[{valor}]: {dp[valor-1,1]}\n')


print ('# ########################## BELLMAN-FORD #############################')

acm, dp = bellmanFord(redeOtica)
print('\nRede Otica')
print('____ _____\n')
for valor in saidasRede:
    print(f'Nó: {valor}')
    print(f'dist[{valor}]: {dp[valor-1,0]} | prev[{valor}]: {dp[valor-1,1]}\n')

acm, dp = dijkstra(mapaEUA)
print('\nMapa Rodoviario')
print('____ __________\n')
for valor in saidasMapa:
    print(f'Nó: {valor}')
    print(f'dist[{valor}]: {dp[valor-1,0]} | prev[{valor}]: {dp[valor-1,1]}\n')