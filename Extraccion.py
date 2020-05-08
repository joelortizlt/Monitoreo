import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import funciones as f
from InputsNoRevolvente import InputsNoRevolvente

lista_nombres=['CEF']#,'CHIP','GAHI','MiViv','VEH','PymeNR']
ruta_real=['/Users/renzomartinch/Downloads/CEFCB/CEFCB_Reales.csv']#,'/Users/renzomartinch/Downloads/CHIP/Hipot_Reales.csv','/Users/renzomartinch/Downloads/GAHI/Gahi_Reales.csv','/Users/renzomartinch/Downloads/MiVivienda/MiVivienda_Reales.csv','/Users/renzomartinch/Downloads/VEH/Vehicular_Reales.csv','/Users/renzomartinch/Downloads/PymeNR/PymeNR_Reales.csv']
ruta_teorico=['/Users/renzomartinch/Downloads/CEFCB/CEFCB_Inputs.csv']#,'/Users/renzomartinch/Downloads/CHIP/Hipot_Inputs.csv','/Users/renzomartinch/Downloads/GAHI/Gahi_Inputs.csv','/Users/renzomartinch/Downloads/MiVivienda/MiVivienda_Inputs.csv','/Users/renzomartinch/Downloads/VEH/Vehicular_Inputs.csv','/Users/renzomartinch/Downloads/PymeNR/PymeNR_Inputs.csv']
ruta_tmin=['/Users/renzomartinch/Downloads/CEFCB/CEFCB_Precios.csv']#,'/Users/renzomartinch/Downloads/CHIP/Hipot_Precios.csv','/Users/renzomartinch/Downloads/GAHI/Gahi_Precios.csv','/Users/renzomartinch/Downloads/MiVivienda/MiVivienda_Precios.csv','/Users/renzomartinch/Downloads/VEH/Vehicular_Precios.csv','/Users/renzomartinch/Downloads/PymeNR/PymeNR_Precios.csv']
lista_cortes=[[],['C_PLAZO'],['C_SEGMENTO'],['C_MONEDA'],['C_MALAVENTA']]
lista_cortes_Pyme=[[],['C_PLAZO'],['C_PRODUCTO'],['C_MONEDA'],['C_MALAVENTA']]

for i in range(1):
    REAL = pd.read_csv(str(ruta_real[i]))
    TEORICO = pd.read_csv(ruta_teorico[i])
    TMIN = pd.read_csv(ruta_tmin[i])
    product = InputsNoRevolvente(REAL,TEORICO,completar=True,mincosecha=201901,maxcosecha=201912)
    for j in range(5):
        if i!=5:
            cortes = lista_cortes[j]
        else:
            cortes = lista_cortes_Pyme[j]
        product.condensar(cortes)
        product.optimizar()
        product.impactoTmin(TMIN,completar=True)
        temp = pd.merge(left=product.Tmin, right=product.stats, how='left', left_on=f.all_cortes(product.Tmin), right_on=f.all_cortes(product.stats))
        etiqueta = lista_nombres[i]+str(j)+".xlsx"
        temp.to_excel(etiqueta)
