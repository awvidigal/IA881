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

# simetria = np.array_equal(redeOticaNaoOrientada, redeOticaNaoOrientada.T)

mapaEUA = mapaEUA.fillna(0)
mapaEUA = mapaEUA.astype(int)
mapaEUA = mapaEUA.values
mapaEuaNaoOrientado = mapaEUA

for indice, valor in np.ndenumerate(mapaEUA):
    if valor:
        mapaEuaNaoOrientado[indice[1],indice[0]] = valor

# simetria = np.array_equal(mapaEuaNaoOrientado, mapaEuaNaoOrientado.T)


# italianaOtica = [
#     [0,140,110,210,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [0,0,110,0,0,95,90,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,90,0,0,95,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,85,0,0,0,0,0,210,0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,230,0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,90,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,130,150,120,0,0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,55,0,200,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,60,110,180,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,190,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,190,0,130,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,120,170,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,180,0,460,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,200,270,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,210,0,90,0,310,350],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,100,250,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,420,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,200,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,210],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,150],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
# ]

