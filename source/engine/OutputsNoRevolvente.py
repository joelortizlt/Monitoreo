#Se impoortan la librerías necesarias
import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import math

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

            l=min(len(curvas.loc[i, 'rebate_real']),len(curvas.loc[i, 'rebate_teorico']))
            curvas.at[i, 'rebate_real']=curvas.loc[i, 'rebate_real'].copy()[:l]
            curvas.at[i, 'rebate_teorico']=curvas.loc[i, 'rebate_teorico'].copy()[:l]
            
            l=min(len(curvas.loc[i, 'provisionb_real']),len(curvas.loc[i, 'provisionb_teorico']))
            curvas.at[i, 'provisionb_real']=curvas.loc[i, 'provisionb_real'].copy()[:l]
            curvas.at[i, 'provisionb_teorico']=curvas.loc[i, 'provisionb_teorico'].copy()[:l]
            
            l=min(len(curvas.loc[i, 'ixs_real']),len(curvas.loc[i, 'ixs_teorico']))
            curvas.at[i, 'ixs_real']=curvas.loc[i, 'ixs_real'].copy()[:l]
            curvas.at[i, 'ixs_teorico']=curvas.loc[i, 'ixs_teorico'].copy()[:l]

            l=min(len(curvas.loc[i, 'saldo_real']),len(curvas.loc[i, 'saldo_teorico']))
            curvas.at[i, 'saldo_real']=curvas.loc[i, 'saldo_real'].copy()[:l]
            curvas.at[i, 'saldo_teorico']=curvas.loc[i, 'saldo_teorico'].copy()[:l]

            ratios.at[i,'r_if_real'] = round(((sum(curvas.loc[i, 'if_real'])/sum(curvas.loc[i, 'saldo_real'])))*12,6)*100
            ratios.at[i,'r_ef_real'] = round(((sum(curvas.loc[i, 'ef_real'])/sum(curvas.loc[i, 'saldo_real'])))*12,6)*100
            ratios.at[i,'r_rebate_real'] = round(((sum(curvas.loc[i, 'rebate_real'])/sum(curvas.loc[i, 'saldo_real'])))*12,6)*100
            ratios.at[i,'r_spread_bruto_real'] = ratios.at[i,'r_if_real'] + ratios.at[i,'r_ef_real'] + ratios.at[i,'r_rebate_real']
            ratios.at[i,'r_provisionb_real'] = round(((sum(curvas.loc[i, 'provisionb_real'])/sum(curvas.loc[i, 'saldo_real'])))*12,6)*100
            ratios.at[i,'r_ixs_real'] = round(((sum(curvas.loc[i, 'ixs_real'])/sum(curvas.loc[i, 'saldo_real'])))*12,6)*100
            ratios.at[i,'r_spread_neto_real'] = ratios.at[i,'r_spread_bruto_real'] - ratios.at[i,'r_provisionb_real'] + ratios.at[i,'r_ixs_real'] 
          
            ratios.at[i,'r_if_teorico'] = round(((sum(curvas.loc[i, 'if_teorico'])/sum(curvas.loc[i, 'saldo_teorico'])))*12,6)*100
            ratios.at[i,'r_ef_teorico'] = round(((sum(curvas.loc[i, 'ef_teorico'])/sum(curvas.loc[i, 'saldo_teorico'])))*12,6)*100
            ratios.at[i,'r_rebate_teorico'] = round(((sum(curvas.loc[i, 'rebate_teorico'])/sum(curvas.loc[i, 'saldo_teorico'])))*12,6)*100
            ratios.at[i,'r_spread_bruto_teorico'] = ratios.at[i,'r_if_teorico'] + ratios.at[i,'r_ef_teorico'] + ratios.at[i,'r_rebate_teorico']
            ratios.at[i,'r_provisionb_teorico'] = round(((sum(curvas.loc[i, 'provisionb_teorico'])/sum(curvas.loc[i, 'saldo_teorico'])))*12,6)*100
            ratios.at[i,'r_ixs_teorico'] = round(((sum(curvas.loc[i, 'ixs_teorico'])/sum(curvas.loc[i, 'saldo_teorico'])))*12,6)*100
            ratios.at[i,'r_spread_neto_teorico'] = ratios.at[i,'r_spread_bruto_teorico'] - ratios.at[i,'r_provisionb_teorico'] + ratios.at[i,'r_ixs_teorico']
                
            niveles.at[i,'n_if_real'] = round(sum(curvas.loc[i, 'if_real']),0)
            niveles.at[i,'n_ef_real'] = round(sum(curvas.loc[i, 'ef_real']),0)
            niveles.at[i,'n_rebate_real'] = round(sum(curvas.loc[i, 'rebate_real']),0)
            niveles.at[i,'n_spread_bruto_real'] = niveles.at[i,'n_if_real'] + niveles.at[i,'n_ef_real'] + niveles.at[i,'n_rebate_real']
            niveles.at[i,'n_provisionb_real'] = round(sum(curvas.loc[i, 'provisionb_real']),0)
            niveles.at[i,'n_ixs_real'] = round(sum(curvas.loc[i, 'ixs_real']),0)            
            niveles.at[i,'n_spread_neto_real'] = niveles.at[i,'n_spread_bruto_real'] - niveles.at[i,'n_provisionb_real'] + niveles.at[i,'n_ixs_real'] 
            niveles.at[i,'n_saldo_real'] = round(sum(curvas.loc[i, 'saldo_real']),0)
            
            niveles.at[i,'n_if_teorico'] = round(sum(curvas.loc[i, 'if_teorico']),0)
            niveles.at[i,'n_ef_teorico'] = round(sum(curvas.loc[i, 'ef_teorico']),0)
            niveles.at[i,'n_rebate_teorico'] = round(sum(curvas.loc[i, 'rebate_teorico']),0)
            niveles.at[i,'n_spread_bruto_teorico'] = niveles.at[i,'n_if_teorico'] + niveles.at[i,'n_ef_teorico'] + niveles.at[i,'n_rebate_teorico']
            niveles.at[i,'n_provisionb_teorico'] = round(sum(curvas.loc[i, 'provisionb_teorico']),0)
            niveles.at[i,'n_ixs_teorico'] = round(sum(curvas.loc[i, 'ixs_teorico']),0)
            niveles.at[i,'n_spread_neto_teorico'] = niveles.at[i,'n_spread_bruto_teorico'] - niveles.at[i,'n_provisionb_teorico'] + niveles.at[i,'n_ixs_teorico'] 
            niveles.at[i,'n_saldo_teorico'] = round(sum(curvas.loc[i, 'saldo_teorico']),0)

        self.curvas = curvas
        self.ratios = ratios
        self.niveles = niveles
    
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
    
    
    
