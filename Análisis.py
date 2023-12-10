#%%
import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
from source.engine import funciones as f
from source.engine.InputsNoRevolvente import InputsNoRevolvente
from source.engine.OutputsNoRevolvente import OutputsNoRevolvente

ruta = r'C:\Users\joelo\Documents\Python\Monitoreo\Data'
REAL = pd.read_csv(r'C:\Users\joelo\Documents\Python\Monitoreo\Data\\veh_real.csv')
TEORICO = pd.read_csv(r'C:\Users\joelo\Documents\Python\Monitoreo\Data\\veh_inputs.csv')

inicio = 202201
fin = 202201
agregado_cortes=['C_OK']  
product = OutputsNoRevolvente(REAL,TEORICO,mincosecha=inicio,maxcosecha=fin)
product.condensar(agregado_cortes)
#product.plotear()
#product.plotear(texto : 's)
#product.ratios.to_excel('ratiosVEH.xlsx')
#product.curvas.to_excel('curvasYS.xlsx')
# %%
