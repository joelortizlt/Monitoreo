#Se impoortan la librerías necesarias
import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import funciones as f
from OutputsNoRevolventeReal import OutputsNoRevolventeReal
from OutputsNoRevolventeTeorico import OutputsNoRevolventeTeorico


#creación de la clase
class OutputsNoRevolvente(OutputsNoRevolventeReal,OutputsNoRevolventeTeorico):
    #constructor del objeto
    def __init__(self,df_real,df_teorico,mincosecha='',maxcosecha='',completar=True):
        if completar==True:
            izquierda = df_real[['CODCLAVEOPECTA','COSECHA','MAXMADPYG']+f.all_cortes(df_real)].copy()
            df_teorico = pd.merge(left=izquierda, right=df_teorico, how='inner', left_on=['CODCLAVEOPECTA'], right_on=['CODCLAVEOPECTA'])
        
        OutputsNoRevolventeReal.__init__(self,df=df_real,mincosecha=mincosecha,maxcosecha=maxcosecha)
        OutputsNoRevolventeTeorico.__init__(self,df=df_teorico,mincosecha=mincosecha,maxcosecha=maxcosecha)


    def condensar(self,cortes=[]):

        OutputsNoRevolventeReal.condensar(self,cortes)
        OutputsNoRevolventeTeorico.condensar(self,cortes)

        curvas = pd.merge(left=self.curvasR, right=self.curvasT, how='left', left_on=f.all_cortes(self.curvasR), right_on=f.all_cortes(self.curvasT))

        curvas = curvas.rename(columns={'recuento_x':'recuento'}).drop('recuento_y',1)
        ratios = curvas[f.all_cortes(curvas)+['recuento']].copy()
        
        for i in range(len(curvas)):
            
            l=min(len(curvas.loc[i, 'if_real']),len(curvas.loc[i, 'if_teorico']))
            curvas.at[i, 'if_real']=curvas.loc[i, 'if_real'].copy()[:l]
            curvas.at[i, 'if_teorico']=curvas.loc[i, 'if_teorico'].copy()[:l]
            
            l=min(len(curvas.loc[i, 'ef_real']),len(curvas.loc[i, 'ef_teorico']))
            curvas.at[i, 'ef_real']=curvas.loc[i, 'ef_real'].copy()[:l]
            curvas.at[i, 'ef_teorico']=curvas.loc[i, 'ef_teorico'].copy()[:l]
            
            l=min(len(curvas.loc[i, 'saldo_real']),len(curvas.loc[i, 'saldo_teorico']))
            curvas.at[i, 'saldo_real']=curvas.loc[i, 'saldo_real'].copy()[:l]
            curvas.at[i, 'saldo_teorico']=curvas.loc[i, 'saldo_teorico'].copy()[:l]
                  
            ratios.at[i,'r_if_real'] = round((1+(sum(curvas.loc[i, 'if_real'])/sum(curvas.loc[i, 'saldo_real'])))**12-1,6)*100
            ratios.at[i,'r_ef_real'] = round((1+(sum(curvas.loc[i, 'ef_real'])/sum(curvas.loc[i, 'saldo_real'])))**12-1,6)*100
            ratios.at[i,'r_spread_real'] = round((1+((sum(curvas.loc[i, 'if_real'])-sum(curvas.loc[i, 'ef_real']))/sum(curvas.loc[i, 'saldo_real'])))**12-1,6)*100
            
            ratios.at[i,'r_if_teorico'] = round((1+(sum(curvas.loc[i, 'if_teorico'])/sum(curvas.loc[i, 'saldo_teorico'])))**12-1,6)*100
            ratios.at[i,'r_ef_teorico'] = round((1+(sum(curvas.loc[i, 'ef_teorico'])/sum(curvas.loc[i, 'saldo_teorico'])))**12-1,6)*100
            ratios.at[i,'r_apread_teorico'] = round((1+((sum(curvas.loc[i, 'if_teorico'])-sum(curvas.loc[i, 'ef_teorico']))/sum(curvas.loc[i, 'saldo_teorico'])))**12-1,6)*100
            
        self.curvas = curvas
        self.ratios = ratios
    
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
    
    
    
