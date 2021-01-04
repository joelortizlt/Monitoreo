#Se impoortan la librerías necesarias
import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error

from source.engine import funciones as f
from source.engine.OutputsNoRevolventeReal import OutputsNoRevolventeReal
from source.engine.OutputsNoRevolventeTeorico import OutputsNoRevolventeTeorico


#creación de la clase
class OutputsNoRevolvente(OutputsNoRevolventeReal,OutputsNoRevolventeTeorico):
    #constructor del objeto
    def __init__(self,df_real,df_teorico,mincosecha='',maxcosecha='',completar=True):
        if completar==True:
            izquierda = df_real[['CODCLAVEOPECTA','COSECHA','MAXMADPYG','MTODESEMBOLSADO']+f.all_cortes(df_real)].copy()
            df_teorico = pd.merge(left=izquierda, right=df_teorico, how='inner', left_on=['CODCLAVEOPECTA'], right_on=['CODCLAVEOPECTA'])

            izquierda = df_teorico[['CODCLAVEOPECTA']].copy()
            df_real = pd.merge(left=izquierda, right=df_real, how='inner', left_on=['CODCLAVEOPECTA'], right_on=['CODCLAVEOPECTA'])
        
        OutputsNoRevolventeReal.__init__(self,df=df_real,mincosecha=mincosecha,maxcosecha=maxcosecha)
        OutputsNoRevolventeTeorico.__init__(self,df=df_teorico,mincosecha=mincosecha,maxcosecha=maxcosecha)


    def condensar(self,cortes=[]):

        OutputsNoRevolventeReal.condensar(self,cortes)
        OutputsNoRevolventeTeorico.condensar(self,cortes)

        curvas = pd.merge(left=self.curvasR, right=self.curvasT, how='left', left_on=f.all_cortes(self.curvasR), right_on=f.all_cortes(self.curvasT))

        curvas = curvas.rename(columns={'recuento_x':'recuento'}).drop('recuento_y',1)
        curvas = curvas.rename(columns={'monto_x':'monto'}).drop('monto_y',1)
        ratios = curvas[f.all_cortes(curvas)+['recuento','monto']].copy()
        niveles = curvas[f.all_cortes(curvas)+['recuento','monto']].copy()
        
        for i in range(len(curvas)):
            
            l=min(len(curvas.loc[i, 'if_real']),len(curvas.loc[i, 'if_teorico']))
            curvas.at[i, 'if_real']=curvas.loc[i, 'if_real'].copy()[:l]
            curvas.at[i, 'if_teorico']=curvas.loc[i, 'if_teorico'].copy()[:l]
            
            l=min(len(curvas.loc[i, 'ef_real']),len(curvas.loc[i, 'ef_teorico']))
            curvas.at[i, 'ef_real']=curvas.loc[i, 'ef_real'].copy()[:l]
            curvas.at[i, 'ef_teorico']=curvas.loc[i, 'ef_teorico'].copy()[:l]

            #l=min(len(curvas.loc[i, 'pe_real']),len(curvas.loc[i, 'pe_teorico']))
            #curvas.at[i, 'pe_real']=curvas.loc[i, 'pe_real'].copy()[:l]
            #curvas.at[i, 'pe_teorico']=curvas.loc[i, 'pe_teorico'].copy()[:l]
            
            l=min(len(curvas.loc[i, 'saldo_real']),len(curvas.loc[i, 'saldo_teorico']))
            curvas.at[i, 'saldo_real']=curvas.loc[i, 'saldo_real'].copy()[:l]
            curvas.at[i, 'saldo_teorico']=curvas.loc[i, 'saldo_teorico'].copy()[:l]

            ratios.at[i,'r_if_real'] = round(((sum(curvas.loc[i, 'if_real'])/sum(curvas.loc[i, 'saldo_real'])))*12,6)*100
            ratios.at[i,'r_ef_real'] = round(((sum(curvas.loc[i, 'ef_real'])/sum(curvas.loc[i, 'saldo_real'])))*12,6)*100
            ratios.at[i,'r_spread_bruto_real'] = ratios.at[i,'r_if_real']-ratios.at[i,'r_ef_real']
            #ratios.at[i,'r_pe_real'] = round(((sum(curvas.loc[i, 'pe_real'])/sum(curvas.loc[i, 'saldo_real'])))*12,6)*100
            #ratios.at[i,'r_spread_neto_real'] = ratios.at[i,'r_spread_bruto_real']-ratios.at[i,'r_pe_real']
            
            ratios.at[i,'r_if_teorico'] = round(((sum(curvas.loc[i, 'if_teorico'])/sum(curvas.loc[i, 'saldo_teorico'])))*12,6)*100
            ratios.at[i,'r_ef_teorico'] = round(((sum(curvas.loc[i, 'ef_teorico'])/sum(curvas.loc[i, 'saldo_teorico'])))*12,6)*100
            ratios.at[i,'r_spread_bruto_teorico'] = ratios.at[i,'r_if_teorico']-ratios.at[i,'r_ef_teorico']
            #ratios.at[i,'r_pe_teorico'] = round(((sum(curvas.loc[i, 'pe_teorico'])/sum(curvas.loc[i, 'saldo_teorico'])))*12,6)*100
            #ratios.at[i,'r_spread_neto_teorico'] = ratios.at[i,'r_spread_bruto_teorico']-ratios.at[i,'r_pe_teorico']

            niveles.at[i,'n_if_real'] = round(sum(curvas.loc[i, 'if_real']),0)
            niveles.at[i,'n_ef_real'] = round(sum(curvas.loc[i, 'ef_real']),0)
            #niveles.at[i,'n_pe_real'] = round(sum(curvas.loc[i, 'pe_real']),0)
            niveles.at[i,'n_saldo_real'] = round(sum(curvas.loc[i, 'saldo_real']),0)
            
            niveles.at[i,'n_if_teorico'] = round(sum(curvas.loc[i, 'if_teorico']),0)
            niveles.at[i,'n_ef_teorico'] = round(sum(curvas.loc[i, 'ef_teorico']),0)
            #niveles.at[i,'n_pe_teorico'] = round(sum(curvas.loc[i, 'pe_teorico']),0)
            niveles.at[i,'n_saldo_teorico'] = round(sum(curvas.loc[i, 'saldo_teorico']),0)

        self.curvas = curvas
        self.ratios = ratios
        self.niveles = niveles
    
    def plotear(self,texto):
        cortes_temp = f.all_cortes(self.curvas)
        for i in range(len(self.curvas)):
            z=[]
            for j in range(len(self.curvas[texto+'_real'][i])):
                z.append(j+1)
            a=''
            for j in cortes_temp:
                a=a+str(j)[2:]+' '+str(self.curvas[j][i])+' y '
                
            plt.xlabel('Periodo', fontsize=12)
            plt.ylabel(texto, fontsize=12)
            plt.title(texto+': curva real vs. teórico para '+a[0:-3], fontsize=16)
            r = self.curvas[texto+'_real'][i]
            plt.plot(z,r,label = 'real')
            t = self.curvas[texto+'_teorico'][i]
            plt.plot(z,t,label = 'teórico')
            plt.plot(0)
            plt.legend(fontsize=10)
            plt.show()
    
    
    
