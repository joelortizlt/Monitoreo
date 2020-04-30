#Se impoortan la librerías necesarias
import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import funciones as f

from InputsNoRevolvente import InputsNoRevolvente

#Se insumen los CSV
REAL = pd.read_csv('/Users/renzomartinch/Downloads/CHIP/Hipot_Reales.csv')
TEORICO = pd.read_csv('/Users/renzomartinch/Downloads/CHIP/Hipot_Inputs.csv')
TMIN = pd.read_csv('/Users/renzomartinch/Downloads/CHIP/Hipot_Precios.csv')
#Se definen los cortes
cortes = ['C_SEGMENTO']

vehicular = InputsNoRevolvente(REAL,TEORICO,completar=True)
print(vehicular.df_real)
print(vehicular.df_teorico)

vehicular.condensar(cortes)
print(vehicular.curvas)
print(vehicular.stats)
vehicular.plotear('can')
vehicular.MAE('can')

vehicular.optimizar()
print(vehicular.curvas)
print(vehicular.stats)
vehicular.plotear('can',optimo=True)
vehicular.MAE('can',optimo=True)

vehicular.impactoTmin(TMIN)
print(vehicular.Tmin)