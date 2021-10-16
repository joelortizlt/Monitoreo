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

ruta = r'C:\Users\joelo\Documents\BCP\Monitoreo\FICO\Validacion' #--Files Location
nombreproducto = '\cef201907'
REAL = pd.read_csv(ruta+str(nombreproducto)+'_Reales.csv', low_memory=False)
TEORICO = pd.read_csv(ruta+str(nombreproducto)+'_Inputs.csv', low_memory=False)
TMIN = pd.read_csv(ruta+str(nombreproducto)+'_Precios.csv', low_memory=False)

#agregado_cortes=['C_SEGMENTO','C_MONEDA','C_PLAZO','C_OK']                         # Gahi & Veh
#agregado_cortes=['C_PLAZO','C_OK']     # Hipot
#agregado_cortes=['C_SCORE','C_PLAZO','C_OK']                              #MiViv
#agregado_cortes=['C_PLAZO']            # CEF
#agregado_cortes=['C_PRODUCTO','C_MONEDA','C_PYG']
#gregado_cortes=['C_CAMPANIA','C_PLAZO','C_OK']
#agregado_cortes=['C_PLAZO','C_RANGO_INGRESO','C_CUOTADOBLE','C_JOVEN','C_SEGMENTO','C_OK']  

  
#%%
#Call the object InputsNoRevolvente and select a date range
product = InputsNoRevolvente(REAL,TEORICO,mincosecha=201907,maxcosecha=201907)
cortes = []
product.condensar(cortes)
product.plotear('pd')
product.plotear('can')
product.plotear('pre')
#%%
#Set the segmentation variables, for average curve  run as cortes = []
agregado_cortes=['C_OK']            # CEF
appended_data = []
for j in agregado_cortes:
    cortes = [j]
#Se agrupa en base a los cortes definidos
    product.condensar(cortes)
    product.optimizar()
    df = product.curvas[[j,'pd_real','pd_teorico','can_real','can_teorico','pre_real','pre_teorico']]
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
#product.plotear('pd')
#product.plotear('can')
product.plotear('pre')



#%%
#Se puede optimizar
product.optimizar()

#%%
product.curvas

#%%
product.stats
#product.stats.to_excel(ruta+str(nombreproducto)+'_Can_escalares.xlsx')

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
product = OutputsNoRevolvente(REAL,TEORICO,mincosecha=201907,maxcosecha=201907)#,maxcosecha=201912)

#%%
#Se definen los cortes
cortes = ['C_PRODUCTO']
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
product.curvas.to_excel(ruta+str(nombreproducto)+'_Curvas.xlsx')
product.niveles.to_excel(ruta+str(nombreproducto)+'_levels.xlsx')
product.ratios.to_excel(ruta+str(nombreproducto)+'_ratios.xlsx')
# %%
