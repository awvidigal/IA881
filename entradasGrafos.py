import numpy as np
import pandas as pd

mapaEUA = pd.read_csv(
    'mapa_rodoviario_eua.csv',
    delimiter= ';',
    header= None
)

redeOtica = pd.read_csv(
    'rede_otica_italia.csv',
    sep= ';',
    header= None
)

redeOtica = redeOtica.fillna(0)
redeOtica = redeOtica.astype(int)
redeOtica = redeOtica.values
redeOticaNaoOrientada = redeOtica

for indice, valor in np.ndenumerate(redeOtica):
    if valor:
        redeOticaNaoOrientada[indice[1],indice[0]] = valor

mapaEUA = mapaEUA.fillna(0)
mapaEUA = mapaEUA.astype(int)
mapaEUA = mapaEUA.values
mapaEuaNaoOrientado = mapaEUA

for indice, valor in np.ndenumerate(mapaEUA):
    if valor:
        mapaEuaNaoOrientado[indice[1],indice[0]] = valor



