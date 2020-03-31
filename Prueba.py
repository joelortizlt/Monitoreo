import pandas as pd
from NoRevolvente_Real import  NoRevolventeReal
from NoRevolvente_Teorico import  NoRevolventeTeorico
from Comparacion import NoRevolvente


#Se insumen los CSV
csv_REAL_VEH = 'D:\Codes\Monitoreo\Vehicular/PDCANPRE_REALES.csv'
csv_PD_VEH = 'D:\Codes\Monitoreo\Vehicular/PD_TEORICO.csv'
csv_CAN_VEH = 'D:\Codes\Monitoreo\Vehicular/CAN_TEORICO.csv'
csv_PRE_VEH = 'D:\Codes\Monitoreo\Vehicular/PRE_TEORICO.csv'
cortes = ['c_riesgo']
vehicularR = NoRevolventeReal(csv_REAL_VEH)
vehicularR.condensar(cortes)
vehicularR.curvas.head(3)
vehicularT = NoRevolventeTeorico(csvpd = csv_PD_VEH, csvcan = csv_CAN_VEH, csvpre = csv_PRE_VEH)
vehicularT.condensar(cortes)
vehicularT.curvas.head(3)

vehicular = NoRevolvente(vehicularR,vehicularT)
vehicular.curvas

vehicular.optimizar()
vehicular.curvas

vehicular.plotear('can',optimo=True)
vehicular.MAE('can',optimo=True)