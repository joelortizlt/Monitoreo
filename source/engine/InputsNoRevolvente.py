#Se impoortan la librerías necesarias
import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import math

from source.engine import funciones as f
from source.engine.InputsNoRevolventeReal import InputsNoRevolventeReal
from source.engine.InputsNoRevolventeTeorico import InputsNoRevolventeTeorico


#creación de la clase
class InputsNoRevolvente(InputsNoRevolventeReal,InputsNoRevolventeTeorico):
    #constructor del objeto
    def __init__(self,df_real,df_teorico,mincosecha='',maxcosecha='',completar=True):
        if completar==True:

            izquierda = df_real[['CODCLAVEOPECTA','COSECHA','MAXMAD','MTODESEMBOLSADO']+f.all_cortes(df_real)].copy()
            df_teorico = pd.merge(left=izquierda, right=df_teorico, how='inner', left_on=['CODCLAVEOPECTA'], right_on=['CODCLAVEOPECTA'])

            izquierda = df_teorico[['CODCLAVEOPECTA']].copy()
            df_real = pd.merge(left=izquierda, right=df_real, how='left', left_on=['CODCLAVEOPECTA'], right_on=['CODCLAVEOPECTA'])

        InputsNoRevolventeReal.__init__(self,df=df_real,mincosecha=mincosecha,maxcosecha=maxcosecha)
        InputsNoRevolventeTeorico.__init__(self,df=df_teorico,mincosecha=mincosecha,maxcosecha=maxcosecha)


    def condensar(self,cortes=[]):

        InputsNoRevolventeReal.condensar(self,cortes)
        InputsNoRevolventeTeorico.condensar(self,cortes)
        curvas = pd.merge(left=self.curvasR, right=self.curvasT, how='left', left_on=f.all_cortes(self.curvasR), right_on=f.all_cortes(self.curvasT))
        #curvas['check']=curvas['recuento_x']-curvas['recuento_y']
        curvas = curvas.rename(columns={'recuento_x':'recuento'}).drop('recuento_y',1)
        stats = curvas[f.all_cortes(curvas)+['recuento']].copy()
        promedios = curvas[f.all_cortes(curvas)+['recuento']].copy()
        #intervalos
        ci_pd = curvas[f.all_cortes(curvas)+['recuento']].copy()
        ci_can = curvas[f.all_cortes(curvas)+['recuento']].copy()
        ci_pre = curvas[f.all_cortes(curvas)+['recuento']].copy()
        for ci in [ci_pd,ci_can,ci_pre]:
            ci['y_real']=''
            ci['y_pred']=''
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
            curvas.at[i, 'vivos']=curvas.loc[i, 'vivos'].copy()[:l]
            stats.at[i,'MAE_pd'] = mean_absolute_error(curvas.loc[i, 'pd_real'], curvas.loc[i, 'pd_teorico'])
            #intervalos
            ci_pd.at[i, 'y_real']=curvas.at[i, 'pd_real'].copy()
            ci_pd.at[i, 'y_pred']=curvas.at[i, 'pd_teorico'].copy()
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
            ci_can.at[i, 'y_pred']=curvas.at[i, 'can_teorico'].copy()
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

            l=min(len(curvas.loc[i, 'pre_real']),len(curvas.loc[i, 'pre_teorico']))
            curvas.at[i, 'pre_real']=curvas.loc[i, 'pre_real'].copy()[:l]
            curvas.at[i, 'pre_teorico']=curvas.loc[i, 'pre_teorico'].copy()[:l]
            stats.at[i,'MAE_pre'] = mean_absolute_error(curvas.loc[i, 'pre_real'], curvas.loc[i, 'pre_teorico']) 
            #intervalos
            ci_pre.at[i, 'y_real']=curvas.at[i, 'pre_real'].copy()
            ci_pre.at[i, 'y_pred']=curvas.at[i, 'pre_teorico'].copy()
            ci_pre.at[i, 'CI:5.0-95.0']=curvas.at[i, 'pre_real'].copy()
            ci_pre.at[i, 'CI:5.0-95.0_u']=curvas.at[i, 'pre_real'].copy()
            ci_pre.at[i, 'CI:2.5-97.5']=curvas.at[i, 'pre_real'].copy()
            ci_pre.at[i, 'CI:2.5-97.5_u']=curvas.at[i, 'pre_real'].copy()
            ci_pre.at[i, 'CI:0.5-99.5']=curvas.at[i, 'pre_real'].copy()
            ci_pre.at[i, 'CI:0.5-99.5_u']=curvas.at[i, 'pre_real'].copy()
            for j in range(l):
                p = curvas.at[i, 'pre_teorico'][j]/100
                n = self.nT.at[i, 'pre_teorico'][j]
                sd = (p*(1-p)/n)**0.5
                ci_pre.at[i, 'CI:5.0-95.0'][j]=round((p-sd*1.645)*100,4)
                ci_pre.at[i, 'CI:5.0-95.0_u'][j]=round((p+sd*1.645)*100,4)
                ci_pre.at[i, 'CI:2.5-97.5'][j]=round((p-sd*1.96)*100,4)
                ci_pre.at[i, 'CI:2.5-97.5_u'][j]=round((p+sd*1.96)*100,4)
                ci_pre.at[i, 'CI:0.5-99.5'][j]=round((p-sd*2.575)*100,4)
                ci_pre.at[i, 'CI:0.5-99.5_u'][j]=round((p+sd*2.575)*100,4)

            promedios.at[i, 'pd_real'] = sum(curvas.at[i, 'pd_real'])/len(curvas.at[i, 'pd_real'])   
            promedios.at[i, 'can_real'] = sum(curvas.at[i, 'can_real'])/len(curvas.at[i, 'can_real'])
            promedios.at[i, 'pre_real'] = sum(curvas.at[i, 'pre_real'])/len(curvas.at[i, 'pre_real'])
            promedios.at[i, 'pd_teorico'] = sum(curvas.at[i, 'pd_teorico'])/len(curvas.at[i, 'pd_teorico'])
            promedios.at[i, 'can_teorico'] = sum(curvas.at[i, 'can_teorico'])/len(curvas.at[i, 'can_teorico'])
            promedios.at[i, 'pre_teorico'] = sum(curvas.at[i, 'pre_teorico'])/len(curvas.at[i, 'pre_teorico'])

        self.curvas = curvas
        self.stats = stats
        self.promedios = promedios
        self.ci_pd = ci_pd
        self.ci_can = ci_can
        self.ci_pre = ci_pre
    
    
    def plotear(self, texto, optimo=False, print = False): 
        cortes_temp = f.all_cortes(self.curvas)
        for i in range(len(self.curvas)):
            z = []
            for j in range(len(self.curvas[texto+'_real'][i])):
                z.append(j+1)
            a = ''
            for j in cortes_temp:
                a = a + str(j)[2:] + ' ' + str(self.curvas[j][i]) + ' y '

            plt.xlabel('Maduración', fontsize=10)
            plt.title(texto.upper() + ': ' + a[0:-3], fontsize=14, pad=20, color = 'midnightblue')
            max_real = max(max(self.curvas[texto+'_real']))
            max_teorico = max(max(self.curvas[texto+'_teorico']))
            len_y = math.ceil(max(max_real,max_teorico)/5)*5
            
            r = self.curvas[texto + '_real'][i]
            plt.annotate(round(r[0],1),(1-0.5,r[0]+len_y/50)) #Etiqueta 1
            plt.annotate(round(r[5],1),(6-0.5,r[5]+len_y/50)) #Etiqueta 6

            b = min(12,len(r))-1
            plt.annotate(round(r[b],1),(b+1-0.5,r[b]+len_y/50)) #Etiqueta 12
            plt.plot(z, r, label='real', linestyle='', marker='o', markersize=4, color='black')
            
            t = self.curvas[texto + '_teorico'][i]
            plt.annotate(round(t[0],1),(1-0.5,t[0]+len_y/50)) #Etiqueta 1
            plt.annotate(round(t[5],1),(6-0.5,t[5]+len_y/50)) #Etiqueta 6
            plt.annotate(round(t[b],1),(b+1-0.5,t[b]+len_y/50)) #Etiqueta 12
            plt.plot(z, t, label='teórico', color='lightseagreen') #color='royalblue'
            
            if optimo:
                o = self.curvas[texto + '_optimo'][i]
                plt.plot(z, o, label='óptimo', color='black')
            plt.plot(0)
            plt.ylim([0, len_y]) #add len

