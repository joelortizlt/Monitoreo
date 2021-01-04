#Se impoortan la librerías necesarias
import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
from  Logicas import funciones as f
from Logicas.InputsRevolventeReal import InputsRevolventeReal
from Logicas.InputsRevolventeTeorico import InputsRevolventeTeorico


#creación de la clase
class InputsRevolvente(InputsRevolventeReal,InputsRevolventeTeorico):
    #constructor del objeto
    def __init__(self,df_real,df_teorico,mincosecha='',maxcosecha='',completar=True):
        if completar==True:
            izquierda = df_real[['CODCLAVEOPECTA','COSECHA','MAXMAD']+f.all_cortes(df_real)].copy()
            df_teorico = pd.merge(left=izquierda, right=df_teorico, how='inner', left_on=['CODCLAVEOPECTA'], right_on=['CODCLAVEOPECTA'])
        
            izquierda = df_teorico[['CODCLAVEOPECTA']].copy()
            df_real = pd.merge(left=izquierda, right=df_real, how='left', left_on=['CODCLAVEOPECTA'], right_on=['CODCLAVEOPECTA'])
        
        InputsRevolventeReal.__init__(self,df=df_real,mincosecha=mincosecha,maxcosecha=maxcosecha)
        InputsRevolventeTeorico.__init__(self,df=df_teorico,mincosecha=mincosecha,maxcosecha=maxcosecha)


    def condensar(self,cortes=[]):

        InputsRevolventeReal.condensar(self,cortes)
        InputsRevolventeTeorico.condensar(self,cortes)
        curvas = pd.merge(left=self.curvasR, right=self.curvasT, how='left', left_on=f.all_cortes(self.curvasR), right_on=f.all_cortes(self.curvasT))
        #curvas['check']=curvas['recuento_x']-curvas['recuento_y']
        curvas = curvas.rename(columns={'recuento_x':'recuento'}).drop('recuento_y',1)
        stats = curvas[f.all_cortes(curvas)+['recuento']].copy()
        promedios = curvas[f.all_cortes(curvas)+['recuento']].copy()
        #intervalos
        ci_pd = curvas[f.all_cortes(curvas)+['recuento']].copy()
        ci_can = curvas[f.all_cortes(curvas)+['recuento']].copy()
        ci_saldo = curvas[f.all_cortes(curvas)+['recuento']].copy()
        for ci in [ci_pd,ci_can,ci_saldo]:
            ci['y_real']=''
            ci['y_teorico']=''
            ci['CI:5.0-95.0']=''
            ci['CI:5.0-95.0_u']=''
            ci['CI:2.5-97.5']=''
            ci['CI:2.5-97.5_u']=''
            ci['CI:0.5-99.5']=''
            ci['CI:0.5-99.5_u']=''

        for i in range(len(curvas)):

            l=min(len(curvas.loc[i, 'pd_real']),len(curvas.loc[i, 'pd_teorico']))
            curvas.at[i, 'pd_real']=curvas.loc[i, 'pd_real'].copy()[:l]
            curvas.at[i, 'pd_teorico']=curvas.loc[i, 'pd_teorico'].copy()[:l]
            stats.at[i,'MAE_pd'] = mean_absolute_error(curvas.loc[i, 'pd_real'], curvas.loc[i, 'pd_teorico'])
            #intervalos
            ci_pd.at[i, 'y_real']=curvas.at[i, 'pd_real'].copy()
            ci_pd.at[i, 'y_teorico']=curvas.at[i, 'pd_teorico'].copy()
            ci_pd.at[i, 'CI:5.0-95.0']=curvas.at[i, 'pd_real'].copy()
            ci_pd.at[i, 'CI:5.0-95.0_u']=curvas.at[i, 'pd_real'].copy()
            ci_pd.at[i, 'CI:2.5-97.5']=curvas.at[i, 'pd_real'].copy()
            ci_pd.at[i, 'CI:2.5-97.5_u']=curvas.at[i, 'pd_real'].copy()
            ci_pd.at[i, 'CI:0.5-99.5']=curvas.at[i, 'pd_real'].copy()
            ci_pd.at[i, 'CI:0.5-99.5_u']=curvas.at[i, 'pd_real'].copy()
            for j in range(l):
                p = curvas.at[i, 'pd_teorico'][j]/100
                n = self.nT.at[i, 'pd_teorico'][j]
                sd = (p*(1-p)/n)**0.5
                ci_pd.at[i, 'CI:5.0-95.0'][j]=round((p-sd*1.645)*100,4)
                ci_pd.at[i, 'CI:5.0-95.0_u'][j]=round((p+sd*1.645)*100,4)
                ci_pd.at[i, 'CI:2.5-97.5'][j]=round((p-sd*1.96)*100,4)
                ci_pd.at[i, 'CI:2.5-97.5_u'][j]=round((p+sd*1.96)*100,4)
                ci_pd.at[i, 'CI:0.5-99.5'][j]=round((p-sd*2.575)*100,4)
                ci_pd.at[i, 'CI:0.5-99.5_u'][j]=round((p+sd*2.575)*100,4)
                
            l=min(len(curvas.loc[i, 'can_real']),len(curvas.loc[i, 'can_teorico']))
            curvas.at[i, 'can_real']=curvas.loc[i, 'can_real'].copy()[:l]
            curvas.at[i, 'can_teorico']=curvas.loc[i, 'can_teorico'].copy()[:l]
            stats.at[i,'MAE_can'] = mean_absolute_error(curvas.loc[i, 'can_real'], curvas.loc[i, 'can_teorico']) 
            #intervalos
            ci_can.at[i, 'y_real']=curvas.at[i, 'can_real'].copy()
            ci_can.at[i, 'y_teorico']=curvas.at[i, 'can_teorico'].copy()
            ci_can.at[i, 'CI:5.0-95.0']=curvas.at[i, 'can_real'].copy()
            ci_can.at[i, 'CI:5.0-95.0_u']=curvas.at[i, 'can_real'].copy()
            ci_can.at[i, 'CI:2.5-97.5']=curvas.at[i, 'can_real'].copy()
            ci_can.at[i, 'CI:2.5-97.5_u']=curvas.at[i, 'can_real'].copy()
            ci_can.at[i, 'CI:0.5-99.5']=curvas.at[i, 'can_real'].copy()
            ci_can.at[i, 'CI:0.5-99.5_u']=curvas.at[i, 'can_real'].copy()
            for j in range(l):
                p = curvas.at[i, 'can_teorico'][j]/100
                n = self.nT.at[i, 'can_teorico'][j]
                sd = (p*(1-p)/n)**0.5
                ci_can.at[i, 'CI:5.0-95.0'][j]=round((p-sd*1.645)*100,4)
                ci_can.at[i, 'CI:5.0-95.0_u'][j]=round((p+sd*1.645)*100,4)
                ci_can.at[i, 'CI:2.5-97.5'][j]=round((p-sd*1.96)*100,4)
                ci_can.at[i, 'CI:2.5-97.5_u'][j]=round((p+sd*1.96)*100,4)
                ci_can.at[i, 'CI:0.5-99.5'][j]=round((p-sd*2.575)*100,4)
                ci_can.at[i, 'CI:0.5-99.5_u'][j]=round((p+sd*2.575)*100,4)

            l=min(len(curvas.loc[i, 'saldo_real']),len(curvas.loc[i, 'saldo_teorico']))
            curvas.at[i, 'saldo_real']=curvas.loc[i, 'saldo_real'].copy()[:l]
            curvas.at[i, 'saldo_teorico']=curvas.loc[i, 'saldo_teorico'].copy()[:l]
            stats.at[i,'MAE_saldo'] = mean_absolute_error(curvas.loc[i, 'saldo_real'], curvas.loc[i, 'saldo_teorico']) 
            #intervalos
            ci_saldo.at[i, 'y_real']=curvas.at[i, 'saldo_real'].copy()
            ci_saldo.at[i, 'y_teorico']=curvas.at[i, 'saldo_teorico'].copy()
            ci_saldo.at[i, 'CI:5.0-95.0']=curvas.at[i, 'saldo_real'].copy()
            ci_saldo.at[i, 'CI:5.0-95.0_u']=curvas.at[i, 'saldo_real'].copy()
            ci_saldo.at[i, 'CI:2.5-97.5']=curvas.at[i, 'saldo_real'].copy()
            ci_saldo.at[i, 'CI:2.5-97.5_u']=curvas.at[i, 'saldo_real'].copy()
            ci_saldo.at[i, 'CI:0.5-99.5']=curvas.at[i, 'saldo_real'].copy()
            ci_saldo.at[i, 'CI:0.5-99.5_u']=curvas.at[i, 'saldo_real'].copy()
            for j in range(l):
                p = curvas.at[i, 'saldo_teorico'][j]
                n = self.nT.at[i, 'saldo_teorico'][j]
                s = self.nT.at[i, 'saldo_teorico_s'][j]
                sd = s/(n**0.5)
                ci_saldo.at[i, 'CI:5.0-95.0'][j]=p-sd*1.645
                ci_saldo.at[i, 'CI:5.0-95.0_u'][j]=p+sd*1.645
                ci_saldo.at[i, 'CI:2.5-97.5'][j]=p-sd*1.96
                ci_saldo.at[i, 'CI:2.5-97.5_u'][j]=p+sd*1.96
                ci_saldo.at[i, 'CI:0.5-99.5'][j]=p-sd*2.575
                ci_saldo.at[i, 'CI:0.5-99.5_u'][j]=p+sd*2.575

            promedios.at[i, 'pd_real'] = sum(curvas.at[i, 'pd_real'])/len(curvas.at[i, 'pd_real'])   
            promedios.at[i, 'can_real'] = sum(curvas.at[i, 'can_real'])/len(curvas.at[i, 'can_real'])
            promedios.at[i, 'saldo_real'] = sum(curvas.at[i, 'saldo_real'])/len(curvas.at[i, 'saldo_real'])
            promedios.at[i, 'pd_teorico'] = sum(curvas.at[i, 'pd_teorico'])/len(curvas.at[i, 'pd_teorico'])
            promedios.at[i, 'can_teorico'] = sum(curvas.at[i, 'can_teorico'])/len(curvas.at[i, 'can_teorico'])
            promedios.at[i, 'saldo_teorico'] = sum(curvas.at[i, 'saldo_teorico'])/len(curvas.at[i, 'saldo_teorico'])

        self.curvas = curvas
        self.stats = stats
        self.promedios = promedios
        self.ci_pd = ci_pd
        self.ci_can = ci_can
        self.ci_saldo = ci_saldo
    
    
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
        self.curvas['saldo_optimo'] = ''
        self.stats['MAEop_pd'] = ''
        self.stats['MAEop_can'] = ''
        self.stats['MAEop_saldo'] = ''
        
        for i in range(len(self.stats)):
            
            minMAE = self.stats.loc[i, 'MAE_pd'].copy()
            scalarMAE = 1
            x = self.curvas.loc[i, 'pd_real'].copy()
            y = self.curvas.loc[i, 'pd_teorico'].copy()
            for s in np.arange(0,5,step):
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
            self.promedios.at[i, 'pd_optimo'] = sum(self.curvas.at[i, 'pd_optimo'])/len(self.curvas.at[i, 'pd_optimo'])

            minMAE = self.stats.loc[i, 'MAE_can'].copy()
            scalarMAE = 1
            x = self.curvas.loc[i, 'can_real'].copy()
            y = self.curvas.loc[i, 'can_teorico'].copy()
            for s in np.arange(0,5,step):
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
            self.promedios.at[i, 'can_optimo'] = sum(self.curvas.at[i, 'can_optimo'])/len(self.curvas.at[i, 'can_optimo'])

            minMAE = self.stats.loc[i, 'MAE_saldo'].copy()
            scalarMAE = 1
            x = self.curvas.loc[i, 'saldo_real'].copy()
            y = self.curvas.loc[i, 'saldo_teorico'].copy()
            for s in np.arange(0,5,step):
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
            self.promedios.at[i, 'saldo_optimo'] = sum(self.curvas.at[i, 'saldo_optimo'])/len(self.curvas.at[i, 'saldo_optimo'])


    def impactoTmin(self,df_tmin,impactoTIR=False):

        cortes=f.all_cortes(self.stats)
        izquierda = self.df_real[['CODCLAVEOPECTA','COSECHA']+f.all_cortes(self.df_real)].copy()

        derecha = df_tmin[['CODCLAVEOPECTA','SaldoProm','Tmin','PDTmin','CANTmin','SALTmin']].copy()
        df = pd.merge(left=izquierda, right=derecha, how='inner', left_on=['CODCLAVEOPECTA'], right_on=['CODCLAVEOPECTA'])

        if cortes==['C_TODOS']:
            df.loc[:,'C_TODOS']=''
        df = df[cortes+['CODCLAVEOPECTA','COSECHA','SaldoProm','Tmin','PDTmin','CANTmin','SALTmin']]
        Tmin = self.curvas[f.all_cortes(self.curvas)+['recuento']].copy()

        for i in range(len(Tmin)):
            temp = pd.merge(df, pd.DataFrame([Tmin.loc[i,:]]), how='inner', left_on=cortes, right_on=cortes)    
            Tmin.at[i,'Tmin_base']  = f.weighted_average(temp,'Tmin','SaldoProm')
            Tmin.at[i,'delta_pd']  = (f.weighted_average(temp,'PDTmin','SaldoProm')-Tmin.loc[i,'Tmin_base'])*(self.stats.loc[i,'scalar_pd']-1)*10
            Tmin.at[i,'delta_can']  = (f.weighted_average(temp,'CANTmin','SaldoProm')-Tmin.loc[i,'Tmin_base'])*(self.stats.loc[i,'scalar_can']-1)*10
            Tmin.at[i,'delta_saldo']  = (f.weighted_average(temp,'SALTmin','SaldoProm')-Tmin.loc[i,'Tmin_base'])*(self.stats.loc[i,'scalar_saldo']-1)*10
            Tmin.at[i,'Tmin_final']  = Tmin.loc[i,'Tmin_base']+Tmin.loc[i,'delta_pd']+Tmin.loc[i,'delta_can']+Tmin.loc[i,'delta_saldo']
            Tmin.at[i,'Monto'] = temp['SaldoProm'].sum()
        self.Tmin = Tmin

        Tmin_base_prom = f.weighted_average(self.Tmin,'Tmin_base','Monto')
        delta_pd_prom = f.weighted_average(self.Tmin,'delta_pd','Monto')
        delta_can_prom = f.weighted_average(self.Tmin,'delta_can','Monto')
        delta_saldo_prom = f.weighted_average(self.Tmin,'delta_saldo','Monto')
        Tmin_final_prom = f.weighted_average(self.Tmin,'Tmin_final','Monto')      

        data = [['Tmin_base_prom', Tmin_base_prom], ['delta_pd_prom', delta_pd_prom], ['delta_can_prom', delta_can_prom], ['delta_saldo_prom', delta_saldo_prom], ['Tmin_final_prom', Tmin_final_prom]]  
        TminProm = pd.DataFrame(data, columns = ['Campo', 'Valor'])
        self.TminProm = TminProm


        if impactoTIR==True:
            derecha2 = df_tmin[['CODCLAVEOPECTA','ECAP','TIR','TIRPD','TIRCAN','TIRSAL']].copy()
            df2 = pd.merge(left=izquierda, right=derecha2, how='inner', left_on=['CODCLAVEOPECTA'], right_on=['CODCLAVEOPECTA'])
            
            if cortes==['C_TODOS']:
                df2.loc[:,'C_TODOS']=''
            df2 = df2[cortes+['CODCLAVEOPECTA','COSECHA','ECAP','TIR','TIRPD','TIRCAN','TIRSAL']]
            TIR = self.curvas[f.all_cortes(self.curvas)+['recuento']].copy()

            for i in range(len(TIR)):
                temp = pd.merge(df2, pd.DataFrame([TIR.loc[i,:]]), how='inner', left_on=cortes, right_on=cortes)    
                TIR.at[i,'TIR_base']  = f.weighted_average(temp,'TIR','ECAP')
                TIR.at[i,'delta_pd']  = (f.weighted_average(temp,'TIRPD','ECAP')-TIR.loc[i,'TIR_base'])*(self.stats.loc[i,'scalar_pd']-1)*10
                TIR.at[i,'delta_can']  = (f.weighted_average(temp,'TIRCAN','ECAP')-TIR.loc[i,'TIR_base'])*(self.stats.loc[i,'scalar_can']-1)*10
                TIR.at[i,'delta_saldo']  = (f.weighted_average(temp,'TIRSAL','ECAP')-TIR.loc[i,'TIR_base'])*(self.stats.loc[i,'scalar_saldo']-1)*10
                TIR.at[i,'TIR_final']  = TIR.loc[i,'TIR_base']+TIR.loc[i,'delta_pd']+TIR.loc[i,'delta_can']+TIR.loc[i,'delta_saldo']
                TIR.at[i,'Capital promedio'] = temp['ECAP'].sum()
            self.TIR = TIR

            TIR_base_prom = f.weighted_average(self.TIR,'TIR_base','Capital promedio')
            delta_pd_prom = f.weighted_average(self.TIR,'delta_pd','Capital promedio')
            delta_can_prom = f.weighted_average(self.TIR,'delta_can','Capital promedio')
            delta_saldo_prom = f.weighted_average(self.TIR,'delta_saldo','Capital promedio')
            TIR_final_prom = f.weighted_average(self.TIR,'TIR_final','Capital promedio')      

            data = [['TIR_base_prom', TIR_base_prom], ['delta_pd_prom', delta_pd_prom], ['delta_can_prom', delta_can_prom], ['delta_saldo_prom', delta_saldo_prom], ['TIR_final_prom', TIR_final_prom]]  
            TIRProm = pd.DataFrame(data, columns = ['Campo', 'Valor'])
            self.TIRProm = TIRProm