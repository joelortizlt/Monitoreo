import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import Funciones_apoyo as fn

#creación de la clase

class NoRevolvente():
    #constructor del objeto
    def __init__(self,NRR,NRT): #se insumen 2 objetos (uno real y uno teorico)
        curvas = pd.merge(left=NRR.curvas, right=NRT.curvas, how='left', left_on=fn.all_cortes(NRR.curvas), right_on=fn.all_cortes(NRT.curvas))
        curvas['check']=curvas['recuento_x']-curvas['recuento_y']
        curvas = curvas.rename(columns={'recuento_x':'recuento'}).drop('recuento_y',1)
        
        stats = curvas[fn.all_cortes(curvas)+['recuento']].copy()
        
        for i in range(len(curvas)):
            
            l=min(len(curvas.loc[i, 'pd_real']),len(curvas.loc[i, 'pd_teorico']))
            curvas.at[i, 'pd_real']=curvas.loc[i, 'pd_real'].copy()[:l]
            curvas.at[i, 'pd_teorico']=curvas.loc[i, 'pd_teorico'].copy()[:l]
            stats.at[i,'MAE_pd'] = mean_absolute_error(curvas.loc[i, 'pd_real'], curvas.loc[i, 'pd_teorico'])
            
            l=min(len(curvas.loc[i, 'can_real']),len(curvas.loc[i, 'can_teorico']))
            curvas.at[i, 'can_real']=curvas.loc[i, 'can_real'].copy()[:l]
            curvas.at[i, 'can_teorico']=curvas.loc[i, 'can_teorico'].copy()[:l]
            stats.at[i,'MAE_can'] = mean_absolute_error(curvas.loc[i, 'can_real'], curvas.loc[i, 'can_teorico']) 
            
            l=min(len(curvas.loc[i, 'pre_real']),len(curvas.loc[i, 'pre_teorico']))
            curvas.at[i, 'pre_real']=curvas.loc[i, 'pre_real'].copy()[:l]
            curvas.at[i, 'pre_teorico']=curvas.loc[i, 'pre_teorico'].copy()[:l]
            stats.at[i,'MAE_pre'] = mean_absolute_error(curvas.loc[i, 'pre_real'], curvas.loc[i, 'pre_teorico']) 

        self.curvas = curvas
        self.stats = stats
    
    
    def plotear(self,texto,optimo=False):
        cortes_temp = fn.all_cortes(self.curvas)
        for i in range(len(self.curvas)):
            z=[]
            for j in range(len(self.curvas[texto+'_real'][i])):
                z.append(j+1)
            a=''
            for j in cortes_temp:
                a=a+str(j)[2:]+' '+str(self.curvas[j][i])+' y '
                
            plt.xlabel('Periodo', fontsize=12)
            plt.ylabel(texto, fontsize=12)
            plt.title(texto+': curva real vs. teórica para '+a[0:-3], fontsize=16)
            r = self.curvas[texto+'_real'][i]
            plt.plot(z,r,label = 'real')
            t = self.curvas[texto+'_teorico'][i]
            plt.plot(z,t,label = 'teórica')
            if optimo:
                o = self.curvas[texto+'_optimo'][i]
                plt.plot(z,o,label = 'óptima')
            plt.plot(0)
            plt.legend(fontsize=10)
            plt.show()
    
    
    def MAE(self,texto,optimo=False):
        temp = self.stats.sort_values(by=['MAE_'+texto], ascending=True)
        temp = temp.reset_index()
        cortes_temp = fn.all_cortes(self.stats)
        
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
        
        self.curvas['pd_optimo'] = ''
        self.curvas['can_optimo'] = ''
        self.curvas['pre_optimo'] = ''
        
        for i in range(len(self.stats)):
            
            minMAE = self.stats.loc[i, 'MAE_pd'].copy()
            scalarMAE = 1
            for s in np.arange(0,2,step):
                x = self.curvas.loc[i, 'pd_real'].copy()
                y = self.curvas.loc[i, 'pd_teorico'].copy()
                z = []
                for k in range(len(y)):
                    z.append(y[k]*s)
                tempMAE = mean_absolute_error(x, z)
                if tempMAE <= minMAE:
                    minMAE = tempMAE
                    scalarMAE = s
                    ypd = z
            self.stats.at[i,'MAEop_pd'] = minMAE
            temppd = scalarMAE
            
            minMAE = self.stats.loc[i, 'MAE_can'].copy()
            scalarMAE = 1
            for s in np.arange(0,2,step):
                x = self.curvas.loc[i, 'can_real'].copy()
                y = self.curvas.loc[i, 'can_teorico'].copy()
                z = []
                for k in range(len(y)):
                    z.append(y[k]*s)
                tempMAE = mean_absolute_error(x, z)
                if tempMAE <= minMAE:
                    minMAE = tempMAE
                    scalarMAE = s
                    ycan = z
            self.stats.at[i,'MAEop_can'] = minMAE
            tempcan = scalarMAE

            minMAE = self.stats.loc[i, 'MAE_can'].copy()
            scalarMAE = 1
            for s in np.arange(0,2,step):
                x = self.curvas.loc[i, 'pre_real'].copy()
                y = self.curvas.loc[i, 'pre_teorico'].copy()
                z = []
                for k in range(len(y)):
                    z.append(y[k]*s)
                tempMAE = mean_absolute_error(x, z)
                if tempMAE <= minMAE:
                    minMAE = tempMAE
                    scalarMAE = s
                    ypre = z
            self.stats.at[i,'MAEop_pre'] = minMAE
            temppre = scalarMAE
            
            self.stats.at[i,'scalar_pd'] = temppd
            self.stats.at[i,'scalar_can'] = tempcan
            self.stats.at[i,'scalar_pre'] = temppre
            
            self.curvas.at[i,'pd_optimo'] = [round(x,4) for x in ypd]
            self.curvas.at[i,'can_optimo'] = [round(x,4) for x in ycan]
            self.curvas.at[i,'pre_optimo'] = [round(x,4) for x in ypre]