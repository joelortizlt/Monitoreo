import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import funciones as f
from InputsNoRevolvente import InputsNoRevolvente
from OutputsNoRevolvente import OutputsNoRevolvente

class Extraccion():
    #constructor del objeto
    def __init__(self,ruta,nombreproducto,inicio,fin,cortes,bool_tmin=True,bool_tir=True,bool_outputs=True):
        
        lista_cortes=[]
        for i in cortes:
            lista_cortes.append([i])

        ruta_real=[str(ruta)+str(nombreproducto)+'_reales.csv']
        ruta_teorico=[str(ruta)+str(nombreproducto)+'_inputs.csv']
        ruta_tmin=[str(ruta)+str(nombreproducto)+'_precios.csv']

        REAL = pd.read_csv(ruta_real[0])#, encoding='latin-1')
        TEORICO = pd.read_csv(ruta_teorico[0])#, encoding='latin-1')
        if bool_tmin==True or bool_tir==True:
            TMIN = pd.read_csv(ruta_tmin[0])#, encoding='latin-1')

        product = InputsNoRevolvente(REAL,TEORICO,mincosecha=inicio,maxcosecha=fin)
        product.condensar(cortes)
        product.optimizar()

        n = len(cortes)
        a = product.promedios
        b = product.stats.drop(product.stats.iloc[:, 0:(n+1)], axis = 1)
        if bool_tmin==True:
            product.impactoTmin(TMIN)
            c = product.Tmin.drop(product.Tmin.iloc[:, 0:(n+1)], axis = 1) 
        if bool_tir==True:
            product.impactoTIR(TMIN)
            d = product.TIR.drop(product.TIR.iloc[:, 0:(n+1)], axis = 1)
        if bool_outputs==True:
            product = OutputsNoRevolvente(REAL,TEORICO,mincosecha=inicio,maxcosecha=fin)
            product.condensar(cortes)
            e = product.ratios.drop(product.ratios.iloc[:, 0:(n+2)], axis = 1)
            f = product.niveles.drop(product.niveles.iloc[:, 0:(n+2)], axis = 1)

        if bool_tmin==True and bool_tir==True and bool_outputs==True:
            desagregado = pd.concat([a,b,c,d,e,f], axis=1)
        elif bool_tmin==True and bool_tir==True:
            desagregado = pd.concat([a,b,c,d], axis=1)
        elif bool_tmin==True and bool_outputs==True:
            desagregado = pd.concat([a,b,c,e,f], axis=1)
        elif bool_tir==True and bool_outputs==True:
            desagregado = pd.concat([a,b,d,e,f], axis=1)
        elif bool_tmin==True:
            desagregado = pd.concat([a,b,c], axis=1)
        elif bool_tir==True:
            desagregado = pd.concat([a,b,d], axis=1)
        elif bool_outputs==True:
            desagregado = pd.concat([a,b,e,f], axis=1)
        else:
            desagregado = pd.concat([a,b], axis=1)

        self.desagregado = desagregado

        product = InputsNoRevolvente(REAL,TEORICO,mincosecha=inicio,maxcosecha=fin)
        first = True
        first_g = True
        for corte in lista_cortes:

            condensado = desagregado.groupby(corte).size().reset_index().rename(columns={0:'descartar'}).drop('descartar',1)

            for j in range(len(condensado)):
                    
                temp = desagregado.loc[desagregado[corte[0]] == condensado.at[j,corte[0]]]

                r = temp['recuento']
                condensado.at[j,'recuento'] = sum(r)
                for k in ['pd_real','can_real','pre_real','pd_teorico','can_teorico','pre_teorico','pd_optimo','can_optimo','pre_optimo','MAE_pd','MAE_can','MAE_pre','MAEop_pd','MAEop_can','MAEop_pre','scalar_pd','scalar_can','scalar_pre']:
                    condensado.at[j,k] = sum(temp[k] * r) / sum(r)
                
                if bool_tmin==True:
                    m = temp['Monto']
                    for k in ['Tmin_base','delta_Tmin_pd','delta_Tmin_can','delta_Tmin_pre','Tmin_final']:
                        condensado.at[j,k] = sum(temp[k] * m) / sum(m)
                    condensado.at[j,'Monto'] = sum(m)

                if bool_tir==True:
                    e = temp['Capital promedio']    
                    for k in ['TIR_base','delta_TIR_pd','delta_TIR_can','delta_TIR_pre','TIR_final']:
                        condensado.at[j,k] = sum(temp[k] * e) / sum(e)
                    condensado.at[j,'Capital promedio'] = sum(e)
                
                if bool_outputs==True:
                    s = temp['n_saldo_real']
                    for k in ['r_if_real','r_ef_real','r_spread_bruto_real','r_if_teorico','r_ef_teorico','r_spread_bruto_teorico']:
                        condensado.at[j,k] = sum(temp[k] * s) / sum(s)
                    for k in ['n_if_real','n_ef_real','n_saldo_real','n_if_teorico','n_ef_teorico','n_saldo_teorico']:
                        condensado.at[j,k] = sum(temp[k])
                
            nametemp=condensado.columns[0]
            condensado.rename(columns={nametemp:"CORTE"}, inplace=True)

            if first==True:
                final = condensado
            else:
                final = final.append(condensado,ignore_index=True)
            first=False

            #---

            product.condensar(corte)
            a = product.ci_pd
            b = product.ci_can.drop(product.ci_can.iloc[:, 0:2], axis = 1)
            c = product.ci_pre.drop(product.ci_pre.iloc[:, 0:2], axis = 1)
            condensado_g = pd.concat([a,b,c], axis=1)

            nametemp_g=condensado_g.columns[0]
            condensado_g.rename(columns={nametemp_g:"CORTE"}, inplace=True)

            if first_g==True:
                final_g = condensado_g
            else:
                condensado_g
                final_g = final_g.append(condensado_g,ignore_index=True)
            first_g=False

        #final.to_excel(str(nombreproducto)+"_PlanchaPonderada.xlsx")
        self.data = final
        self.data_g = final_g
    


    def plot(self,fila,columna='pd'):
        
        if columna=='pd' or columna=='can' or columna=='pre':

            x=[]
            for i in range(len(self.data_g.at[fila,'y_real_'+columna])):
                x.append(i+1)

            r = self.data_g.at[fila,'y_real_'+columna]
            y = self.data_g.at[fila,'y_pred_'+columna]
            y90 = self.data_g.at[fila,'CI:5.0-95.0_'+columna]
            yu90 = self.data_g.at[fila,'CI:5.0-95.0_u_'+columna]
            y95 = self.data_g.at[fila,'CI:2.5-97.5_'+columna]
            yu95 = self.data_g.at[fila,'CI:2.5-97.5_u_'+columna]
            y99 = self.data_g.at[fila,'CI:0.5-99.5_'+columna]
            yu99 = self.data_g.at[fila,'CI:0.5-99.5_u_'+columna]

            fig, ax = plt.subplots()
            ax.fill_between(x, y99, yu99, color='#d5ffff')
            ax.fill_between(x, y95, yu95, color='#bdf6fe')
            ax.fill_between(x, y90, yu90, color='#8af1fe')
            ax.plot(x, y, color='blue')
            ax.plot(x, r, color='red')
            plt.show()
        
        else:
            print("Please, use 'pd', 'can' or 'pre' as column name")

#CAMBIAR
arg1 = '/Users/renzomartinch/Downloads/Comite/Bases/'
arg2 = 'veh'
arg3 = 201812
arg4 = 201912
arg5 =['C_SEGMENTO','C_MONEDA','C_PLAZO','C_OK']
#arg5 =['C_SEGMENTO','C_MONEDA','C_PLAZO','C_CANAL','C_OK']
#arg5 =['C_PRODUCTO','C_MONEDA','C_PYG']
#arg5 =['C_CAMPANIA','C_PLAZO','C_OK']

test = Extraccion(arg1,arg2,arg3,arg4,arg5)
print(test.desagregado)
print(test.data)
print(test.data_g)
test.plot(1,'can')
