import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import funciones as f

class MonitoreoNoRevolvente():
    #constructor del objeto
    def __init__(self,NRR,NRT): #se insumen 2 objetos (uno real y uno teorico)
        curvas = pd.merge(left=NRR.curvas, right=NRT.curvas, how='left', left_on=f.all_cortes(NRR.curvas), right_on=f.all_cortes(NRT.curvas))
        curvas['check']=curvas['recuento_x']-curvas['recuento_y']
        curvas = curvas.rename(columns={'recuento_x':'recuento'}).drop('recuento_y',1)
        
        stats = curvas[f.all_cortes(curvas)+['recuento']].copy()
        
        for i in range(len(curvas)):
            
            l=min(len(curvas.loc[i, "pd_real"]),len(curvas.loc[i, "pd_teorica"]))
            curvas.at[i, "pd_real"]=curvas.loc[i, "pd_real"].copy()[:l]
            curvas.at[i, "pd_teorica"]=curvas.loc[i, "pd_teorica"].copy()[:l]
            stats.at[i,'MAE_pd'] = mean_absolute_error(curvas.loc[i, "pd_real"], curvas.loc[i, "pd_teorica"])
            
            l=min(len(curvas.loc[i, "can_real"]),len(curvas.loc[i, "can_teorica"]))
            curvas.at[i, "can_real"]=curvas.loc[i, "can_real"].copy()[:l]
            curvas.at[i, "can_teorica"]=curvas.loc[i, "can_teorica"].copy()[:l]
            stats.at[i,'MAE_can'] = mean_absolute_error(curvas.loc[i, "can_real"], curvas.loc[i, "can_teorica"]) 
            
            l=min(len(curvas.loc[i, "pre_real"]),len(curvas.loc[i, "pre_teorica"]))
            curvas.at[i, "pre_real"]=curvas.loc[i, "pre_real"].copy()[:l]
            curvas.at[i, "pre_teorica"]=curvas.loc[i, "pre_teorica"].copy()[:l]
            stats.at[i,'MAE_pre'] = mean_absolute_error(curvas.loc[i, "pre_real"], curvas.loc[i, "pre_teorica"]) 

        self.curvas = curvas
        self.stats = stats
    
    def plotear(self,texto,optima=False):
        cortes_temp = f.all_cortes(self.curvas)
        for i in range(len(self.curvas)):
            z=[]
            for j in range(len(self.curvas[texto+"_real"][i])):
                z.append(j+1)
            a=""
            for j in cortes_temp:
                a=a+str(j)[2:]+' '+str(self.curvas[j][i])+' y '
                
            plt.xlabel('Periodo', fontsize=12)
            plt.ylabel(texto, fontsize=12)
            plt.title(texto+': curva real vs. teórica para '+a[0:-3], fontsize=16)
            r = self.curvas[texto+"_real"][i]
            plt.plot(z,r,label = 'real')
            t = self.curvas[texto+"_teorica"][i]
            plt.plot(z,t,label = 'teórica')
            if optima:
                o = self.curvas[texto+"_optima"][i]
                plt.plot(z,o,label = 'óptima')
            plt.plot(0)
            plt.legend(fontsize=10)
            plt.show()
    
    def MAE(self,texto):
        temp = self.stats.sort_values(by=["MAE_"+texto], ascending=True)
        temp = temp.reset_index()
        cortes_temp = f.all_cortes(self.stats)
            
        values=temp["MAE_"+texto] #1
        description = [] #2
        for i in range(len(temp)):
            a=""
            for j in cortes_temp:
                a=a+str(j)[2:]+' '+str(temp[j][i])+'; '
            description.append(a[0:-2])
        position = np.arange(len(description)) #3
            
        plt.barh(position,values,color='orange',edgecolor='black',height=0.75)
        plt.yticks(position, description, fontsize=7)
        plt.xlabel('MAE', fontsize=12)
        plt.ylabel('Grupo', fontsize=12)
        plt.title(texto+': MAE por grupos',fontsize=16)
        #plt.figure(figsize=(10,20))
        plt.show()
    
    def optimizar(self):
        
        self.curvas['pd_optima'] = ''
        self.curvas['can_optima'] = ''
        self.curvas['pre_optima'] = ''
        
        for i in range(len(self.stats)):
            
            minMAE = self.stats.loc[i, "MAE_pd"].copy()
            scalarMAE = 1
            for s in np.arange(0,5,0.01):
                x = self.curvas.loc[i, "pd_real"].copy()
                y = self.curvas.loc[i, "pd_teorica"].copy()
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
            
            minMAE = self.stats.loc[i, "MAE_can"].copy()
            scalarMAE = 1
            for s in np.arange(0,5,0.01):
                x = self.curvas.loc[i, "can_real"].copy()
                y = self.curvas.loc[i, "can_teorica"].copy()
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

            minMAE = self.stats.loc[i, "MAE_can"].copy()
            scalarMAE = 1
            for s in np.arange(0,5,0.01):
                x = self.curvas.loc[i, "pre_real"].copy()
                y = self.curvas.loc[i, "pre_teorica"].copy()
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
            
            self.curvas.at[i,'pd_optima'] = [round(x,4) for x in ypd]
            self.curvas.at[i,'can_optima'] = [round(x,4) for x in ycan]
            self.curvas.at[i,'pre_optima'] = [round(x,4) for x in ypre]