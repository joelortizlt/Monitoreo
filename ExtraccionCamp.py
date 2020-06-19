import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import funciones as f
from InputsNoRevolvente import InputsNoRevolvente

lista_nombres=['Campanas']
ruta_real=['/Users/renzomartinch/Downloads/Comite_0622/Campanas_Reales.csv']
ruta_teorico=['/Users/renzomartinch/Downloads/Comite_0622/Campanas_Inputs.csv']
ruta_tmin=['/Users/renzomartinch/Downloads/Comite_0622/Campanas_Precios.csv']
lista_cortes=[[],['C_PLAZO'],['C_CAMPANIA'],['C_GRACIA']]

for i in range(len(lista_nombres)):
    REAL = pd.read_csv(ruta_real[i], encoding='latin-1')
    TEORICO = pd.read_csv(ruta_teorico[i])
    TMIN = pd.read_csv(ruta_tmin[i])
    product = InputsNoRevolvente(REAL,TEORICO,mincosecha=201801,maxcosecha=201912)
    
    for j in range(len(lista_cortes)):

        print(lista_nombres[i],j)

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
imprimir.to_excel("plancha4.xlsx")