#%%
#Se importan la librerías necesarias e insumen los .CSV
import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import funciones as f
from OutputsNoRevolvente import OutputsNoRevolvente

REAL = pd.read_csv('/Users/renzomartinch/Downloads/SeguimientoJulio/Vehicular_Reales.csv', low_memory=False)
TEORICO = pd.read_csv('/Users/renzomartinch/Downloads/SeguimientoJulio/Vehicular_Inputs.csv', low_memory=False)
TMIN = pd.read_csv('/Users/renzomartinch/Downloads/SeguimientoJulio/Vehicular_Precios.csv', low_memory=False)

#%%
#Se crea el objeto
product = OutputsNoRevolvente(REAL,TEORICO,mincosecha=201801)#,maxcosecha=201803)

#%%
#Se definen los cortes
cortes = []
#Se agrupa en base a los cortes definidos
product.condensar(cortes)

#%%
product.curvas

#%%
product.ratios

#%%
product.niveles

#%%
#Se puede ver gráficamente los resultados
product.plotear('if')
product.plotear('ef')
product.plotear('saldo')

#%%
product.ratios.to_excel("ratiosCHIP.xlsx")