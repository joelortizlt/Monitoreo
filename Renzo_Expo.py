# %%Se impoortan la librerías necesarias
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
REAL = pd.read_csv('C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_GAHI\INPUTS_REAL.csv')
TEORICO = pd.read_csv('C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_GAHI\INPUTS_TEORICO.csv')
TMIN = pd.read_csv('C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_GAHI\TMIN.csv')

# Se definen los cortes
cortes = ['C_SEGMENTO']

# ,'C_PLAZO','C_MONEDA'

#Se crean los objetos
inputs = InputsNoRevolvente(REAL,TEORICO,completar=True)
inputs.condensar(cortes)
#Método para optimizar
inputs.optimizar()
#Impacto en Tmin
inputs.impactoTmin(TMIN)


# %%Monitoreo de Modelo
inputs.curvas

# %%Calibracion Automática del Error Absoluto Medio
inputs.stats

# %%Calculo de Impactos Cortes
inputs.Tmin

# %%Calculo de Impactos Cortes
inputs.TminProm

# %%Graph
inputs.plotear('can',optimo = True)
inputs.MAE('can',optima = True)

# %%
