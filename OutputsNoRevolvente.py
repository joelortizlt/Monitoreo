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
            izquierda = df_real[['CODCLAVEOPECTA','COSECHA','MAXMAD']+f.all_cortes(df_real)].copy()
            df_teorico = pd.merge(left=izquierda, right=df_teorico, how='inner', left_on=['CODCLAVEOPECTA'], right_on=['CODCLAVEOPECTA'])
        
        OutputsNoRevolventeReal.__init__(self,df=df_real,mincosecha=mincosecha,maxcosecha=maxcosecha)
        OutputsNoRevolventeTeorico.__init__(self,df=df_teorico,mincosecha=mincosecha,maxcosecha=maxcosecha)


    def condensar(self,cortes=[]):

        OutputsNoRevolventeReal.condensar(self,cortes)
        OutputsNoRevolventeTeorico.condensar(self,cortes)

        curvas = pd.merge(left=self.curvasR, right=self.curvasT, how='left', left_on=f.all_cortes(self.curvasR), right_on=f.all_cortes(self.curvasT))
        curvas['check']=curvas['recuento_x']-curvas['recuento_y']
        curvas = curvas.rename(columns={'recuento_x':'recuento'}).drop('recuento_y',1)
        ratios = curvas[f.all_cortes(curvas)+['recuento']].copy()
        stats = curvas[f.all_cortes(curvas)+['recuento']].copy()
        
        for i in range(len(curvas)):
            
            l=min(len(curvas.loc[i, 'if_real']),len(curvas.loc[i, 'if_teorico']))
            curvas.at[i, 'if_real']=curvas.loc[i, 'if_real'].copy()[:l]
            curvas.at[i, 'if_teorico']=curvas.loc[i, 'if_teorico'].copy()[:l]
            stats.at[i, 'MAE_if'] = mean_absolute_error(curvas.loc[i, 'if_real'], curvas.loc[i, 'if_teorico'])
            
            l=min(len(curvas.loc[i, 'ef_real']),len(curvas.loc[i, 'ef_teorico']))
            curvas.at[i, 'ef_real']=curvas.loc[i, 'ef_real'].copy()[:l]
            curvas.at[i, 'ef_teorico']=curvas.loc[i, 'ef_teorico'].copy()[:l]
            stats.at[i, 'MAE_ef'] = mean_absolute_error(curvas.loc[i, 'ef_real'], curvas.loc[i, 'ef_teorico']) 
            
            l=min(len(curvas.loc[i, 'saldo_real']),len(curvas.loc[i, 'saldo_teorico']))
            curvas.at[i, 'saldo_real']=curvas.loc[i, 'saldo_real'].copy()[:l]
            curvas.at[i, 'saldo_teorico']=curvas.loc[i, 'saldo_teorico'].copy()[:l]
            stats.at[i, 'MAE_saldo'] = mean_absolute_error(curvas.loc[i, 'saldo_real'], curvas.loc[i, 'saldo_teorico']) 
                  
            ratios.at[i,'r_if_real'] = round((1+(sum(curvas.loc[i, 'if_real'])/sum(curvas.loc[i, 'saldo_real'])))**12-1,6)*100
            ratios.at[i,'r_ef_real'] = round((1+(sum(curvas.loc[i, 'ef_real'])/sum(curvas.loc[i, 'saldo_real'])))**12-1,6)*100
            ratios.at[i,'r_spread_real'] = round((1+((sum(curvas.loc[i, 'if_real'])+sum(curvas.loc[i, 'ef_real']))/sum(curvas.loc[i, 'saldo_real'])))**12-1,6)*100
            
            ratios.at[i,'r_if_teorico'] = round((1+(sum(curvas.loc[i, 'if_teorico'])/sum(curvas.loc[i, 'saldo_teorico'])))**12-1,6)*100
            ratios.at[i,'r_ef_teorico'] = round((1+(sum(curvas.loc[i, 'ef_teorico'])/sum(curvas.loc[i, 'saldo_teorico'])))**12-1,6)*100
            ratios.at[i,'r_apread_teorico'] = round((1+((sum(curvas.loc[i, 'if_teorico'])+sum(curvas.loc[i, 'ef_teorico']))/sum(curvas.loc[i, 'saldo_teorico'])))**12-1,6)*100
            
        self.curvas = curvas
        self.ratios = ratios
        self.stats = stats
    
    
    def plotear(self,texto,optimo=False):
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
            if optimo:
                o = self.curvas[texto+'_optimo'][i]
                plt.plot(z,o,label = 'óptimo')
            plt.plot(0)
            plt.legend(fontsize=10)
            plt.show()
    
    
    
    def MAE(self,texto,optimo=False):
        temp = self.stats.sort_values(by=['MAE_'+texto], ascending=True)
        temp = temp.reset_index()
        cortes_temp = f.all_cortes(self.stats)
        
        values=temp['MAE_'+texto] #1
        if optimo==True:
            values2=temp['MAEop_'+texto]
            
        description = [] #2
        for i in range(len(temp)):
            a=''
            for j in cortes_temp:
                a=a+str(j)[2:]+' '+str(temp[j][i])+'; '
            description.append(a[0:-2])
        position = np.arange(len(description)) #3
            
        bar1 = plt.barh(position,values,color='orange',edgecolor='black',height=0.5,label='MAE')
        if optimo==True:
            bar2 = plt.barh(position,values2,color='blue',edgecolor='black',height=0.5,label='MAE óptimo')
        plt.yticks(position, description, fontsize=12)
        plt.xticks(fontsize=12)
        plt.xlabel('MAE', fontsize=12)
        plt.ylabel('Grupo', fontsize=12)
        plt.title(texto+': MAE por grupos',fontsize=16)
        plt.legend()
        plt.show()
    
    
    
    def optimizar(self,step=0.01):
        
        self.curvas['if_optimo'] = ''
        self.curvas['ef_optimo'] = ''
        self.curvas['saldo_optimo'] = ''
        self.stats['MAEop_if'] = ''
        self.stats['MAEop_ef'] = ''
        self.stats['MAEop_saldo'] = ''
        
        for i in range(len(self.stats)):
            
            minMAE = self.stats.loc[i, 'MAE_if'].copy()
            scalarMAE = 1
            x = self.curvas.loc[i, 'if_real'].copy()
            y = self.curvas.loc[i, 'if_teorico'].copy()
            for s in np.arange(0,2,step):
                z = []
                for k in range(len(y)):
                    z.append(y[k]*s)
                tempMAE = mean_absolute_error(x, z)
                if tempMAE <= minMAE:
                    minMAE = tempMAE
                    scalarMAE = s
                    yopt = z
            if scalarMAE==0:
                minMAE = mean_absolute_error(x, y)
                scalarMAE = 1
                yopt = y
            self.stats.at[i,'MAEop_if'] = minMAE
            self.stats.at[i,'scalar_if'] = scalarMAE
            self.curvas.at[i,'if_optimo'] = [round(x,4) for x in yopt]

            
            minMAE = self.stats.loc[i, 'MAE_ef'].copy()
            scalarMAE = 1
            x = self.curvas.loc[i, 'ef_real'].copy()
            y = self.curvas.loc[i, 'ef_teorico'].copy()
            for s in np.arange(0,2,step):
                z = []
                for k in range(len(y)):
                    z.append(y[k]*s)
                tempMAE = mean_absolute_error(x, z)
                if tempMAE <= minMAE:
                    minMAE = tempMAE
                    scalarMAE = s
                    yopt = z
            if scalarMAE==0:
                minMAE = mean_absolute_error(x, y)
                scalarMAE = 1
                yopt = y
            self.stats.at[i,'MAEop_ef'] = minMAE
            self.stats.at[i,'scalar_ef'] = scalarMAE
            self.curvas.at[i,'ef_optimo'] = [round(x,4) for x in yopt]


            minMAE = self.stats.loc[i, 'MAE_saldo'].copy()
            scalarMAE = 1
            x = self.curvas.loc[i, 'saldo_real'].copy()
            y = self.curvas.loc[i, 'saldo_teorico'].copy()
            for s in np.arange(0,2,step):
                z = []
                for k in range(len(y)):
                    z.append(y[k]*s)
                tempMAE = mean_absolute_error(x, z)
                if tempMAE <= minMAE:
                    minMAE = tempMAE
                    scalarMAE = s
                    yopt = z
            if scalarMAE==0:
                minMAE = mean_absolute_error(x, y)
                scalarMAE = 1
                yopt = y
            self.stats.at[i,'MAEop_saldo'] = minMAE
            self.stats.at[i,'scalar_saldo'] = scalarMAE
            self.curvas.at[i,'saldo_optimo'] = [round(x,4) for x in yopt]