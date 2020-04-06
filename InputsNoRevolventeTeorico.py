#Se impoortan la librerías necesarias
import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import funciones as f



#creación de la clase
class InputsNoRevolventeTeorico():
    #constructor del objeto
    def __init__(self,df,mincosecha='',maxcosecha=''): #se insume un documento de Excel
        
        #tranformar la data de las hojas del excel en dataframes
        df_teorico = df
        
        #colocar las curvas en una sola celda
        df_teorico['pd_marginal'] = pd.DataFrame({'pd':df_teorico.iloc[:,f.encontrar_encabezado(df_teorico,'PD1'):f.encontrar_encabezado(df_teorico,'CAN1')].values.tolist()})
        df_teorico['can_marginal'] = pd.DataFrame({'pd':df_teorico.iloc[:,f.encontrar_encabezado(df_teorico,'CAN1'):f.encontrar_encabezado(df_teorico,'PRE1')].values.tolist()})
        df_teorico['pre_marginal'] = pd.DataFrame({'pd':df_teorico.iloc[:,f.encontrar_encabezado(df_teorico,'PRE1'):f.encontrar_encabezado(df_teorico,'pd_marginal')].values.tolist()})
 
        #seleccionar solo la data relevante
        df_teorico = df_teorico[f.all_cortes(df_teorico)+['CODSOLICITUD','COSECHA','maxmad','pd_marginal', 'can_marginal', 'pre_marginal']]
        
        if mincosecha!='':
            df_teorico = df_teorico[df_teorico['COSECHA']>=mincosecha]
        if maxcosecha!='':
            df_teorico = df_teorico[df_teorico['COSECHA']<=maxcosecha]
        self.df_teorico = df_teorico
        
        
    #creación de los cortes
    def condensar(self,cortes=[]): #se insume una lista con los cortes que se desea
        
        #si no se ingresa cortes espécificos, se usan todos
        if cortes==[]:
            self.df_teorico['c_todos']=''
            cortes=['c_todos']

        #Creamos la 'plantilla'
        curvas = self.df_teorico.groupby(cortes).size().reset_index().rename(columns={0:'recuento'})
        curvas['pd_teorico'] = ''
        curvas['can_teorico'] = ''
        curvas['pre_teorico'] = ''
        
        #TEÓRICOS
        for i in range(len(curvas)):
            
            #pd teórico
            temp = pd.merge(self.df_teorico[cortes+['CODSOLICITUD','COSECHA','maxmad','pd_marginal']], pd.DataFrame([curvas.loc[i,:]]), left_on=cortes, right_on=cortes, how='inner')
            temp['result'] = list(map(f.operation_pd, temp['maxmad'], temp['pd_marginal']))
            resultado = f.aggr_avg(temp['result'])
            resultado = np.cumsum(resultado)  
            curvas.at[i,'pd_teorico'] = f.porcentaje(resultado)
            
            #cancelaciones teórico
            temp = pd.merge(self.df_teorico[cortes+['CODSOLICITUD','COSECHA','maxmad','can_marginal']], pd.DataFrame([curvas.loc[i,:]]), left_on=cortes, right_on=cortes, how='inner')
            temp['result']=list(map(f.operation_pd, temp['maxmad'], temp['can_marginal']))
            resultado = f.aggr_avg(temp['result'])
            resultado = np.cumsum(resultado)   
            curvas.at[i,'can_teorico'] = f.porcentaje(resultado)
            
            #prepagos teórico
            temp = pd.merge(self.df_teorico[cortes+['CODSOLICITUD','COSECHA','maxmad','pre_marginal']], pd.DataFrame([curvas.loc[i,:]]), left_on=cortes, right_on=cortes, how='inner')
            temp['result']=list(map(f.operation_pd, temp['maxmad'], temp['pre_marginal']))
            resultado = f.aggr_avg(temp['result'])
            resultado = np.cumsum(resultado)
            curvas.at[i,'pre_teorico'] = f.porcentaje(resultado)

        self.curvasT = curvas