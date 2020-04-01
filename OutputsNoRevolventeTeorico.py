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
    def __init__(self,csvif=None,csvef=None,csvsaldo=None,mincosecha='',maxcosecha=''): #se insume un documento de Excel
        
        #tranformar la data de las hojas del excel en dataframes
        df_if = pd.read_csv(csvif)
        df_ef = pd.read_csv(csvef)
        df_saldo = pd.read_csv(csvsaldo)
        
        #colocar las curvas en una sola celda
        df_if['if'] = pd.DataFrame({'pd':df_if.iloc[:,f.encontrar_encabezado(df_if,1):].values.tolist()})
        df_ef['ef'] = pd.DataFrame({'pd':df_ef.iloc[:,f.encontrar_encabezado(df_ef,1):].values.tolist()})
        df_saldo['saldo'] = pd.DataFrame({'pd':df_saldo.iloc[:,f.encontrar_encabezado(df_saldo,1):].values.tolist()})
 
        #seleccionar solo la data relevante
        df_if = df_if[f.all_cortes(df_if)+['CODSOLICITUD','COSECHA','maxmad','if']]
        df_ef = df_ef[f.all_cortes(df_ef)+['CODSOLICITUD','COSECHA','maxmad','ef']]
        df_saldo = df_saldo[f.all_cortes(df_saldo)+['CODSOLICITUD','COSECHA','maxmad','saldo']]
        if mincosecha!='':
            df_if = df_if[df_if['COSECHA']>=mincosecha]
            df_ef = df_ef[df_ef['COSECHA']>=mincosecha]
            df_saldo = df_saldo[df_saldo['COSECHA']>=mincosecha]
        if maxcosecha!='':
            df_if = df_if[df_if['COSECHA']<=maxcosecha]
            df_ef = df_ef[df_ef['COSECHA']<=maxcosecha]
            df_saldo = df_saldo[df_saldo['COSECHA']<=maxcosecha]
        self.df_if = df_if
        self.df_ef = df_ef
        self.df_saldo = df_saldo
        
        
    #creación de los cortes
    def condensar(self,cortes=[]): #se insume una lista con los cortes que se desea
        
        #si no se ingresa cortes espécificos, se usan todos
        if cortes==[]:
            self.df_if['c_todos']=''
            self.df_ef['c_todos']=''
            self.df_saldo['c_todos']=''
            cortes=['c_todos']

        #Creamos la 'plantilla'
        curvas = self.df_if.groupby(cortes).size().reset_index().rename(columns={0:'recuento'})
        curvas['if_teorico'] = ''
        curvas['ef_teorico'] = ''
        curvas['saldo_teorico'] = ''
        
        ratios = self.df_if.groupby(cortes).size().reset_index().rename(columns={0:'recuento'})
        ratios['r_if_teorico'] = ''
        ratios['r_ef_teorico'] = ''
        ratios['r_spread_teorico'] = ''
        
        #TEÓRICAS
        for i in range(len(curvas)):
            
            #IF teórico
            temp = pd.merge(self.df_if[cortes+['CODSOLICITUD','COSECHA','maxmad','if']], pd.DataFrame([curvas.loc[i,:]]), left_on=cortes, right_on=cortes, how='inner')
            temp['result'] = list(map(f.operation_pd, temp['maxmad'], temp['if']))
            a = f.aggr_sum(temp['result'])
            
            #EF teórico
            temp = pd.merge(self.df_ef[cortes+['CODSOLICITUD','COSECHA','maxmad','ef']], pd.DataFrame([curvas.loc[i,:]]), left_on=cortes, right_on=cortes, how='inner')
            temp['result']=list(map(f.operation_pd, temp['maxmad'], temp['ef']))
            b = f.aggr_sum(temp['result'])
            
            #SALDO teórico
            temp = pd.merge(self.df_saldo[cortes+['CODSOLICITUD','COSECHA','maxmad','saldo']], pd.DataFrame([curvas.loc[i,:]]), left_on=cortes, right_on=cortes, how='inner')
            temp['result']=list(map(f.operation_pd, temp['maxmad'], temp['saldo']))
            c = f.aggr_sum(temp['result'])
            
            curvas.at[i,'if_teorico'] = [round(x,0) for x in a]
            curvas.at[i,'ef_teorico'] = [round(x,0) for x in b]
            curvas.at[i,'saldo_teorico'] = [round(x,0) for x in c]
            
            ratios.at[i,'r_if_teorico'] = round((1+(sum(a)/sum(c)))**12-1,6)*100
            ratios.at[i,'r_ef_teorico'] = round((1+(sum(b)/sum(c)))**12-1,6)*100
            ratios.at[i,'r_apread_teorico'] = round((1+((sum(a)+sum(b))/sum(c)))**12-1,6)*100

        self.curvas = curvas
        self.ratios = ratios