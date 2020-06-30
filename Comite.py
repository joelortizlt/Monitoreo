#%%
#Se importan la librerías necesarias
import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import funciones as f
from InputsNoRevolvente import InputsNoRevolvente
from InputsRevolvente import InputsRevolvente

#%%
#Se insumen los CSV
REAL = pd.read_csv('D:\Codes\Data\Hipot_Reales.csv', low_memory=False)
TEORICO = pd.read_csv('D:\Codes\Data\Hipot_Inputs.csv', low_memory=False)
TMIN = pd.read_csv('D:\Codes\Data\Hipot_Precios.csv', low_memory=False)
    #%%
#Se definen los cortes
# cortes = ['C_PLAZO']
# cortes = ['C_PRODUCTO']
cortes = ['C_PLAZO','C_SEGMENTO']
# cortes = ['C_SEGMENTO']
# cortes = ['C_MALAVENTA']

#CHIP Cortes: C_PLAZO,C_SEGMENTO,C_MONEDA,C_MALAVENTA
#GAHI Cortes: C_PLAZO,C_SEGMENTO,C_MONEDA,C_MALAVENTA
#Hipot Cortes: C_PLAZO,C_PRODUCTO,C_RANGOPD,C_MALAVENTA
#Se crea el objeto
product = InputsNoRevolvente(REAL,TEORICO,201801,201912,completar=True)
product.condensar(cortes)
product.optimizar()
#product18 = InputsNoRevolvente(REAL,TEORICO,201801,201812,completar=True)
#product18.condensar(cortes)
#product18.optimizar()
# product19 = InputsNoRevolvente(REAL,TEORICO,201901,201912,completar=True)
# product19.condensar(cortes)
# product19.optimizar()

#%%
product.impactoTmin(TMIN,impactoTIR=False)
# product17 = InputsNoRevolvente(REAL,TEORICO,
# 201701,201712,completar=True)
# product17.condensar(cortes)
# product17.optimizar()
# product17.impactoTmin(TMIN,completar=True)

#product18.impactoTmin(TMIN,impactoTIR=True)

# product19.impactoTmin(TMIN,impactoTIR=True)
#%%
product.stats
#%%
product.Tmin
#%%
product.TIR
#%%
# product17.Tmin

#%%
#product.plotear('pd',optimo=True)
# product17.plotear('pd',optimo=True)
#product18.plotear('pd',optimo=True)
#product19.plotear('pd',optimo=True)
product.plotear('can',optimo=True)
#product17.plotear('can',optimo=True)
#product18.plotear('can',optimo=True)
#product19.plotear('can',optimo=True)
product.plotear('pre',optimo=True)
# product17.plotear('pre',optimo=True)
#product18.plotear('pre',optimo=True)
#product19.plotear('pre',optimo=True)

#%%
product.TminProm

# %%


# %%
TEORICO

# %%
