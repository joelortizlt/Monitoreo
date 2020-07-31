import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import funciones as f
from InputsNoRevolvente import InputsNoRevolvente

#lista_nombres=['CEF','PymeCT','PymeAF']
lista_nombres=['CHIP','GAHI','MiViv','VEH']
#ruta_real=['/Users/renzomartinch/Downloads/Comite_0622/CEFCB_Reales.csv','/Users/renzomartinch/Downloads/Comite_0622/PymeCT_Reales.csv','/Users/renzomartinch/Downloads/Comite_0622/PymeAF_Reales.csv']
ruta_real=['/Users/renzomartinch/Downloads/Comite_0622/Hipot_Reales.csv','/Users/renzomartinch/Downloads/Comite_0622/Gahi_Reales.csv','/Users/renzomartinch/Downloads/Comite_0622/MiVivienda_Reales.csv','/Users/renzomartinch/Downloads/Comite_0622/Vehicular_Reales.csv']
#ruta_teorico=['/Users/renzomartinch/Downloads/Comite_0622/CEFCB_Inputs.csv','/Users/renzomartinch/Downloads/Comite_0622/PymeNR_Inputs.csv','/Users/renzomartinch/Downloads/Comite_0622/PymeNR_Inputs.csv']
ruta_teorico=['/Users/renzomartinch/Downloads/Comite_0622/Hipot_Inputs.csv','/Users/renzomartinch/Downloads/Comite_0622/Gahi_Inputs.csv','/Users/renzomartinch/Downloads/Comite_0622/MiVivienda_Inputs.csv','/Users/renzomartinch/Downloads/Comite_0622/Vehicular_Inputs.csv']
#ruta_tmin=['/Users/renzomartinch/Downloads/Comite_0622/CEFCB_Precios.csv','/Users/renzomartinch/Downloads/Comite_0622/PymeNR_Precios.csv','/Users/renzomartinch/Downloads/Comite_0622/PymeNR_Precios.csv']
ruta_tmin=['/Users/renzomartinch/Downloads/Comite_0622/Hipot_Precios.csv','/Users/renzomartinch/Downloads/Comite_0622/Gahi_Precios.csv','/Users/renzomartinch/Downloads/Comite_0622/MiVivienda_Precios.csv','/Users/renzomartinch/Downloads/Comite_0622/Vehicular_Precios.csv']
lista_cortes=[[],['C_PLAZO'],['C_SEGMENTO'],['C_MONEDA']]#,['C_RANGOSCORE']]
lista_cortes_Pyme=[[],['C_PLAZO'],['C_PRODUCTO'],['C_MONEDA'],['C_RANGOPD']]

for i in range(len(lista_nombres)):
    REAL = pd.read_csv(ruta_real[i], encoding='latin-1')
    TEORICO = pd.read_csv(ruta_teorico[i])
    TMIN = pd.read_csv(ruta_tmin[i])
    product = InputsNoRevolvente(REAL,TEORICO,mincosecha=201801,maxcosecha=201912)
    
    for j in range(len(lista_cortes)):

        print(lista_nombres[i],j)

        if lista_nombres[i]=='PymeCT' or lista_nombres[i]=='PymeAF':
            cortes = lista_cortes_Pyme[j]
        else:
            cortes = lista_cortes[j]
        product.condensar(cortes)
        product.optimizar()
        product.impactoTmin(TMIN)#,impactoTIR=True)

        temp = pd.concat([product.promedios,product.stats,product.Tmin,product.curvas], axis=1) #don't forget: product.TIR
        name=temp.columns[0]
        temp.rename(columns={name:"CORTE"}, inplace=True)
        if i==0 and j==0:
            imprimir = temp
        else:
            imprimir = imprimir.append(temp,ignore_index=True)

print(imprimir)
imprimir.to_excel("plancha.xlsx")