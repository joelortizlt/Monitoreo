#Se impoortan la librerías necesarias
#%%
import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
from source.engine import funciones as f
from source.engine.InputsNoRevolvente import InputsNoRevolvente
from source.engine.OutputsNoRevolvente import OutputsNoRevolvente

df = pd.read_csv(r'C:\Users\joelo\Documents\Python\Monitoreo\Data\Teorico_Portafolio.csv')

#TEORICO2 = pd.merge(left=REAL[['CODCLAVEOPECTA','COSECHA','PORT_202306','MTODESEMBOLSADO']], right=TEORICO, how='inner', left_on=['CODCLAVEOPECTA'], right_on=['CODCLAVEOPECTA'])
#%%
def corte_portafolio(a, b):
    return b[a-1:a]

def aggr_sum(result_col):
    def avg(x):
        x = [i for i in x if i is not None]
        return sum(x, 0.0000)
    filt = list(map(avg, it.zip_longest(*result_col)))
    return filt

def Portafolio_Teorico(df):
      
    #colocar las curvas en una sola celda
    df['Saldo'] = pd.DataFrame({'pd':df.loc[:,'SALDOPROM1':'SALDOPROM36'].values.tolist()})
    df['IF'] = pd.DataFrame({'pd':df.loc[:,'IF1':'IF36'].values.tolist()})
    df['EF'] = pd.DataFrame({'pd':df.loc[:,'EF1':'EF36'].values.tolist()})
    df['Rebate'] = pd.DataFrame({'pd':df.loc[:,'Rebate1':'Rebate36'].values.tolist()})
    df['ProvisionB'] = pd.DataFrame({'pd':df.loc[:,'PE1':'PE36'].values.tolist()})
    df['IxS'] = pd.DataFrame({'pd':df.loc[:,'IxS1':'IxS36'].values.tolist()})

    #seleccionar solo la data relevante
    df = df[['CODCLAVEOPECTA','COSECHA','PORT_202306','MTODESEMBOLSADO','Saldo','IF','EF','Rebate','ProvisionB','IxS']]

    
    #SALDO teórico
    df['Saldo_202306'] = list(map(corte_portafolio, df['PORT_202306'], df['Saldo']))
    #IF teórico
    df['IF_202306'] = list(map(corte_portafolio, df['PORT_202306'], df['IF']))
    #EF teórico
    df['EF_202306']=list(map(corte_portafolio, df['PORT_202306'], df['EF']))
    #Rebate teorico
    df['GEB_202306']=list(map(corte_portafolio, df['PORT_202306'], df['Rebate']))
    #Provision teorico
    df['PE_202306']=list(map(corte_portafolio, df['PORT_202306'], df['ProvisionB']))
    #Ing no financiero teorico
    df['IxS_202306']=list(map(corte_portafolio, df['PORT_202306'], df['IxS']))

    df = df[['CODCLAVEOPECTA','COSECHA','PORT_202306','MTODESEMBOLSADO','Saldo_202306','IF_202306']]
       


    return df
# %%
df1 = Portafolio_Teorico(df)
# %%
print(aggr_sum(df1['Saldo_202306']))
# %%
