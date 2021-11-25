#%%
#Se importan la librerías necesarias e insumen los .CSV
from os import replace
import sys

from pandas.core.frame import DataFrame
sys.path.append(r"C:\Users\joelo\Documents\BCP\Monitoreo\Monitoreo") #<--- Library Location

import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error

from source.engine import funciones as f
from source.engine.InputsNoRevolvente import InputsNoRevolvente
from source.engine.OutputsNoRevolvente import OutputsNoRevolvente

ruta = r'C:\Users\joelo\Documents\BCP\Monitoreo\Nov21' #--Files Location
nombreproducto = '\hipot'
REAL = pd.read_csv(ruta+str(nombreproducto)+'_Reales.csv', low_memory=False)
TEORICO = pd.read_csv(ruta+str(nombreproducto)+'_Inputs.csv', low_memory=False)
TMIN = pd.read_csv(ruta+str(nombreproducto)+'_Precios.csv', low_memory=False)

#%%  
#Call the object InputsNoRevolvente and select a date range
product = InputsNoRevolvente(REAL,TEORICO)
cortes = ['C_AÑO']
product.condensar(cortes)
#%%
#product.plotear('pd')
product.plotear('can')
product.plotear('pre')
#%%
#Set the segmentation variables, for average curve  run as cortes = []
agregado_cortes=['C_AÑO','C_MONEDA','C_PLAZO']            
appended_data = []
for j in agregado_cortes:
    cortes = [j]
#Se agrupa en base a los cortes definidos
    product.condensar(cortes)
    product.optimizar()
    df = product.curvas[[j,'pre_real','pre_teorico']]
    appended_data.append(df)

appended_data = pd.concat(appended_data)    
appended_data.to_excel(ruta+str(nombreproducto)+'_Curvas.xlsx')

#%%
product.stats

#%%
product.promedios

#%%
product.curvas

#%%
#Se puede ver gráficamente los resultados
product.plotear('pd')
product.plotear('can')
product.plotear('pre')



#%%
#Se puede optimizar
product.optimizar()

#%%
product.curvas

#%%
product.stats
#%%
product.curvas.to_excel(ruta+str(nombreproducto)+'_curvas.xlsx')

#%%
product.promedios

#%%
#También pueden graficarse
#product.plotear('pd',optimo=True)
#product.plotear('can',optimo=True)
product.plotear('pre',optimo=True)


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
product = OutputsNoRevolvente(REAL,TEORICO, mincosecha=202001 ,maxcosecha=202108)

#%%
#Se definen los cortes
cortes = ['C_PRODUCTO']
#Se agrupa en base a los cortes definidos
product.condensar(cortes)
product.ratios
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
#product.curvas.to_excel(ruta+str(nombreproducto)+'_Curvas.xlsx')
#product.niveles.to_excel(ruta+str(nombreproducto)+'_levels.xlsx')
product.ratios.to_excel(ruta+str(nombreproducto)+'_ratios.xlsx')
# %%
