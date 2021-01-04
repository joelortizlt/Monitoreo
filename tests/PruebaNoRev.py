#%%
#Se importan la librerías necesarias e insumen los .CSV
import sys
sys.path.append(r"C:\Users\joelo\Documents\BCP\Monitoreo\Monitoreo") #<--- CAMBIAR

import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error

from source.engine import funciones as f
from source.engine.InputsNoRevolvente import InputsNoRevolvente
from source.engine.OutputsNoRevolvente import OutputsNoRevolvente

ruta = r'C:\Users\joelo\Documents\BCP\Data'
nombreproducto = '\Gahi'
REAL = pd.read_csv(ruta+str(nombreproducto)+'_Reales.csv', low_memory=False)
TEORICO = pd.read_csv(ruta+str(nombreproducto)+'_Inputs.csv', low_memory=False)
TMIN = pd.read_csv(ruta+str(nombreproducto)+'_Precios.csv', low_memory=False)

#%%
#Se crea el objeto
product = InputsNoRevolvente(REAL,TEORICO,mincosecha=201901,maxcosecha=201912)

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
#También pueden graficarse
product.plotear('pd',optimo=True)
product.plotear('can',optimo=True)
product.plotear('pre',optimo=True)
product.MAE('pd',optimo=True)
product.MAE('can',optimo=True)
product.MAE('pre',optimo=True)

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
cortes = ['C_PLAZO']
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
# %%
