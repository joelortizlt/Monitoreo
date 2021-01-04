#%%
#Se importan la librerías necesarias e insumen los .CSV
import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
from  Logicas import funciones as f
from  Logicas import InputsRevolvente as InputsRevolvente

REAL = pd.read_csv(r"C:\Users\joelo\Documents\BCP\Data\TSN_Reales.xlsx")
TEORICO = pd.read_csv(r"C:\Users\joelo\Documents\BCP\Data\TSN_Inputs.xlsx")
#TMIN = pd.read_csv('C:\Users\joelo\Documents\BCP\Data\TSN_Precios.csv')
#a

#%%
TEORICO.head(10)
#%%
#Se crea el objeto
product = InputsRevolvente.InputsRevolvente(REAL,TEORICO,mincosecha=201901,maxcosecha=201912)
product.df_real

#%%
#Se definen los cortes
cortes = ['C_LINEA']
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
product.ci_saldo

#%%
#Se puede ver gráficamente los resultados
#product.plotear('pd')
#product.plotear('can')
product.plotear('saldo')
#product.MAE('pd')
#product.MAE('can')
#product.MAE('saldo')

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
#product.plotear('pd',optimo=True)
#product.plotear('can',optimo=True)
product.plotear('saldo',optimo=True)
#product.MAE('pd',optimo=True)
#product.MAE('can',optimo=True)
#product.MAE('saldo',optimo=True)

#%%
product.stats.to_excel("factores.xlsx")

#%%
product.impactoTmin(TMIN,impactoTIR=False)
product.Tmin

#%%
product.TminProm

#%%
product.impactoTmin(TMIN,impactoTIR=True)
product.TIR

#%%
product.TIRProm

# %%
