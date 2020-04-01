#Se impoortan la librerías necesarias
import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import funciones as f



#creación de la clase
class InputsNoRevolventeReal():
    #constructor del objeto
    def __init__(self,csv,mincosecha='',maxcosecha=''): #se insume un documento de Excel
        
        #tranformar la data de las hojas del excel en dataframes
        df_real = pd.read_csv(csv)
        
        #colocar las curvas en una sola celda
        df_real['prepagos'] = pd.DataFrame({'pd':df_real.iloc[:,f.encontrar_encabezado(df_real,'PREPAGO_1'):f.encontrar_encabezado(df_real,'MTODESEMBOLSADO_1')].values.tolist()})
        df_real['desembolso'] = pd.DataFrame({'pd':df_real.iloc[:,f.encontrar_encabezado(df_real,'MTODESEMBOLSADO_1'):f.encontrar_encabezado(df_real,'prepagos')].values.tolist()})
        
        #seleccionar solo la data relevante
        df_real = df_real[f.all_cortes(df_real)+['CODSOLICITUD','COSECHA','FAIL_TYPE', 'SURVIVAL','maxmad','prepagos','desembolso']]
        if mincosecha!='':
            df_real = df_real[df_real['COSECHA']>=mincosecha]
        if maxcosecha!='':
            df_real = df_real[df_real['COSECHA']<=maxcosecha]
        self.df_real = df_real
        
        
    #creación de los cortes
    def condensar(self,cortes=[]): #se insume una lista con los cortes que se desea
        
        #si no se ingresa cortes espécificos, se usan todos
        if cortes==[]:
            self.df_real['c_todos']=''
            cortes=['c_todos']
        
        #Creamos la 'plantilla'
        curvas = self.df_real.groupby(cortes).size().reset_index().rename(columns={0:'recuento'})
        curvas['pd_real'] = ''
        curvas['can_real'] = ''
        curvas['pre_real'] = ''
        
        #REALES
        for i in range(len(curvas)):
            temp = pd.merge(self.df_real[cortes+['CODSOLICITUD','COSECHA','maxmad','FAIL_TYPE','SURVIVAL','prepagos','desembolso']], pd.DataFrame([curvas.loc[i,:]]), left_on=cortes, right_on=cortes, how='inner')
            
            #pd y cancelaciones reales
            vector = pd.DataFrame()
            c = 0
            surviv = 1
            for j in range(1, temp['maxmad'].max()+1):
                #Count del número de defaults en cada maduración del rango de fechas
                default = temp.query('FAIL_TYPE == 1' + ' & SURVIVAL=='+str(j))['SURVIVAL'].count()
                #Count del número de cancelaciones en cada maduración del rango de fechas
                cancel = temp.query('FAIL_TYPE == 2' + ' & SURVIVAL=='+str(j))['SURVIVAL'].count()
                #Count del número de cuentas en cada maduración tomando en cuenta la máxima maduración y rango de fechas
                dem = temp.query('maxmad>=' + str(j))['SURVIVAL'].count()
                #Marginales
                pd_marginal = None
                if not dem == 0:
                    pd_marginal = default/dem
                    can_marginal = cancel/dem
                can_final = surviv*can_marginal
                surviv = (1-pd_marginal-can_marginal)*surviv
                #Agregar a la tabla
                vector.loc[c, 'pd_marginal'] = pd_marginal
                vector.loc[c, 'can_final'] = can_final
                c = c + 1
                
            resultado = vector['pd_marginal'].cumsum()
            curvas.at[i,'pd_real'] = f.porcentaje(resultado)

            resultado = vector['can_final'].cumsum()
            curvas.at[i,'can_real'] = f.porcentaje(resultado)
            
            #prepagos reales
            temp['sum_prepagos']=list(map(f.operation_pd, temp['maxmad'], temp['prepagos']))
            temp['sum_desembolso']=list(map(f.operation_pd, temp['maxmad'], temp['desembolso']))    
            a = f.aggr_sum(temp['sum_prepagos'])
            b = f.aggr_sum(temp['sum_desembolso'])
            resultado = [ai / bi for ai, bi in zip(a, b)]
            resultado = np.cumsum(resultado)
            curvas.at[i,'pre_real'] = f.porcentaje(resultado)
        
        self.curvas = curvas