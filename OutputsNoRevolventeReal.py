#Se impoortan la librerías necesarias
import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import funciones as f



#creación de la clase
class OutputsNoRevolventeReal():
    #constructor del objeto
    def __init__(self,df,mincosecha='',maxcosecha=''): #se insume un documento de Excel
        
        #tranformar la data de las hojas del excel en dataframes
        df_real = df
        
        #colocar las curvas en una sola celda
        df_real['saldo'] = pd.DataFrame({'pd':df_real.iloc[:,f.encontrar_encabezado(df_real,'SALDOPROM1'):f.encontrar_encabezado(df_real,'IF1')].values.tolist()})
        df_real['if'] = pd.DataFrame({'pd':df_real.iloc[:,f.encontrar_encabezado(df_real,'IF1'):f.encontrar_encabezado(df_real,'EF1')].values.tolist()})
        df_real['ef'] = pd.DataFrame({'pd':df_real.iloc[:,f.encontrar_encabezado(df_real,'EF1'):f.encontrar_encabezado(df_real,'saldo')].values.tolist()})
        
        #seleccionar solo la data relevante
        df_real = df_real[f.all_cortes(df_real)+['CODCLAVEOPECTA','COSECHA','MAXMADPYG','MTODESEMBOLSADO','if','ef','saldo']]
        if mincosecha!='':
            df_real = df_real[df_real['COSECHA']>=mincosecha]
        if maxcosecha!='':
            df_real = df_real[df_real['COSECHA']<=maxcosecha]
        self.df_real = df_real
        
        
    #creación de los cortes
    def condensar(self,cortes=[]): #se insume una lista con los cortes que se desea
        
        #si no se ingresa cortes espécificos, se usan todos
        if cortes==[]:
            self.df_real['C_TODOS']=''
            cortes=['C_TODOS']
        
        #Creamos las 'plantillas'
        curvas = self.df_real.groupby(cortes).size().reset_index().rename(columns={0:'recuento'})
        curvas['monto'] = ''
        curvas['if_real'] = ''
        curvas['ef_real'] = ''
        curvas['saldo_real'] = ''
        
        #REALES
        for i in range(len(curvas)):
            temp = pd.merge(self.df_real[cortes+['CODCLAVEOPECTA','COSECHA','MAXMADPYG','MTODESEMBOLSADO','if','ef','saldo']], pd.DataFrame([curvas.loc[i,:]]), left_on=cortes, right_on=cortes, how='inner')

            temp['sum_if']=list(map(f.operation_pd, temp['MAXMADPYG'], temp['if']))
            temp['sum_ef']=list(map(f.operation_pd, temp['MAXMADPYG'], temp['ef']))
            temp['sum_saldo']=list(map(f.operation_pd, temp['MAXMADPYG'], temp['saldo']))
            
            a = f.aggr_sum(temp['sum_if'])
            b = f.aggr_sum(temp['sum_ef'])
            c = f.aggr_sum(temp['sum_saldo'])
            
            curvas.at[i,'monto'] = temp['MTODESEMBOLSADO'].sum()
            curvas.at[i,'if_real'] = [round(x,0) for x in a]
            curvas.at[i,'ef_real'] = [round(x,0) for x in b]
            curvas.at[i,'saldo_real'] = [round(x,0) for x in c]

        self.curvasR = curvas