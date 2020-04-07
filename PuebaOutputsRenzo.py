#Se impoortan la librerías necesarias
import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import funciones as f

from OutputsNoRevolventeReal import OutputsNoRevolventeReal
from OutputsNoRevolventeTeorico import OutputsNoRevolventeTeorico
from OutputsNoRevolvente import OutputsNoRevolvente

#Se insumen los CSV
REAL = pd.read_csv('/Users/renzomartinch/Downloads/GAHI/Outputs_REAL.csv')
TEORICO = pd.read_csv('/Users/renzomartinch/Downloads/GAHI/Outputs_TEORICO.csv')
#Se definen los cortes
cortes = ['C_SEGMENTO']

vehicular = OutputsNoRevolvente(REAL,TEORICO,completar=True)
print(vehicular.df_real)
print(vehicular.df_teorico)
vehicular.condensar(cortes)
print(vehicular.curvas)
print(vehicular.stats)
vehicular.plotear('ef')
vehicular.MAE('ef')

vehicular.optimizar()
print(vehicular.curvas)
print(vehicular.stats)
vehicular.plotear('ef',optimo=True)
vehicular.MAE('ef',optimo=True)