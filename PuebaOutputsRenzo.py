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
csv_REAL_VEH = '/Users/renzomartinch/Downloads/IFEFSAL_REALES.csv'
csv_IF_VEH = '/Users/renzomartinch/Downloads/IF_TEORICO.csv'
csv_EF_VEH = '/Users/renzomartinch/Downloads/EF_TEORICO.csv'
csv_SALDO_VEH = '/Users/renzomartinch/Downloads/SALDO_TEORICO.csv'
#Se definen los cortes
cortes = ['c_riesgo']

vehicularR = OutputsNoRevolventeReal(csv_REAL_VEH)
vehicularR.condensar(cortes)

vehicularT = OutputsNoRevolventeTeorico(csvif = csv_IF_VEH, csvef = csv_EF_VEH, csvsaldo = csv_SALDO_VEH)
vehicularT.condensar(cortes)

vehicular = OutputsNoRevolvente(vehicularR,vehicularT)
print(vehicular.curvas)

vehicular.plotear('saldo')
vehicular.MAE('saldo')

vehicular.optimizar()
print(vehicular.curvas)

vehicular.plotear('saldo',optimo=True)
vehicular.MAE('saldo',optimo=True)