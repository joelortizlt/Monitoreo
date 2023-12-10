#Se impoortan la librerías necesarias
import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error

from source.engine import funciones as f


#Creación de la clase
class InputsNoRevolventeReal():
    #constructor del objeto
    def __init__(self,df,mincosecha='',maxcosecha=''): #se insume un dataframe y (opcionalmente) filtros por cosechas
        
        df_real = df
        
        #Se coloca las curvas en una sola celda (por temas de orden)
        df_real['prepagos'] = pd.DataFrame({'pd':df_real.iloc[:,f.encontrar_encabezado(df_real,'PREPAGO1'):f.encontrar_encabezado(df_real,'MTODESEMBOLSADO1')].values.tolist()})
        df_real['desembolso'] = pd.DataFrame({'pd':df_real.iloc[:,f.encontrar_encabezado(df_real,'MTODESEMBOLSADO1'):f.encontrar_encabezado(df_real,'SALDOPROM1')].values.tolist()})
        
        #Se selecciona solo los campos relevantes y se filtra por cosecha
        df_real = df_real[f.all_cortes(df_real)+['CODCLAVEOPECTA','COSECHA','FAIL_TYPE', 'SURVIVAL','MAXMAD','prepagos','desembolso']]
        if mincosecha!='':
            df_real = df_real[df_real['COSECHA']>=mincosecha]
        if maxcosecha!='':
            df_real = df_real[df_real['COSECHA']<=maxcosecha]
        self.df_real = df_real
        
        
    #creación de los cortes
    def condensar(self,cortes=[]): #se insume una lista con los cortes que se desea
        
        #si no se ingresa cortes espécificos, se calcula el general sin desagregar
        if cortes==[]:
            self.df_real.loc[:,'C_TODOS']=''
            cortes=['C_TODOS']
        
        #Creamos la 'plantilla' con todas las cobinaciones de los cortes
        curvas = self.df_real.groupby(cortes).size().reset_index().rename(columns={0:'recuento'})
        curvas['pd_real'] = ''
        curvas['can_real'] = ''
        curvas['pre_real'] = ''
        curvas['vivos'] = ''
        #REALES
        for i in range(len(curvas)):
            temp = pd.merge(self.df_real[cortes+['CODCLAVEOPECTA','MAXMAD','FAIL_TYPE','SURVIVAL','prepagos','desembolso']], pd.DataFrame([curvas.loc[i,:]]), how='inner', left_on=cortes, right_on=cortes)
            
            #pd y cancelaciones reales
            vector = pd.DataFrame()
            c = 0
            surviv = 1
            for j in range(1, temp['SURVIVAL'].max()+1):
                #Count del número de defaults en cada maduración del rango de fechas
                default = temp.query('FAIL_TYPE == 1' + ' & SURVIVAL=='+str(j))['SURVIVAL'].count()
                #Count del número de cancelaciones en cada maduración del rango de fechas
                cancel = temp.query('FAIL_TYPE == 2' + ' & SURVIVAL=='+str(j))['SURVIVAL'].count()
                #Count del número de cuentas en cada maduración tomando en cuenta la máxima maduración y rango de fechas
                dem = temp.query('SURVIVAL>=' + str(j))['SURVIVAL'].count()
                dem_pd = temp.query('MAXMAD>=' + str(j))['SURVIVAL'].count()
                #Marginales
                pd_marginal = None
                p1 = None

                if not dem == 0:
                    p1 = default/dem
                    can_marginal = cancel/dem
                can_final = surviv*can_marginal
                surviv = (1-p1-can_marginal)*surviv
                #Agregar a la tabla
                vector.loc[c, 'p1'] = p1
                vector.loc[c, 'can_final'] = can_final
                vector.loc[c,'vivos'] = dem

                if not dem_pd == 0:
                    pd_marginal = default/dem_pd
                #Agregar a la tabla
                vector.loc[c, 'pd_marginal'] = pd_marginal
                c = c + 1
                
            resultado = vector['pd_marginal'].cumsum()
            curvas.at[i,'pd_real'] = f.porcentaje(resultado)

            resultado = vector['can_final'].cumsum()
            curvas.at[i,'can_real'] = f.porcentaje(resultado)
            
            curvas.at[i,'vivos'] = vector['vivos'].values

            #prepagos reales
            temp['sum_prepagos']=list(map(f.operation_pd, temp['MAXMAD'], temp['prepagos']))
            temp['sum_desembolso']=list(map(f.operation_pd, temp['MAXMAD'], temp['desembolso']))    
            a = f.aggr_sum(temp['sum_prepagos'])
            b = f.aggr_sum(temp['sum_desembolso'])
            resultado = [ai / bi for ai, bi in zip(a, b)]
            resultado = np.cumsum(resultado)
            curvas.at[i,'pre_real'] = f.porcentaje(resultado)
        
        self.curvasR = curvas