#            plt.annotate('Créditos: ' + str(f"{self.curvas['recuento'][i]:,}") + "\n" +
#                        'Cancelados: ' + str(f"{self.df_real[(self.df_real.FAIL_TYPE==2)].groupby(corte)['CODCLAVEOPECTA'].count().reset_index(drop=True)[i]:,}"),
#                        (0.5,len_y/1.14), size=9.5,
#                        bbox=dict(boxstyle="round", alpha=0.05)) #Etiqueta inferior derecha
            plt.legend(fontsize = 9, loc=1 ,bbox_to_anchor=(1.025,-0.04), frameon=False)
            
            if print == True:
                plt.savefig(texto, dpi=400)
                plt.close()
            else:
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

            minMAE = self.stats.loc[i, 'MAE_pre'].copy()
            scalarMAE = 1
            x = self.curvas.loc[i, 'pre_real'].copy()
            y = self.curvas.loc[i, 'pre_teorico'].copy()
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
            self.stats.at[i,'MAEop_pre'] = minMAE
            self.stats.at[i,'scalar_pre'] = scalarMAE
            self.curvas.at[i,'pre_optimo'] = [round(x,4) for x in yopt]
            self.promedios.at[i, 'pre_optimo'] = sum(self.curvas.at[i, 'pre_optimo'])/len(self.curvas.at[i, 'pre_optimo'])
    

    def impacto(self,df_PRECIOS):
        cortes=f.all_cortes(self.stats)
        izquierda = self.df_real[['CODCLAVEOPECTA','COSECHA']+f.all_cortes(self.df_real)].copy()

        derecha = df_PRECIOS[['CODCLAVEOPECTA','MTODESEMBOLSADO','Tmin','PDTmin','CANTmin','PRETmin',
                           'ECAP','TIR','PDTIR','CANTIR','PRETIR',
                           'SALDOAVG','ROA','PDROA','CANROA','PREROA']].copy()
        df = pd.merge(left=izquierda, right=derecha, how='inner', left_on=['CODCLAVEOPECTA'], right_on=['CODCLAVEOPECTA'])

        if cortes==['C_TODOS']:
            df.loc[:,'C_TODOS']=''
        df = df[cortes+['CODCLAVEOPECTA','COSECHA','MTODESEMBOLSADO','Tmin','PDTmin','CANTmin','PRETmin',
                        'ECAP','TIR','PDTIR','CANTIR','PRETIR',
                        'SALDOAVG','ROA','PDROA','CANROA','PREROA']]
        Impacto = self.curvas[f.all_cortes(self.curvas)+['recuento']].copy()

        for i in range(len(Impacto)):
            temp = pd.merge(df, pd.DataFrame([Impacto.loc[i,:]]), how='inner', left_on=cortes, right_on=cortes)    
            
            Impacto.at[i,'Tmin_base']  = f.weighted_average(temp,'Tmin','MTODESEMBOLSADO')
            Impacto.at[i,'Tmin_delta_pd']  = (f.weighted_average(temp,'PDTmin','MTODESEMBOLSADO')-Impacto.loc[i,'Tmin_base'])*(self.stats.loc[i,'scalar_pd']-1)*10
            Impacto.at[i,'Tmin_delta_can']  = (f.weighted_average(temp,'CANTmin','MTODESEMBOLSADO')-Impacto.loc[i,'Tmin_base'])*(self.stats.loc[i,'scalar_can']-1)*10
            Impacto.at[i,'Tmin_delta_pre']  = (f.weighted_average(temp,'PRETmin','MTODESEMBOLSADO')-Impacto.loc[i,'Tmin_base'])*(self.stats.loc[i,'scalar_pre']-1)*10
            Impacto.at[i,'Tmin_final']  = Impacto.loc[i,'Tmin_base']+Impacto.loc[i,'Tmin_delta_pd']+Impacto.loc[i,'Tmin_delta_can']+Impacto.loc[i,'Tmin_delta_pre']
            Impacto.at[i,'Monto'] = temp['MTODESEMBOLSADO'].sum()

            Impacto.at[i,'TIR_base']  = f.weighted_average(temp,'TIR','ECAP')
            Impacto.at[i,'TIR_delta_pd']  = (f.weighted_average(temp,'PDTIR','ECAP')-Impacto.loc[i,'TIR_base'])*(self.stats.loc[i,'scalar_pd']-1)*10
            Impacto.at[i,'TIR_delta_can']  = (f.weighted_average(temp,'CANTIR','ECAP')-Impacto.loc[i,'TIR_base'])*(self.stats.loc[i,'scalar_can']-1)*10
            Impacto.at[i,'TIR_delta_pre']  = (f.weighted_average(temp,'PRETIR','ECAP')-Impacto.loc[i,'TIR_base'])*(self.stats.loc[i,'scalar_pre']-1)*10
            Impacto.at[i,'TIR_final']  = Impacto.loc[i,'TIR_base']+Impacto.loc[i,'TIR_delta_pd']+Impacto.loc[i,'TIR_delta_can']+Impacto.loc[i,'TIR_delta_pre']
            Impacto.at[i,'Capital promedio'] = temp['ECAP'].sum()

            Impacto.at[i,'ROA_base']  = f.weighted_average(temp,'ROA','SALDOAVG')
            Impacto.at[i,'ROA_delta_pd']  = (f.weighted_average(temp,'PDROA','SALDOAVG')-Impacto.loc[i,'ROA_base'])*(self.stats.loc[i,'scalar_pd']-1)*10
            Impacto.at[i,'ROA_delta_can']  = (f.weighted_average(temp,'CANROA','SALDOAVG')-Impacto.loc[i,'ROA_base'])*(self.stats.loc[i,'scalar_can']-1)*10
            Impacto.at[i,'ROA_delta_pre']  = (f.weighted_average(temp,'PREROA','SALDOAVG')-Impacto.loc[i,'ROA_base'])*(self.stats.loc[i,'scalar_pre']-1)*10
            Impacto.at[i,'ROA_final']  = Impacto.loc[i,'ROA_base']+Impacto.loc[i,'ROA_delta_pd']+Impacto.loc[i,'ROA_delta_can']+Impacto.loc[i,'ROA_delta_pre']
            Impacto.at[i,'Saldo promedio'] = temp['SALDOAVG'].sum()

        self.Impacto = Impacto

        Tmin_base = f.weighted_average(self.Impacto,'Tmin_base','Monto')
        Tmin_delta_pd = f.weighted_average(self.Impacto,'Tmin_delta_pd','Monto')
        Tmin_delta_can = f.weighted_average(self.Impacto,'Tmin_delta_can','Monto')
        Tmin_delta_pre = f.weighted_average(self.Impacto,'Tmin_delta_pre','Monto')
        Tmin_final = f.weighted_average(self.Impacto,'Tmin_final','Monto')     

        TIR_base = f.weighted_average(self.Impacto,'TIR_base','Capital promedio')
        TIR_delta_pd = f.weighted_average(self.Impacto,'TIR_delta_pd','Capital promedio')
        TIR_delta_can = f.weighted_average(self.Impacto,'TIR_delta_can','Capital promedio')
        TIR_delta_pre = f.weighted_average(self.Impacto,'TIR_delta_pre','Capital promedio')
        TIR_final = f.weighted_average(self.Impacto,'TIR_final','Capital promedio')   

        ROA_base = f.weighted_average(self.Impacto,'ROA_base','Saldo promedio')
        ROA_delta_pd = f.weighted_average(self.Impacto,'ROA_delta_pd','Saldo promedio')
        ROA_delta_can = f.weighted_average(self.Impacto,'ROA_delta_can','Saldo promedio')
        ROA_delta_pre = f.weighted_average(self.Impacto,'ROA_delta_pre','Saldo promedio')
        ROA_final = f.weighted_average(self.Impacto,'ROA_final','Saldo promedio')     

        data = [['Tmin_base', Tmin_base], ['Tmin_delta_pd', Tmin_delta_pd], ['Tmin_delta_can', Tmin_delta_can], ['Tmin_delta_pre', Tmin_delta_pre], ['Tmin_final', Tmin_final],
                ['TIR_base', TIR_base], ['TIR_delta_pd', TIR_delta_pd], ['TIR_delta_can', TIR_delta_can], ['TIR_delta_pre', TIR_delta_pre], ['TIR_final', TIR_final],
                ['ROA_base', ROA_base], ['ROA_delta_pd', ROA_delta_pd], ['ROA_delta_can', ROA_delta_can], ['ROA_delta_pre', ROA_delta_pre], ['ROA_final', ROA_final]]  
        
        ImpactoProm = pd.DataFrame(data, columns = ['Campo', 'Valor'])
        self.ImpactoProm = ImpactoProm

        
