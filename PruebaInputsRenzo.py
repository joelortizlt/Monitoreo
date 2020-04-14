#Se impoortan la librerías necesarias
import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import funciones as f

from InputsNoRevolvente import InputsNoRevolvente

#Se insumen los CSV
REAL = pd.read_csv('C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_GAHI\INPUTS_REAL.csv')
TEORICO = pd.read_csv('C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_GAHI\INPUTS_TEORICO.csv')
TMIN = pd.read_csv('C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_GAHI\TMIN.csv')
#Se definen los cortes
cortes = ['C_SEGMENTO','C_PLAZO']

vehicular = InputsNoRevolvente(REAL,TEORICO,completar=True)
print(vehicular.df_real)
print(vehicular.df_teorico)

vehicular.condensar(cortes)
print(vehicular.curvas)
print(vehicular.stats)
vehicular.plotear('pre')
vehicular.MAE('pre')

vehicular.optimizar()
print(vehicular.curvas)
print(vehicular.stats)
vehicular.plotear('pre',optimo=True)
vehicular.MAE('pre',optimo=True)

vehicular.impactoTmin(TMIN)
print(vehicular.Tmin)