#%%
#Se importan la librerías necesarias e insumen los .CSV
import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import funciones as f
from InputsNoRevolvente import InputsNoRevolvente

REAL = pd.read_csv('C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_PymeNR_TIR\PymeNR_AF_Reales.csv', low_memory=False)
TEORICO = pd.read_csv('C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_PymeNR_TIR\PymeNR_Inputs.csv', low_memory=False)
TMIN = pd.read_csv('C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_PymeNR_TIR\PymeNR_Precios.csv', low_memory=False)

#%%
#Se crea el objeto
product = InputsNoRevolvente(REAL,TEORICO)
product.df_teorico

#%%
#Se definen los cortes
cortes = ['C_PRODUCTO']
#Se agrupa en base a los cortes definidos
product.condensar(cortes)
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
product.MAE('pd')
product.MAE('can')
product.MAE('pre')

#%%
#Se puede optimizar
product.optimizar()
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
product.MAE('pd',optimo=True)
product.MAE('can',optimo=True)
product.MAE('pre',optimo=True)

#%%
product.impactoTmin(TMIN,impactoTIR=False)
product.Tmin

#%%
product.TminProm

#%%
product.impactoTmin(TMIN,impactoTIR=True)
product.TIR

#%%
product.Tmin

# %%
