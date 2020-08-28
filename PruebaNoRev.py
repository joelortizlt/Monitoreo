#%%
#Se importan la librerías necesarias e insumen los .CSV
import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import funciones as f
from InputsNoRevolvente import InputsNoRevolvente
from OutputsNoRevolvente import OutputsNoRevolvente
REAL = pd.read_csv('/Users/renzomartinch/Downloads/ComiteAgosto/estacional_Reales.csv', low_memory=False)
TEORICO = pd.read_csv('/Users/renzomartinch/Downloads/ComiteAgosto/estacional_Inputs.csv', low_memory=False)
TMIN = pd.read_csv('/Users/renzomartinch/Downloads/ComiteAgosto/estacional_Precios.csv', low_memory=False)

#%%
#Se crea el objeto
product = InputsNoRevolvente(REAL,TEORICO,mincosecha=201801)#,maxcosecha=201912)

#%%
#Se definen los cortes
cortes = ['C_PLAZO']
#Se agrupa en base a los cortes definidos
product.condensar(cortes)

#%%
product.curvas

#%%
product.stats

#%%
product.promedios

#%%
product.ci_pd

#%%
#Se puede ver gráficamente los resultados
product.plotear('pd')
product.plotear('can')
product.plotear('pre')
#product.MAE('pd')
#product.MAE('can')
#product.MAE('pre')

#%%
#Se puede optimizar
product.optimizar()

#%%
product.curvas

#%%
product.stats

#%%
product.promedios

#%%
#También pueden graficarse
product.plotear('pd',optimo=True)
product.plotear('can',optimo=True)
product.plotear('pre',optimo=True)
#product.MAE('pd',optimo=True)
#product.MAE('can',optimo=True)
#product.MAE('pre',optimo=True)

#%%
product.impactoTmin(TMIN)
product.Tmin

#%%
product.TminProm

#%%
product.impactoTIR(TMIN)
product.TIR

#%%
product.TIRProm

# %%
#Se crea el objeto
product = OutputsNoRevolvente(REAL,TEORICO,mincosecha=201801)#,maxcosecha=201912)

#%%
#Se definen los cortes
cortes = ['C_CAMPANIA']
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