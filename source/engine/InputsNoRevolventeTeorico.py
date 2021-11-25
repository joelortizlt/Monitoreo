#Se impoortan la librerías necesarias
import numpy as np
from numpy.core.records import array
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error

from source.engine import funciones as f


#creación de la clase
class InputsNoRevolventeTeorico():
    #constructor del objeto
    def __init__(self,df,mincosecha='',maxcosecha=''): #se insume un documento de Excel
        
        df_teorico = df
        
        #Se coloca las curvas en una sola celda (por temas de orden)
        df_teorico['pd_marginal'] = pd.DataFrame({'pd':df_teorico.iloc[:,f.encontrar_encabezado(df_teorico,'PD1'):f.encontrar_encabezado(df_teorico,'CAN1')].values.tolist()})
        df_teorico['can_marginal'] = pd.DataFrame({'pd':df_teorico.iloc[:,f.encontrar_encabezado(df_teorico,'CAN1'):f.encontrar_encabezado(df_teorico,'PRE1')].values.tolist()})
        df_teorico['pre_marginal'] = pd.DataFrame({'pd':df_teorico.iloc[:,f.encontrar_encabezado(df_teorico,'PRE1'):f.encontrar_encabezado(df_teorico,'SALDOPROM1')].values.tolist()})
 
        #Se selecciona solo los campos relevantes y se filtra por cosecha
        df_teorico = df_teorico[f.all_cortes(df_teorico)+['CODCLAVEOPECTA','COSECHA','MAXMAD','MTODESEMBOLSADO','pd_marginal', 'can_marginal', 'pre_marginal']]
        if mincosecha!='':
            df_teorico = df_teorico[df_teorico['COSECHA']>=mincosecha]
        if maxcosecha!='':
            df_teorico = df_teorico[df_teorico['COSECHA']<=maxcosecha]
        self.df_teorico = df_teorico
        
        
    #creación de los cortes
    def condensar(self,cortes=[]): #se insume una lista con los cortes que se desea
        
        #si no se ingresa cortes espécificos, se calcula el general sin desagregar
        if cortes==[]:
            self.df_teorico.loc[:,'C_TODOS']=''
            cortes=['C_TODOS']

        #Creamos la 'plantilla' con todas las cobinaciones de los cortes
        curvas = self.df_teorico.groupby(cortes).size().reset_index().rename(columns={0:'recuento'})
        curvas['pd_teorico'] = ''
        curvas['can_teorico'] = ''
        curvas['pre_teorico'] = ''
        n = curvas.copy()
        
        #TEÓRICOS
        for i in range(len(curvas)):
            
            temp = pd.merge(self.df_teorico[cortes+['CODCLAVEOPECTA','COSECHA','MAXMAD','MTODESEMBOLSADO','pd_marginal','can_marginal','pre_marginal']], pd.DataFrame([curvas.loc[i,:]]), how='inner', left_on=cortes, right_on=cortes)
            
            #pd teórico
            temp['result'] = list(map(f.operation_pd, temp['MAXMAD'], temp['pd_marginal']))
            resultado = f.aggr_avg(temp['result'])
            resultado = np.cumsum(resultado)
            curvas.at[i,'pd_teorico'] = f.porcentaje(resultado)
            n.at[i,'pd_teorico']= f.aggr_count(temp['result'])
            
            #cancelaciones teórico
            temp['result']=list(map(f.operation_pd, temp['MAXMAD'], temp['can_marginal']))
            resultado = f.aggr_avg(temp['result'])
            resultado = np.cumsum(resultado)   
            curvas.at[i,'can_teorico'] = f.porcentaje(resultado)
            n.at[i,'can_teorico']= f.aggr_count(temp['result'])
            
            #prepagos teórico
            temp['result'] = list(map(f.operation_pd, temp['MAXMAD'], temp['pre_marginal']))
            temp['monto'] = [len(x)*[w] for x,w in zip(temp['result'], temp['MTODESEMBOLSADO'])]

            resultado = f.weighted_average2(temp,'result','monto',temp['MAXMAD'].max())
            resultado = np.cumsum(resultado)
            curvas.at[i,'pre_teorico'] = f.porcentaje(resultado)
            n.at[i,'pre_teorico']= f.aggr_count(temp['result'])

        self.curvasT = curvas
        self.nT = n


