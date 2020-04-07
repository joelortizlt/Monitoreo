#Se impoortan la librerías necesarias
import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import funciones as f



#creación de la clase
class OutputsNoRevolventeTeorico():
    #constructor del objeto
    def __init__(self,df,mincosecha='',maxcosecha=''): #se insume un documento de Excel
        
        #tranformar la data de las hojas del excel en dataframes
        df_teorico = df
        
        #colocar las curvas en una sola celda
        df_teorico['if'] = pd.DataFrame({'pd':df_teorico.iloc[:,f.encontrar_encabezado(df_teorico,'IF1'):f.encontrar_encabezado(df_teorico,'EF1')].values.tolist()})
        df_teorico['ef'] = pd.DataFrame({'pd':df_teorico.iloc[:,f.encontrar_encabezado(df_teorico,'EF1'):f.encontrar_encabezado(df_teorico,'SALDO1')].values.tolist()})
        df_teorico['saldo'] = pd.DataFrame({'pd':df_teorico.iloc[:,f.encontrar_encabezado(df_teorico,'SALDO1'):f.encontrar_encabezado(df_teorico,'if')].values.tolist()})
 
        #seleccionar solo la data relevante
        df_teorico = df_teorico[f.all_cortes(df_teorico)+['CODSOLICITUD','COSECHA','MAXMAD','if','ef','saldo']]

        if mincosecha!='':
            df_teorico = df_teorico[df_teorico['COSECHA']>=mincosecha]
        if maxcosecha!='':
            df_teorico = df_teorico[df_teorico['COSECHA']<=maxcosecha]
        self.df_teorico = df_teorico
        
        
    #creación de los cortes
    def condensar(self,cortes=[]): #se insume una lista con los cortes que se desea
        
        #si no se ingresa cortes espécificos, se usan todos
        if cortes==[]:
            self.df_teorico['C_TODOS']=''
            cortes=['C_TODOS']

        #Creamos la 'plantilla'
        curvas = self.df_teorico.groupby(cortes).size().reset_index().rename(columns={0:'recuento'})
        ratios = curvas.copy()
        curvas['if_teorico'] = ''
        curvas['ef_teorico'] = ''
        curvas['saldo_teorico'] = ''
        ratios['r_if_teorico'] = ''
        ratios['r_ef_teorico'] = ''
        ratios['r_spread_teorico'] = ''
        
        #TEÓRICAS
        for i in range(len(curvas)):
            
            temp = pd.merge(self.df_teorico[cortes+['CODSOLICITUD','COSECHA','MAXMAD','if','ef','saldo']], pd.DataFrame([curvas.loc[i,:]]), left_on=cortes, right_on=cortes, how='inner')
            #IF teórico
            temp['result'] = list(map(f.operation_pd, temp['MAXMAD'], temp['if']))
            a = f.aggr_sum(temp['result'])
            
            #EF teórico
            temp['result']=list(map(f.operation_pd, temp['MAXMAD'], temp['ef']))
            b = f.aggr_sum(temp['result'])
            
            #SALDO teórico
            temp['result']=list(map(f.operation_pd, temp['MAXMAD'], temp['saldo']))
            c = f.aggr_sum(temp['result'])
            
            curvas.at[i,'if_teorico'] = [round(x,0) for x in a]
            curvas.at[i,'ef_teorico'] = [round(x,0) for x in b]
            curvas.at[i,'saldo_teorico'] = [round(x,0) for x in c]
            ratios.at[i,'r_if_teorico'] = round((1+(sum(a)/sum(c)))**12-1,6)*100
            ratios.at[i,'r_ef_teorico'] = round((1+(sum(b)/sum(c)))**12-1,6)*100
            ratios.at[i,'r_apread_teorico'] = round((1+((sum(a)+sum(b))/sum(c)))**12-1,6)*100

        self.curvasT = curvas
        self.ratiosT = ratios