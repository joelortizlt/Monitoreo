import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import funciones as f
from InputsRevolvente import InputsRevolvente

lista_nombres=['TSN']
ruta_real=['/Users/renzomartinch/Downloads/Comite_0622/TSN_Reales.csv']
ruta_teorico=['/Users/renzomartinch/Downloads/Comite_0622/TSN_Inputs.csv']
ruta_tmin=['/Users/renzomartinch/Downloads/Comite_0622/TSN_Precios.csv']
lista_cortes=[[],['C_LINEA'],['C_SUBSEGMENTO'],['C_PD']]

for i in range(len(lista_nombres)):
    REAL = pd.read_csv(ruta_real[i])
    TEORICO = pd.read_csv(ruta_teorico[i])
    TMIN = pd.read_csv(ruta_tmin[i])
    product = InputsRevolvente(REAL,TEORICO,mincosecha=201901,maxcosecha=201912)
    
    for j in range(len(lista_cortes)):
        cortes = lista_cortes[j]
        product.condensar(cortes)
        product.optimizar()
        product.impactoTmin(TMIN,impactoTIR=True)

        temp = pd.concat([product.promedios,product.stats,product.Tmin,product.TIR,product.curvas], axis=1)
        name=temp.columns[0]
        temp.rename(columns={name:"CORTE"}, inplace=True)
        if i==0 and j==0:
            imprimir = temp
        else:
            imprimir = imprimir.append(temp,ignore_index=True)

print(imprimir)
imprimir.to_excel("plancha3.xlsx")