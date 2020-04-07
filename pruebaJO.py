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


from OutputsNoRevolventeReal import OutputsNoRevolventeReal
from OutputsNoRevolventeTeorico import OutputsNoRevolventeTeorico
from OutputsNoRevolvente import OutputsNoRevolvente

#Se insumen los CSV
REAL = pd.read_csv('D:\Codes\GAHI\INPUTS_REAL.csv')
TEORICO = pd.read_csv('D:\Codes\GAHI\INPUTS_TEORICO.csv')
TMIN = pd.read_csv('D:\Codes\GAHI\TMIN.csv')

#Se definen los cortes
cortes = ['C_SEGMENTO']

inputs = InputsNoRevolvente(REAL,TEORICO,completar=True)
inputs.condensar(cortes)
#print(inputs.curvas)
#print(inputs.stats)
#inputs.plotear('pd')
#inputs.plotear('can')
#inputs.plotear('pre')
#inputs.MAE('can')

inputs.optimizar()
inputs.impactoTmin(TMIN)
print(inputs.Tmin)
print(inputs.TminProm)
#print(inputs.curvas)
#print(inputs.stats)
#inputs.plotear('can',optimo=True)
#inputs.MAE('can',optimo=True)

