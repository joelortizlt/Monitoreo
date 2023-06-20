#Se impoortan la librerías necesarias
import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
from source.engine import funciones as f


#creación de la clase
class OutputsNoRevolventeTeorico():
    #constructor del objeto
    def __init__(self,df,mincosecha='',maxcosecha=''): #se insume un documento de Excel
        
        df_teorico = df
        
        #colocar las curvas en una sola celda
        df_teorico['Saldo'] = pd.DataFrame({'pd':df_teorico.loc[:,'SALDOPROM1':'SALDOPROM36'].values.tolist()})
        df_teorico['IF'] = pd.DataFrame({'pd':df_teorico.loc[:,'IF1':'IF36'].values.tolist()})
        df_teorico['EF'] = pd.DataFrame({'pd':df_teorico.loc[:,'EF1':'EF36'].values.tolist()})
        df_teorico['Rebate'] = pd.DataFrame({'pd':df_teorico.loc[:,'Rebate1':'Rebate36'].values.tolist()})
        df_teorico['ProvisionB'] = pd.DataFrame({'pd':df_teorico.loc[:,'PE1':'PE36'].values.tolist()})
        df_teorico['IxS'] = pd.DataFrame({'pd':df_teorico.loc[:,'IxS1':'IxS36'].values.tolist()})

        #seleccionar solo la data relevante
        df_teorico = df_teorico[f.all_cortes(df_teorico)+['CODCLAVEOPECTA','COSECHA','MAXMADPYG','MTODESEMBOLSADO','Saldo','IF','EF','Rebate','ProvisionB','IxS']]#,'pe']]
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
        curvas['monto'] = ''
        curvas['saldo_teorico'] = ''
        curvas['if_teorico'] = ''
        curvas['ef_teorico'] = ''
        curvas['rebate_teorico'] = ''
        curvas['provisionb_teorico'] = ''
        curvas['ixs_teorico'] = ''
        
        
        #TEÓRICAS
        for i in range(len(curvas)):
            
            temp = pd.merge(self.df_teorico[cortes+['CODCLAVEOPECTA','COSECHA','MAXMADPYG','MTODESEMBOLSADO',
                                                    'Saldo','IF','EF','Rebate','ProvisionB','IxS']], pd.DataFrame([curvas.loc[i,:]]), left_on=cortes, right_on=cortes, how='inner')#,'pe']], pd.DataFrame([curvas.loc[i,:]]), left_on=cortes, right_on=cortes, how='inner')
            #IF teórico
            temp['result'] = list(map(f.operation_pd, temp['MAXMADPYG'], temp['IF']))
            a = f.aggr_sum(temp['result'])
            
            #EF teórico
            temp['result']=list(map(f.operation_pd, temp['MAXMADPYG'], temp['EF']))
            b = f.aggr_sum(temp['result'])

            
            #SALDO teórico
            temp['result']=list(map(f.operation_pd, temp['MAXMADPYG'], temp['Saldo']))
            d = f.aggr_sum(temp['result'])
            
            #Rebate teorico
            temp['result']=list(map(f.operation_pd, temp['MAXMADPYG'], temp['Rebate']))
            e = f.aggr_sum(temp['result'])
            
            #Provision teorico
            temp['result']=list(map(f.operation_pd, temp['MAXMADPYG'], temp['ProvisionB']))
            g = f.aggr_sum(temp['result'])
            
            #Ing no financiero teorico
            temp['result']=list(map(f.operation_pd, temp['MAXMADPYG'], temp['IxS']))
            h = f.aggr_sum(temp['result'])
            
            curvas.at[i,'monto'] = temp['MTODESEMBOLSADO'].sum()
            curvas.at[i,'if_teorico'] = [round(x,0) for x in a]
            curvas.at[i,'ef_teorico'] = [round(x,0) for x in b]
            curvas.at[i,'saldo_teorico'] = [round(x,0) for x in d]
            curvas.at[i,'rebate_teorico'] = [round(x,0) for x in e]
            curvas.at[i,'provisionb_teorico'] = [round(x,0) for x in g]
            curvas.at[i,'ixs_teorico'] = [round(x,0) for x in h]

        self.curvasT = curvas