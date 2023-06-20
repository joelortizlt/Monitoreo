#Se impoortan la librerías necesarias
import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error

from source.engine import funciones as f



#creación de la clase
class OutputsNoRevolventeReal():
    #constructor del objeto
    def __init__(self,df,mincosecha='',maxcosecha=''): #se insume un documento de Excel
        
        #tranformar la data de las hojas del excel en dataframes
        df_real = df
        
        #colocar las curvas en una sola celda
        df_real['Saldo'] = pd.DataFrame({'pd':df_real.loc[:,'SALDOPROM1':'SALDOPROM36'].values.tolist()})
        df_real['IF'] = pd.DataFrame({'pd':df_real.loc[:,'IF1':'IF36'].values.tolist()})
        df_real['EF'] = pd.DataFrame({'pd':df_real.loc[:,'EF1':'EF36'].values.tolist()})
        df_real['Rebate'] = pd.DataFrame({'pd':df_real.loc[:,'Rebate1':'Rebate36'].values.tolist()})
        df_real['ProvisionB'] = pd.DataFrame({'pd':df_real.loc[:,'PROVBRUTA1':'PROVBRUTA36'].values.tolist()})
        df_real['IxS'] = pd.DataFrame({'pd':df_real.loc[:,'IxS1':'IxS36'].values.tolist()})

        #seleccionar solo la data relevante
        df_real = df_real[f.all_cortes(df_real)+['CODCLAVEOPECTA','COSECHA','MAXMADPYG','MTODESEMBOLSADO','IF','EF','Saldo','Rebate','ProvisionB','IxS']]
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
        curvas['rebate_real'] = ''
        curvas['provisionb_real'] = ''
        curvas['ixs_real'] = ''
        
        #REALES
        for i in range(len(curvas)):
            temp = pd.merge(self.df_real[cortes+['CODCLAVEOPECTA','COSECHA','MAXMADPYG','MTODESEMBOLSADO','IF','EF','Saldo','Rebate','ProvisionB','IxS']], pd.DataFrame([curvas.loc[i,:]]), left_on=cortes, right_on=cortes, how='inner')

            temp['sum_if']=list(map(f.operation_pd, temp['MAXMADPYG'], temp['IF']))
            temp['sum_ef']=list(map(f.operation_pd, temp['MAXMADPYG'], temp['EF']))
            temp['sum_saldo']=list(map(f.operation_pd, temp['MAXMADPYG'], temp['Saldo']))
            temp['sum_rebate']=list(map(f.operation_pd, temp['MAXMADPYG'], temp['Rebate']))
            temp['sum_provisionB']=list(map(f.operation_pd, temp['MAXMADPYG'], temp['ProvisionB']))
            temp['sum_IxS']=list(map(f.operation_pd, temp['MAXMADPYG'], temp['IxS']))

            a = f.aggr_sum(temp['sum_if'])
            b = f.aggr_sum(temp['sum_ef'])
            d = f.aggr_sum(temp['sum_saldo'])
            e = f.aggr_sum(temp['sum_rebate'])
            g = f.aggr_sum(temp['sum_provisionB'])
            h = f.aggr_sum(temp['sum_IxS'])
            
            curvas.at[i,'monto'] = temp['MTODESEMBOLSADO'].sum()
            curvas.at[i,'if_real'] = [round(x,0) for x in a]
            curvas.at[i,'ef_real'] = [round(x,0) for x in b]
            curvas.at[i,'saldo_real'] = [round(x,0) for x in d]
            curvas.at[i,'rebate_real'] = [round(x,0) for x in e]
            curvas.at[i,'provisionb_real'] = [round(x,0) for x in g]
            curvas.at[i,'ixs_real'] = [round(x,0) for x in h]

        self.curvasR = curvas