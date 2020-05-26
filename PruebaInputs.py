#%%
#Se importan la librerías necesarias
import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import funciones as f
from InputsNoRevolvente import InputsNoRevolvente

#%%
#Se insumen los CSV
REAL = pd.read_csv('/Users/renzomartinch/Downloads/Comite_1105/Hipot_Reales.csv', low_memory=False)
TEORICO = pd.read_csv('/Users/renzomartinch/Downloads/Comite_1105/Hipot_Inputs.csv', low_memory=False)
TMIN = pd.read_csv('/Users/renzomartinch/Downloads/Comite_1105/Hipot_Precios.csv', low_memory=False)

#%%
#Se crea el objeto
product = InputsNoRevolvente(REAL,TEORICO,completar=True)
product.df_real

#%%
product.df_teorico

#%%
#Se definen los cortes
cortes = ['C_SEGMENTO']
#Se agrupa en base a los cortes definidos
product.condensar(cortes)
product.curvas

#%%
product.nT

#%%
product.stats

#%%
product.promedios

#%%
product.ci_pd

#%%
product.plotear('pd')
product.plotear('can')
product.plotear('pre')
product.MAE('pd')
product.MAE('can')
product.MAE('pre')

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
product.plotear('pd',optimo=True)
product.plotear('can',optimo=True)
product.plotear('pre',optimo=True)
product.MAE('pd',optimo=True)
product.MAE('can',optimo=True)
product.MAE('pre',optimo=True)

#%%
product.impactoTmin(TMIN,completar=True)
product.Tmin

#%%
product.TminProm

# %%
