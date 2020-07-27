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
from OutputsNoRevolvente import OutputsNoRevolvente

#%%
#Se insumen los CSV
REAL = pd.read_csv('D:\Codes\Data\CEF_Reales.csv', low_memory=False)
TEORICO = pd.read_csv('D:\Codes\Data\CEF_Inputs.csv', low_memory=False)
TMIN = pd.read_csv('D:\Codes\Data\CEF_Precios.csv', low_memory=False)



#%%
product = OutputsNoRevolvente(REAL,TEORICO,201901,201901,completar=True)
product.condensar(cortes)
product.plotear('if')
product.plotear('ef')
product.plotear('saldo')
#%%
product.ratios
#%%
#Se definen los cortes
# cortes = ['C_PLAZO']
# cortes = ['C_PRODUCTO']
#cortes = ['C_PLAZO','C_SEGMENTO']
# cortes = ['C_SEGMENTO']
# cortes = ['C_MALAVENTA']


#Se crea el objeto
cortes = ['C_CANAL']
product = InputsNoRevolvente(REAL,TEORICO,201905,202003,completar=True)
#%%
product.condensar(cortes)
#%%
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
cortes = ['C_PAUTA','C_CANAL','C_PLAZO']
product = InputsNoRevolvente(REAL,TEORICO,201905,202003,completar=True)
product.condensar(cortes)
product.plotear('pd',optimo=False)
#%%
product.plotear('can',optimo=False)
#%%
product.plotear('pre',optimo=False)

#%%
product.TminProm

# %%


# %%
TEORICO

# %%
