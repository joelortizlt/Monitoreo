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
cortes = []

product = InputsNoRevolvente(REAL,TEORICO,completar=True)
print(product.df_real)
print(product.df_teorico)

product.condensar(cortes)
print(product.curvas)
print(product.stats)
product.plotear('can')
product.MAE('can')

product.optimizar()
print(product.curvas)
print(product.stats)
product.plotear('can',optimo=True)
product.MAE('can',optimo=True)

product.impactoTmin(TMIN,completar=True)
print(product.Tmin)
print(product.TminProm)