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
REAL = pd.read_csv('/Users/renzomartinch/Downloads/VEH/Vehicular_Reales.csv')
TEORICO = pd.read_csv('/Users/renzomartinch/Downloads/VEH/Vehicular_Inputs.csv')
TMIN = pd.read_csv('/Users/renzomartinch/Downloads/VEH/Vehicular_Precios.csv')

#%%
#Se definen los cortes
cortes = ['C_PLAZO']
#Se crea el objeto
product = InputsNoRevolvente(REAL,TEORICO,completar=True)
#Se agrupa en base a los cortes definidos
product.condensar(cortes)

#%%
#Se puede optimizar
product.optimizar()

#%%
product.curvas

#%%
product.stats

#%%
product.intervalos

#%%
product.plotear('pd')
product.plotear('can')
product.plotear('pre')
#product.MAE('can')

#%%
product.plotear('pd',optimo=True)
product.plotear('can',optimo=True)
product.plotear('pre',optimo=True)
#product.MAE('can',optimo=True)

#%%
product.impactoTmin(TMIN,completar=True)
product.Tmin

#%%