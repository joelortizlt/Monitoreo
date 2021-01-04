import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import Logicas.funciones as f
from Logicas.InputsNoRevolvente import InputsNoRevolvente
from Logicas.OutputsNoRevolvente import OutputsNoRevolvente

#CAMBIAR
nombreproducto = 'estacional'
inicio = 201812
fin = 201912



#agregado_cortes=['C_SEGMENTO','C_MONEDA','C_PLAZO','C_OK']
#agregado_cortes=['C_SEGMENTO','C_MONEDA','C_PLAZO','C_CANAL','C_OK']
#agregado_cortes=['C_PRODUCTO','C_MONEDA','C_PYG']
agregado_cortes=['C_CAMPANIA','C_PLAZO','C_OK']

#lista_cortes=[['C_SEGMENTO'],['C_MONEDA'],['C_PLAZO'],['C_OK']]
#lista_cortes=[['C_SEGMENTO'],['C_MONEDA'],['C_PLAZO'],['C_CANAL'],['C_OK']]
#lista_cortes=[['C_PRODUCTO'],['C_MONEDA'],['C_PYG']]
lista_cortes=[['C_CAMPANIA'],['C_PLAZO'],['C_OK']]

ruta_real=['/Users/renzomartinch/Downloads/ComiteSetiembre/'+str(nombreproducto)+'_reales.csv']
ruta_teorico=['/Users/renzomartinch/Downloads/ComiteSetiembre/'+str(nombreproducto)+'_inputs.csv']
ruta_tmin=['/Users/renzomartinch/Downloads/ComiteSetiembre/'+str(nombreproducto)+'_precios.csv']

n = len(agregado_cortes)

REAL = pd.read_csv(ruta_real[0])#, encoding='latin-1')
TEORICO = pd.read_csv(ruta_teorico[0])#, encoding='latin-1')
TMIN = pd.read_csv(ruta_tmin[0])#, encoding='latin-1')
    
product = InputsNoRevolvente(REAL,TEORICO,mincosecha=inicio,maxcosecha=fin)
product.condensar(agregado_cortes)
product.optimizar()
product.impactoTmin(TMIN)
#product.impactoTIR(TMIN)

a = product.promedios
b = product.stats.drop(product.stats.iloc[:, 0:(n+1)], axis = 1)
c = product.Tmin.drop(product.Tmin.iloc[:, 0:(n+1)], axis = 1) 
#d = product.TIR.drop(product.TIR.iloc[:, 0:(n+1)], axis = 1)

#product = OutputsNoRevolvente(REAL,TEORICO,mincosecha=inicio,maxcosecha=fin)
#product.condensar(agregado_cortes)

#e = product.ratios.drop(product.ratios.iloc[:, 0:(n+2)], axis = 1)
#f = product.niveles.drop(product.niveles.iloc[:, 0:(n+2)], axis = 1)

agregado = pd.concat([a,b,c], axis=1) #<- añadir d,e,f

first = True
for corte in lista_cortes:

    condensado = agregado.groupby(corte).size().reset_index().rename(columns={0:'descartar'}).drop('descartar',1)

    for j in range(len(condensado)):
            
        temp = agregado.loc[agregado[corte[0]] == condensado.loc[j,corte[0]]]
        r = temp['recuento']
        m = temp['Monto']
        #e = temp['Capital promedio']
        #s = temp['n_saldo_real']

        condensado.at[j,'recuento'] = sum(r)
        for k in ['pd_real','can_real','pre_real','pd_teorico','can_teorico','pre_teorico','pd_optimo','can_optimo','pre_optimo','MAE_pd','MAE_can','MAE_pre','MAEop_pd','MAEop_can','MAEop_pre','scalar_pd','scalar_can','scalar_pre']:
            condensado.at[j,k] = sum(temp[k] * r) / sum(r)
            
        for k in ['Tmin_base','delta_Tmin_pd','delta_Tmin_can','delta_Tmin_pre','Tmin_final']:
            condensado.at[j,k] = sum(temp[k] * m) / sum(m)
        condensado.at[j,'Monto'] = sum(m)
            
        #for k in ['TIR_base','delta_TIR_pd','delta_TIR_can','delta_TIR_pre','TIR_final']:
        #    condensado.at[j,k] = sum(temp[k] * e) / sum(e)
        #condensado.at[j,'Capital promedio'] = sum(e)

        #for k in ['r_if_real','r_ef_real','r_spread_bruto_real','r_if_teorico','r_ef_teorico','r_spread_bruto_teorico']:
        #    condensado.at[j,k] = sum(temp[k] * s) / sum(s)

        #for k in ['n_if_real','n_ef_real','n_saldo_real','n_if_teorico','n_ef_teorico','n_saldo_teorico']:
        #    condensado.at[j,k] = sum(temp[k])

    nametemp=condensado.columns[0]
    condensado.rename(columns={nametemp:"CORTE"}, inplace=True)

    if first==True:
        imprimir = condensado
    else:
        imprimir = imprimir.append(condensado,ignore_index=True)
    first=False

print(imprimir)
imprimir.to_excel(str(nombreproducto)+"_PlanchaPonderada.xlsx")