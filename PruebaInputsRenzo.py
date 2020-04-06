#Se impoortan la librerías necesarias
import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import funciones as f

from InputsNoRevolventeReal import InputsNoRevolventeReal
from InputsNoRevolventeTeorico import InputsNoRevolventeTeorico
from InputsNoRevolvente import InputsNoRevolvente

#Se insumen los CSV
csv_REAL = pd.read_csv('/Users/renzomartinch/Downloads/GAHI/INPUTS_REAL.csv')
csv_TEORICO = pd.read_csv('/Users/renzomartinch/Downloads/GAHI/INPUNTS_TEORICO.csv')
#Se definen los cortes
cortes = ['c_riesgo']

vehicularR = InputsNoRevolventeReal(csv_REAL)
vehicularR.condensar(cortes)

vehicularT = InputsNoRevolventeTeorico(csv_TEORICO)
vehicularT.condensar(cortes)

vehicular = InputsNoRevolvente(vehicularR,vehicularT)
print(vehicular.curvas)

vehicular.plotear('can')
vehicular.MAE('can')

vehicular.optimizar()
print(vehicular.curvas)

vehicular.plotear('can',optimo=True)
vehicular.MAE('can',optimo=True)