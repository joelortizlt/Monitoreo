#%%
import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
from source.engine import funciones as f
from source.engine.InputsNoRevolvente import InputsNoRevolvente
from source.engine.OutputsNoRevolvente import OutputsNoRevolvente


#CAMBIAR
nombreproducto = '\cef'

inicio = 202101
fin = 202303

agregado_cortes=['C_OK','C_QUARTER','C_PLAZO','C_SEGMENTO']                   # CEF, Hipot, MiViv, Gahi & Veh
#agregado_cortes=['C_PRODUCTO','C_PYG','C_OK']                      # PYME

lista_cortes=[['C_OK'],['C_QUARTER'],['C_PLAZO'],['C_SEGMENTO']]                # CEF, Hipot, MiViv, Gahi & Veh    
#lista_cortes=[['C_PRODUCTO'],['C_PYG'],['C_OK']]                   # PYME

ruta = r'C:\Users\joelo\Documents\Python\Monitoreo\Data'
ruta_real=[ruta+str(nombreproducto)+'_real.csv']
ruta_teorico=[ruta+str(nombreproducto)+'_inputs.csv']
ruta_tmin=[ruta+str(nombreproducto)+'_precios.csv']

n = len(agregado_cortes)

REAL = pd.read_csv(ruta_real[0])#, encoding='latin-1')
TEORICO = pd.read_csv(ruta_teorico[0])#, encoding='latin-1')
TMIN = pd.read_csv(ruta_tmin[0])#, encoding='latin-1')
#%%    
product = InputsNoRevolvente(REAL,TEORICO,mincosecha=inicio,maxcosecha=fin)

#Inputs
product.condensar(agregado_cortes)
product.optimizar()
a = product.promedios
b = product.stats.drop(product.stats.iloc[:, 0:(n+1)], axis = 1)

#Tmin
product.impactoTmin(TMIN)
c = product.Tmin.drop(product.Tmin.iloc[:, 0:(n+1)], axis = 1) 

#TIR
product.impactoTIR(TMIN)
d = product.TIR.drop(product.TIR.iloc[:, 0:(n+1)], axis = 1)

#ROA
product.impactoROA(TMIN)
e = product.ROA.drop(product.TIR.iloc[:, 0:(n+1)], axis = 1)

#Outputs
product = OutputsNoRevolvente(REAL,TEORICO,mincosecha=inicio,maxcosecha=fin)

product.condensar(agregado_cortes)

f = product.ratios.drop(product.ratios.iloc[:, 0:(n+2)], axis = 1)
g = product.niveles.drop(product.niveles.iloc[:, 0:(n+2)], axis = 1)
#product.plotear(texto='if')

agregado = pd.concat([a,b,c,d,e,f,g], axis=1)

first = True
for corte in lista_cortes:

    condensado = agregado.groupby(corte).size().reset_index().rename(columns={0:'descartar'}).drop('descartar',1)

    for j in range(len(condensado)):
            
        temp = agregado.loc[agregado[corte[0]] == condensado.loc[j,corte[0]]]
        r = temp['recuento']
        m = temp['Monto']
        e = temp['Capital promedio']
        s = temp['n_saldo_real']
        w = temp['Saldo promedio']

        condensado.at[j,'recuento'] = sum(r)

        for k in ['pd_real','can_real','pre_real','pd_teorico','can_teorico','pre_teorico','pd_optimo','can_optimo','pre_optimo','scalar_pd','scalar_can','scalar_pre']:
            condensado.at[j,k] = sum(temp[k] * r) / sum(r)
            
        for k in ['Tmin_base','delta_Tmin_pd','delta_Tmin_can','delta_Tmin_pre','Tmin_final']:
            condensado.at[j,k] = sum(temp[k] * m) / sum(m)
        condensado.at[j,'Monto'] = sum(m)
            
        for k in ['TIR_base','delta_TIR_pd','delta_TIR_can','delta_TIR_pre','TIR_final']:
            condensado.at[j,k] = sum(temp[k] * e) / sum(e)
        condensado.at[j,'Capital promedio'] = sum(e)

        for k in ['ROA_base','delta_ROA_pd','delta_ROA_can','delta_ROA_pre','ROA_final']:
            condensado.at[j,k] = sum(temp[k] * e) / sum(w)
        condensado.at[j,'Saldo promedio'] = sum(w)
 
        for k in ['r_if_real','r_ef_real','r_rebate_real','r_spread_bruto_real','r_provisionb_real','r_ixs_real','r_spread_neto_real','r_if_teorico','r_ef_teorico','r_rebate_teorico','r_spread_bruto_teorico','r_provisionb_teorico','r_ixs_teorico','r_spread_neto_teorico']:
            condensado.at[j,k] = sum(temp[k] * s) / sum(s)

        for k in ['n_if_real','n_ef_real','n_rebate_real','n_spread_bruto_real','n_provisionb_real','n_ixs_real','r_spread_neto_real','n_saldo_real','n_if_teorico','n_ef_teorico','n_rebate_teorico','n_spread_bruto_teorico','n_provisionb_teorico','n_ixs_teorico','r_spread_neto_teorico','n_saldo_teorico']:
            condensado.at[j,k] = sum(temp[k])

    nametemp=condensado.columns[0]
    condensado.rename(columns={nametemp:"CORTE"}, inplace=True)

    if first==True:
        imprimir = condensado
    else:
        imprimir = imprimir.append(condensado,ignore_index=True)
    first=False

print(imprimir)

imprimir.to_excel(ruta+str(nombreproducto)+'_PlanchaPonderada.xlsx')


 # %%

# %%
