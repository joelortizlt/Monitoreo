#%%
#Se impoortan la librerías necesarias
import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import funciones as f
from InputsNoRevolvente import InputsNoRevolvente

#%%
#Se insumen los CSV
REAL = pd.read_csv('/Users/renzomartinch/Downloads/CEF/CEFCB_Reales.csv')
TEORICO = pd.read_csv('/Users/renzomartinch/Downloads/CEF/CEFCB_Inputs.csv')
TMIN = pd.read_csv('/Users/renzomartinch/Downloads/CEF/CEFCB_Precios.csv')

#%%
#Se definen los cortes
cortes = []

#Se crea el objeto
product = InputsNoRevolvente(REAL,TEORICO,completar=True)
product.condensar(cortes)

#%%
product.curvas

#%%
product.stats

#%%
product.plotear('pd')
product.plotear('can')
product.plotear('pre')
#product.MAE('can')

#%%
product.optimizar()

#%%
product.curvas

#%%
product.stats

#%%
product.plotear('pd',optimo=True)
product.plotear('can',optimo=True)
product.plotear('pre',optimo=True)
#product.MAE('can',optimo=True)

#%%
product.impactoTmin(TMIN,completar=True)
product.Tmin

#%%