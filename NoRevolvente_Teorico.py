import numpy as np
import pandas as pd
import Funciones_apoyo as fn

#creación de la clase
class NoRevolventeTeorico():
    #constructor del objeto
    def __init__(self,csvpd=None,csvcan=None,csvpre=None,mincosecha='',maxcosecha=''): #se insume un documento de Excel
        
        #tranformar la data de las hojas del excel en dataframes
        df_pd = pd.read_csv(csvpd)
        df_can = pd.read_csv(csvcan)
        df_pre = pd.read_csv(csvpre)
        
        #colocar las curvas en una sola celda
        df_pd['pd_marginal'] = pd.DataFrame({'pd':df_pd.iloc[:,fn.encontrar_encabezado(df_pd,1):].values.tolist()})
        df_can['can_marginal'] = pd.DataFrame({'pd':df_can.iloc[:,fn.encontrar_encabezado(df_can,1):].values.tolist()})
        df_pre['pre_marginal'] = pd.DataFrame({'pd':df_pre.iloc[:,fn.encontrar_encabezado(df_pre,1):].values.tolist()})
 
        #seleccionar solo la data relevante
        df_pd = df_pd[fn.all_cortes(df_pd)+['CODSOLICITUD','COSECHA','maxmad','pd_marginal']]
        df_can = df_can[fn.all_cortes(df_can)+['CODSOLICITUD','COSECHA','maxmad','can_marginal']]
        df_pre = df_pre[fn.all_cortes(df_pre)+['CODSOLICITUD','COSECHA','maxmad','pre_marginal']]
        
        if mincosecha!='':
            df_pd = df_pd[df_pd['COSECHA']>=mincosecha]
            df_can = df_can[df_can['COSECHA']>=mincosecha]
            df_pre = df_pre[df_pre['COSECHA']>=mincosecha]
        if maxcosecha!='':
            df_pd = df_pd[df_pd['COSECHA']<=maxcosecha]
            df_can = df_can[df_can['COSECHA']<=maxcosecha]
            df_pre = df_pre[df_pre['COSECHA']<=maxcosecha]
        self.df_pd = df_pd
        self.df_can = df_can
        self.df_pre = df_pre
        
        
    #creación de los cortes
    def condensar(self,cortes=[]): #se insume una lista con los cortes que se desea
        
        #si no se ingresa cortes espécificos, se usan todos
        if cortes==[]:
            self.df_pd['c_todos']=''
            self.df_can['c_todos']=''
            self.df_pre['c_todos']=''
            cortes=['c_todos']

        #Creamos la 'plantilla'
        curvas = self.df_pd.groupby(cortes).size().reset_index().rename(columns={0:'recuento'})
        curvas['pd_teorico'] = ''
        curvas['can_teorico'] = ''
        curvas['pre_teorico'] = ''
        
        #TEÓRICOS
        for i in range(len(curvas)):
            
            #pd teórico
            temp = pd.merge(self.df_pd[cortes+['CODSOLICITUD','COSECHA','maxmad','pd_marginal']], pd.DataFrame([curvas.loc[i,:]]), left_on=cortes, right_on=cortes, how='inner')
            temp['result'] = list(map(fn.operation_pd, temp['maxmad'], temp['pd_marginal']))
            resultado = fn.aggr_avg(temp['result'])
            resultado = np.cumsum(resultado)  
            curvas.at[i,'pd_teorico'] = fn.porcentaje(resultado)
            
            #cancelaciones teórico
            temp = pd.merge(self.df_can[cortes+['CODSOLICITUD','COSECHA','maxmad','can_marginal']], pd.DataFrame([curvas.loc[i,:]]), left_on=cortes, right_on=cortes, how='inner')
            temp['result']=list(map(fn.operation_pd, temp['maxmad'], temp['can_marginal']))
            resultado = fn.aggr_avg(temp['result'])
            resultado = np.cumsum(resultado)   
            curvas.at[i,'can_teorico'] = fn.porcentaje(resultado)
            
            #prepagos teórico
            temp = pd.merge(self.df_pre[cortes+['CODSOLICITUD','COSECHA','maxmad','pre_marginal']], pd.DataFrame([curvas.loc[i,:]]), left_on=cortes, right_on=cortes, how='inner')
            temp['result']=list(map(fn.operation_pd, temp['maxmad'], temp['pre_marginal']))
            resultado = fn.aggr_avg(temp['result'])
            resultado = np.cumsum(resultado)
            curvas.at[i,'pre_teorico'] = fn.porcentaje(resultado)

        self.curvas = curvas