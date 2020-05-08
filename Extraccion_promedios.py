import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import funciones as f
from InputsNoRevolvente import InputsNoRevolvente

lista_nombres=['CEF','CHIP','GAHI','MiViv','VEH','PymeCT','PymeAF']
ruta_real=['/Users/renzomartinch/Downloads/Comite_1105/CEFCB_Reales.csv','/Users/renzomartinch/Downloads/Comite_1105/Hipot_Reales.csv','/Users/renzomartinch/Downloads/Comite_1105/Gahi_Reales.csv','/Users/renzomartinch/Downloads/Comite_1105/MiVivienda_Reales.csv','/Users/renzomartinch/Downloads/Comite_1105/Vehicular_Reales.csv','/Users/renzomartinch/Downloads/Comite_1105/PymeCT_Reales.csv','/Users/renzomartinch/Downloads/Comite_1105/PymeAF_Reales.csv']
ruta_teorico=['/Users/renzomartinch/Downloads/Comite_1105/CEFCB_Inputs.csv','/Users/renzomartinch/Downloads/Comite_1105/Hipot_Inputs.csv','/Users/renzomartinch/Downloads/Comite_1105/Gahi_Inputs.csv','/Users/renzomartinch/Downloads/Comite_1105/MiVivienda_Inputs.csv','/Users/renzomartinch/Downloads/Comite_1105/Vehicular_Inputs.csv','/Users/renzomartinch/Downloads/Comite_1105/PymeNR_Inputs.csv','/Users/renzomartinch/Downloads/Comite_1105/PymeNR_Inputs.csv']
ruta_tmin=['/Users/renzomartinch/Downloads/Comite_1105/CEFCB_Precios.csv','/Users/renzomartinch/Downloads/Comite_1105/Hipot_Precios.csv','/Users/renzomartinch/Downloads/Comite_1105/Gahi_Precios.csv','/Users/renzomartinch/Downloads/Comite_1105/MiVivienda_Precios.csv','/Users/renzomartinch/Downloads/Comite_1105/Vehicular_Precios.csv','/Users/renzomartinch/Downloads/Comite_1105/PymeNR_Precios.csv','/Users/renzomartinch/Downloads/Comite_1105/PymeNR_Precios.csv']

for i in range(len(lista_nombres)):
    REAL = pd.read_csv(ruta_real[i])
    TEORICO = pd.read_csv(ruta_teorico[i])
    TMIN = pd.read_csv(ruta_tmin[i])
    product = InputsNoRevolvente(REAL,TEORICO,completar=True)
    product.condensar([])
    product.optimizar()
    product.impactoTmin(TMIN,completar=True)

    temp = pd.concat([product.promedios,product.stats,product.Tmin], axis=1)

    if i==0:
        imprimir = temp
    else:
        imprimir = imprimir.append(temp)

print(imprimir)
imprimir.to_excel("productos.xlsx")
