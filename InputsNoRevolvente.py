#Se impoortan la librerías necesarias
import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import funciones as f
from InputsNoRevolventeReal import InputsNoRevolventeReal
from InputsNoRevolventeTeorico import InputsNoRevolventeTeorico


#creación de la clase
class InputsNoRevolvente(InputsNoRevolventeReal,InputsNoRevolventeTeorico):
    #constructor del objeto
    def __init__(self,df_real,df_teorico,mincosecha='',maxcosecha='',completar=True):
        if completar==True:
            izquierda = df_real[['CODCLAVEOPECTA','COSECHA','MAXMAD']+f.all_cortes(df_real)].copy()
            df_teorico = pd.merge(left=izquierda, right=df_teorico, how='inner', left_on=['CODCLAVEOPECTA'], right_on=['CODCLAVEOPECTA'])
        
        InputsNoRevolventeReal.__init__(self,df=df_real,mincosecha=mincosecha,maxcosecha=maxcosecha)
        InputsNoRevolventeTeorico.__init__(self,df=df_teorico,mincosecha=mincosecha,maxcosecha=maxcosecha)


    def condensar(self,cortes=[]):

        InputsNoRevolventeReal.condensar(self,cortes)
        InputsNoRevolventeTeorico.condensar(self,cortes)

        curvas = pd.merge(left=self.curvasR, right=self.curvasT, how='left', left_on=f.all_cortes(self.curvasR), right_on=f.all_cortes(self.curvasT))
        curvas['check']=curvas['recuento_x']-curvas['recuento_y']
        curvas = curvas.rename(columns={'recuento_x':'recuento'}).drop('recuento_y',1)
        stats = curvas[f.all_cortes(curvas)+['recuento']].copy()

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
        
        self.curvas['pd_optimo'] = ''
        self.curvas['can_optimo'] = ''
        self.curvas['pre_optimo'] = ''
        self.stats['MAEop_pd'] = ''
        self.stats['MAEop_can'] = ''
        self.stats['MAEop_pre'] = ''
        
        for i in range(len(self.stats)):
            
            minMAE = self.stats.loc[i, 'MAE_pd'].copy()
            scalarMAE = 1
            x = self.curvas.loc[i, 'pd_real'].copy()
            y = self.curvas.loc[i, 'pd_teorico'].copy()
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
            self.stats.at[i,'MAEop_pd'] = minMAE
            self.stats.at[i,'scalar_pd'] = scalarMAE
            self.curvas.at[i,'pd_optimo'] = [round(x,4) for x in yopt]

            
            minMAE = self.stats.loc[i, 'MAE_can'].copy()
            scalarMAE = 1
            x = self.curvas.loc[i, 'can_real'].copy()
            y = self.curvas.loc[i, 'can_teorico'].copy()
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
            self.stats.at[i,'MAEop_can'] = minMAE
            self.stats.at[i,'scalar_can'] = scalarMAE
            self.curvas.at[i,'can_optimo'] = [round(x,4) for x in yopt]


            minMAE = self.stats.loc[i, 'MAE_pre'].copy()
            scalarMAE = 1
            x = self.curvas.loc[i, 'pre_real'].copy()
            y = self.curvas.loc[i, 'pre_teorico'].copy()
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
            self.stats.at[i,'MAEop_pre'] = minMAE
            self.stats.at[i,'scalar_pre'] = scalarMAE
            self.curvas.at[i,'pre_optimo'] = [round(x,4) for x in yopt]


    def impactoTmin(self,df_tmin,completar=True):

        cortes=f.all_cortes(self.stats)
        if completar==True:
            izquierda = self.df_real[['CODCLAVEOPECTA','COSECHA','MTODESEMBOLSADO']+f.all_cortes(self.df_real)].copy()
            derecha = df_tmin[['CODCLAVEOPECTA','Tmin','PDTmin','CANTmin','PRETmin']].copy()
            df = pd.merge(left=izquierda, right=derecha, how='inner', left_on=['CODCLAVEOPECTA'], right_on=['CODCLAVEOPECTA'])
        
        if cortes==['C_TODOS']:
            df['C_TODOS']=''
        df = df[cortes+['CODCLAVEOPECTA','COSECHA','MTODESEMBOLSADO','Tmin','PDTmin','CANTmin','PRETmin']]
        Tmin = self.stats[cortes].copy()

        for i in range(len(Tmin)):
            temp = pd.merge(df, pd.DataFrame([Tmin.loc[i,:]]), how='inner', left_on=cortes, right_on=cortes)    
            Tmin.at[i,'Tmin_base']  = f.weighted_average(temp,'Tmin','MTODESEMBOLSADO')
            Tmin.at[i,'delta_pd']  = (f.weighted_average(temp,'PDTmin','MTODESEMBOLSADO')-Tmin.loc[i,'Tmin_base'])*(self.stats.loc[i,'scalar_pd']-1)*10
            Tmin.at[i,'delta_can']  = (f.weighted_average(temp,'CANTmin','MTODESEMBOLSADO')-Tmin.loc[i,'Tmin_base'])*(self.stats.loc[i,'scalar_can']-1)*10
            Tmin.at[i,'delta_pre']  = (f.weighted_average(temp,'PRETmin','MTODESEMBOLSADO')-Tmin.loc[i,'Tmin_base'])*(self.stats.loc[i,'scalar_pre']-1)*10
            Tmin.at[i,'Tmin_final']  = Tmin.loc[i,'Tmin_base']+Tmin.loc[i,'delta_pd']+Tmin.loc[i,'delta_can']+Tmin.loc[i,'delta_pre']
            Tmin.at[i,'Monto'] = temp['MTODESEMBOLSADO'].sum()
        self.Tmin = Tmin

        Tmin_base_prom = f.weighted_average(self.Tmin,'Tmin_base','Monto')
        delta_pd_prom = f.weighted_average(self.Tmin,'delta_pd','Monto')
        delta_can_prom = f.weighted_average(self.Tmin,'delta_can','Monto')
        delta_pre_prom = f.weighted_average(self.Tmin,'delta_pre','Monto')
        Tmin_final_prom = f.weighted_average(self.Tmin,'Tmin_final','Monto')      

        data = [['Tmin_base_prom', Tmin_base_prom], ['delta_pd_prom', delta_pd_prom], ['delta_can_prom', delta_can_prom], ['delta_pre_prom', delta_pre_prom], ['Tmin_final_prom', Tmin_final_prom]]  
        TminProm = pd.DataFrame(data, columns = ['Campo', 'Valor'])
        self.TminProm = TminProm

