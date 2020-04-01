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
csv_REAL_VEH = '/Users/renzomartinch/Downloads/PDCANPRE_REALES.csv'
csv_PD_VEH = '/Users/renzomartinch/Downloads/PD_TEORICO.csv'
csv_CAN_VEH = '/Users/renzomartinch/Downloads/CAN_TEORICO.csv'
csv_PRE_VEH = '/Users/renzomartinch/Downloads/PRE_TEORICO.csv'
#Se definen los cortes
cortes = ['c_riesgo']

vehicularR = InputsNoRevolventeReal(csv_REAL_VEH)
vehicularR.condensar(cortes)

vehicularT = InputsNoRevolventeTeorico(csvpd = csv_PD_VEH, csvcan = csv_CAN_VEH, csvpre = csv_PRE_VEH)
vehicularT.condensar(cortes)

vehicular = InputsNoRevolvente(vehicularR,vehicularT)
print(vehicular.curvas)

vehicular.plotear('can')
vehicular.MAE('can')

vehicular.optimizar()
print(vehicular.curvas)

vehicular.plotear('can',optimo=True)
vehicular.MAE('can',optimo=True)