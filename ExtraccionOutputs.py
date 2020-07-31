import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import funciones as f
from OutputsNoRevolvente import OutputsNoRevolvente

lista_nombres=['Hipot','GAHI','MiViv','VEH','CEF','Pyme']
ruta_real=['/Users/renzomartinch/Downloads/SeguimientoJulio/Hipot_Reales.csv','/Users/renzomartinch/Downloads/SeguimientoJulio/Gahi_Reales.csv','/Users/renzomartinch/Downloads/SeguimientoJulio/MiVivienda_Reales.csv','/Users/renzomartinch/Downloads/SeguimientoJulio/Vehicular_Reales.csv','/Users/renzomartinch/Downloads/SeguimientoJulio/Cef_Reales.csv','/Users/renzomartinch/Downloads/SeguimientoJulio/Pyme_Reales.csv']
ruta_teorico=['/Users/renzomartinch/Downloads/SeguimientoJulio/Hipot_Inputs.csv','/Users/renzomartinch/Downloads/SeguimientoJulio/Gahi_Inputs.csv','/Users/renzomartinch/Downloads/SeguimientoJulio/MiVivienda_Inputs.csv','/Users/renzomartinch/Downloads/SeguimientoJulio/Vehicular_Inputs.csv','/Users/renzomartinch/Downloads/SeguimientoJulio/Cef_Inputs.csv','/Users/renzomartinch/Downloads/SeguimientoJulio/Pyme_Inputs.csv']
lista_cortes=[['C_SEGMENTO'],['C_SEGMENTO'],['C_PLAZO'],['C_PLAZO'],['C_PLAZO'],['C_PRODUCTO']]

for i in range(len(lista_nombres)):
    print(lista_nombres[i])

    REAL = pd.read_csv(ruta_real[i])
    TEORICO = pd.read_csv(ruta_teorico[i])
    product = OutputsNoRevolvente(REAL,TEORICO,mincosecha=201801)
    
    for j in range(2):
        print(lista_nombres[i],j)

        if j==0:
            cortes = []
        else:
            cortes = lista_cortes[i]
        product.condensar(cortes)

        temp = pd.concat([product.ratios,product.niveles,product.curvas], axis=1) #don't forget: product.TIR
        name=temp.columns[0]
        temp.rename(columns={name:"CORTE"}, inplace=True)
        if i==0 and j==0:
            imprimir = temp
        else:
            imprimir = imprimir.append(temp,ignore_index=True)

print(imprimir)
imprimir.to_excel("plancha.xlsx")