# 0. Librerías *****************************************************************************

import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
from scipy.optimize import minimize

#   Dash
import pathlib
import dash_core_components as dcc
import dash_html_components as html

#   Otros Scripts
from utils_Monitoreo import Header, get_header, Plotgraph, Barplot

# 1. Funciones de Soporte Necesarias *******************************************************

def operation_pd(a, b):
    return b[:a]

def aggr_avg(result_col):
    def avg(x):
        x = [i for i in x if i is not None]
        return sum(x, 0.0000)/len(x)
    filt = list(map(avg, it.zip_longest(*result_col)))
    return filt

def aggr_avg_2(result_col):
    def avg(x):
        x = [i for i in x if i is not None]
        return sum(x, 0.0000)
    filt = list(map(avg, it.zip_longest(*result_col)))
    return filt

#Esta función permite encontrar la posición de un encabezado espeífico (a) en un dataframe (df)
def encontrar_encabezado(df,a):
    n=0
    for i in list(df):
        if i==a:
            pos=n
            break
        n=n+1
    return pos

#Esta función devuelve todos los cortes (c_...)
def all_cortes(df):
    temp=[]
    for i in list(df):
        if str(i)[0:2]=='c_':
            temp.append(i)
    return temp

#Esta funcion lleva los valores de una lista a porcentual
def porcentaje(resultado):
    resultado = [100*x for x in resultado]
    resultado = [round(x,4) for x in resultado]
    return resultado


# 2. Creación de Clases ******************************************************************************

class NoRevolventeReal():
    #constructor del objeto
    def __init__(self,xls,mincosecha="",maxcosecha=""): #se insume un documento de Excel
        
        #tranformar la data de las hojas del excel en dataframes
        df_real = pd.read_excel(xls, 'Reales')
        
        #colocar las curvas en una sola celda
        df_real['prepagos'] = pd.DataFrame({"pd":df_real.iloc[:,encontrar_encabezado(df_real,"PREPAGO_1"):encontrar_encabezado(df_real,"MTODESEMBOLSADO_1")].values.tolist()})
        df_real['desembolso'] = pd.DataFrame({"pd":df_real.iloc[:,encontrar_encabezado(df_real,"MTODESEMBOLSADO_1"):encontrar_encabezado(df_real,"prepagos")].values.tolist()})
        
        #seleccionar solo la data relevante
        df_real = df_real[all_cortes(df_real)+['CODSOLICITUD','COSECHA','FAIL_TYPE', 'SURVIVAL','maxmad','prepagos','desembolso']]
        if mincosecha!="":
            df_real = df_real[df_real['COSECHA']>=mincosecha]
        if maxcosecha!="":
            df_real = df_real[df_real['COSECHA']<=maxcosecha]
        self.df_real = df_real
        
        
        
    #creación de los cortes
    def condensar(self,cortes=[]): #se insume una lista con los cortes que se desea
        
        #si no se ingresa cortes espécificos, se usan todos
        if cortes==[]:
            cortes=all_cortes(self.df_real)
        
        #Creamos la "plantilla"
        curvas = self.df_real.groupby(cortes).size().reset_index().rename(columns={0:'recuento'})
        curvas['pd_real'] = ''
        curvas['can_real'] = ''
        curvas['pre_real'] = ''
        
        #REALES
        for i in range(len(curvas)):
            temp = pd.merge(self.df_real[cortes+['CODSOLICITUD','COSECHA','maxmad','FAIL_TYPE','SURVIVAL','prepagos','desembolso']], pd.DataFrame([curvas.loc[i,:]]), left_on=cortes, right_on=cortes, how='inner')
            
            #pd y cancelaciones reales
            vector = pd.DataFrame()
            c = 0
            surviv = 1
            for j in range(1, temp['maxmad'].max()+1):
                #Count del número de defaults en cada maduración del rango de fechas
                default = temp.query("FAIL_TYPE == 1" + " & SURVIVAL=="+str(j))['SURVIVAL'].count()
                #Count del número de cancelaciones en cada maduración del rango de fechas
                cancel = temp.query("FAIL_TYPE == 2" + " & SURVIVAL=="+str(j))['SURVIVAL'].count()
                #Count del número de cuentas en cada maduración tomando en cuenta la máxima maduración y rango de fechas
                dem = temp.query("maxmad>=" + str(j))['SURVIVAL'].count()
                #Marginales
                pd_marginal = None
                if not dem == 0:
                    pd_marginal = default/dem
                    can_marginal = cancel/dem
                can_final = surviv*can_marginal
                surviv = (1-pd_marginal-can_marginal)*surviv
                #Agregar a la tabla
                vector.loc[c, "pd_marginal"] = pd_marginal
                vector.loc[c, "can_final"] = can_final
                c = c + 1
                
            resultado = vector["pd_marginal"].cumsum()
            curvas.at[i,'pd_real'] = porcentaje(resultado)

            resultado = vector["can_final"].cumsum()
            curvas.at[i,'can_real'] = porcentaje(resultado)
            
            #prepagos reales
            temp["sum_prepagos"]=list(map(operation_pd, temp["maxmad"], temp["prepagos"]))
            temp["sum_desembolso"]=list(map(operation_pd, temp["maxmad"], temp["desembolso"]))    
            a = aggr_avg_2(temp['sum_prepagos'])
            b = aggr_avg_2(temp['sum_desembolso'])
            resultado = [ai / bi for ai, bi in zip(a, b)]
            resultado = np.cumsum(resultado)
            curvas.at[i,'pre_real'] = porcentaje(resultado)
        
        self.curvas = curvas


class NoRevolventeTeorico():
    #constructor del objeto
    def __init__(self,xls,mincosecha="",maxcosecha=""): #se insume un documento de Excel
        
        #tranformar la data de las hojas del excel en dataframes
        df_pd = pd.read_excel(xls, 'PD')
        df_can = pd.read_excel(xls, 'Can')
        df_pre = pd.read_excel(xls, 'Pre')
        
        #colocar las curvas en una sola celda
        df_pd['pd_marginal'] = pd.DataFrame({'pd':df_pd.iloc[:,encontrar_encabezado(df_pd,1):].values.tolist()})
        df_can['can_marginal'] = pd.DataFrame({'pd':df_can.iloc[:,encontrar_encabezado(df_can,1):].values.tolist()})
        df_pre['pre_marginal'] = pd.DataFrame({'pd':df_pre.iloc[:,encontrar_encabezado(df_pre,1):].values.tolist()})
 
        #seleccionar solo la data relevante
        df_pd = df_pd[all_cortes(df_pd)+['CODSOLICITUD','COSECHA','maxmad','pd_marginal']]
        df_can = df_can[all_cortes(df_can)+['CODSOLICITUD','COSECHA','maxmad','can_marginal']]
        df_pre = df_pre[all_cortes(df_pre)+['CODSOLICITUD','COSECHA','maxmad','pre_marginal']]
        
        if mincosecha!="":
            df_pd = df_pd[df_pd['COSECHA']>=mincosecha]
            df_can = df_can[df_can['COSECHA']>=mincosecha]
            df_pre = df_pre[df_pre['COSECHA']>=mincosecha]
        if maxcosecha!="":
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
            cortes=all_cortes(self.df_pd)

        #Creamos la "plantilla"
        curvas = self.df_pd.groupby(cortes).size().reset_index().rename(columns={0:'recuento'})
        curvas["pd_teorica"] = ''
        curvas["can_teorica"] = ''
        curvas["pre_teorica"] = ''
        
        #TEÓRICAS
        for i in range(len(curvas)):
            
            #pd teórica
            temp = pd.merge(self.df_pd[cortes+['CODSOLICITUD','COSECHA','maxmad','pd_marginal']], pd.DataFrame([curvas.loc[i,:]]), left_on=cortes, right_on=cortes, how='inner')
            temp["result"] = list(map(operation_pd, temp["maxmad"], temp["pd_marginal"]))
            resultado = aggr_avg(temp['result'])
            resultado = np.cumsum(resultado)  
            curvas.at[i,'pd_teorica'] = porcentaje(resultado)
            
            #cancelaciones teórica
            temp = pd.merge(self.df_can[cortes+['CODSOLICITUD','COSECHA','maxmad','can_marginal']], pd.DataFrame([curvas.loc[i,:]]), left_on=cortes, right_on=cortes, how='inner')
            temp["result"]=list(map(operation_pd, temp["maxmad"], temp["can_marginal"]))
            resultado = aggr_avg(temp['result'])
            resultado = np.cumsum(resultado)   
            curvas.at[i,'can_teorica'] = porcentaje(resultado)
            
            #prepagos teórica
            temp = pd.merge(self.df_pre[cortes+['CODSOLICITUD','COSECHA','maxmad','pre_marginal']], pd.DataFrame([curvas.loc[i,:]]), left_on=cortes, right_on=cortes, how='inner')
            temp["result"]=list(map(operation_pd, temp["maxmad"], temp["pre_marginal"]))
            resultado = aggr_avg(temp['result'])
            resultado = np.cumsum(resultado)
            curvas.at[i,'pre_teorica'] = porcentaje(resultado)

        self.curvas = curvas

class NoRevolvente():
    #constructor del objeto
    def __init__(self,NRR,NRT): #se insumen 2 objetos (uno real y uno teorico)
        curvas = pd.merge(left=NRR.curvas, right=NRT.curvas, how='left', left_on=all_cortes(NRR.curvas), right_on=all_cortes(NRT.curvas))
        curvas['check']=curvas['recuento_x']-curvas['recuento_y']
        curvas = curvas.rename(columns={'recuento_x':'recuento'}).drop('recuento_y',1)
        
        stats = curvas[all_cortes(curvas)+['recuento']].copy()
        
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
        cortes_temp = all_cortes(self.curvas)
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
        cortes_temp = all_cortes(self.stats)
            
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

# 3. Generación de Objetos **********************************************************************************************************************

xls_product = pd.ExcelFile('C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\\6. Reporte_Monitoreo\Data\Vehicular.xlsx')

# Generación de Variables Útiles 'vacías'
pd_graph_list, can_graph_list, pre_graph_list = [], [], []
pd_alertas_list, can_alertas_list, pre_alertas_list = [], [], []
report_list_pd, report_list_can, report_list_pre  = [], [], []
pd_MAE_graph_list, can_MAE_graph_list, pre_MAE_graph_list = [], [], []
resumen_descalibrados_pd, resumen_descalibrados_can, resumen_descalibrados_pre = '', '', ''
resumen_revision_pd, resumen_revision_can, resumen_revision_pre = '', '', ''
comb_size = []
MAE_titles = []

filtro1 = 'c_riesgo'
filtro2 = 'c_plazo'
nro_comb_filtro1, nro_comb_filtro2, nro_comb_mixto = 0, 5, 10

cortes =  [[[filtro1], nro_comb_filtro1], [[filtro2], nro_comb_filtro2], [[filtro1, filtro2], nro_comb_mixto]]

MAE_list = [['MAE_pd', pd_MAE_graph_list], ['MAE_can', can_MAE_graph_list], ['MAE_pre', pre_MAE_graph_list]]

for corte in cortes:
    productR = NoRevolventeReal(xls_product)
    productR.condensar(corte[0])
    productT = NoRevolventeTeorico(xls_product)
    productT.condensar(corte[0])
    product = NoRevolvente(productR,productT)
    product.optimizar()
    product.curvas
    product.stats

    if corte[0]==['c_plazo']:
        product.curvas = product.curvas.drop(index=[5])
    if corte[0]==['c_riesgo', 'c_plazo']:
        product.curvas = product.curvas.drop(index=[5, 11, 17, 23, 29]) # Drop plazo 72 en todas las combinaciones
        product.curvas.index = list(range(25))

    # MAE - Barplots
    if corte[0]==[filtro1] or corte[0]==[filtro2]:
        for tipo_curva in MAE_list:
            barplot = Barplot(product.stats, curva=tipo_curva[0], grupo=corte[0][0])    
            tipo_curva[1].append(barplot)
        comb_size.append(len(product.curvas.index))
        MAE_titles.append(str(corte[0][0])[2:].capitalize())
    
    if corte[0]==[filtro1]:
        valores = product.curvas[filtro1].values
    if corte[0]==[filtro2]:
        for valor in valores:
            MAE_titles.append(filtro1[2:].capitalize() + ' ' + valor)

    nro_combinaciones = len(product.curvas.index)

    for combinacion in list(range(nro_combinaciones)):

        # Gráficos:
        graph = Plotgraph(product.curvas, corte=combinacion)
        pd_graph_list.append(graph)

        graph2 = Plotgraph(product.curvas, curvas='Cancelaciones', corte=combinacion)
        can_graph_list.append(graph2)

        graph3 = Plotgraph(product.curvas, curvas='Prepago', corte=combinacion)
        pre_graph_list.append(graph3)

        # Listado de  alertas:
        for mae in MAE_list:

            if product.stats[mae[0]][combinacion] > 3:
                aux_lista = 'Descalibrado'
            elif product.stats[mae[0]][combinacion] >= 2.5 and product.stats[mae[0]][combinacion] < 3:
                aux_lista = 'Revisión'
            else:
                aux_lista = 'Calibrado'
                
            if mae[0]=='MAE_pd':
                pd_alertas_list.append(aux_lista)
            elif mae[0]=='MAE_can':
                can_alertas_list.append(aux_lista)
            elif mae[0]=='MAE_pre':
                pre_alertas_list.append(aux_lista)

    title_list = [[pd_alertas_list, 'PD', pd_graph_list, report_list_pd, pd_MAE_graph_list, 'MAE_pd'], 
                    [can_alertas_list, 'Cancelaciones', can_graph_list, report_list_can, can_MAE_graph_list, 'MAE_can'],
                    [pre_alertas_list, 'Prepagos', pre_graph_list, report_list_pre, pre_MAE_graph_list, 'MAE_pre'] 
                ]

    for title in title_list:

        paragraph, descalibrado, revision, aux_descal, aux_revision = '', '', '', '', ''

        if corte[0]==[filtro1] or corte[0]==[filtro2]:

            for alerta in list(range(nro_combinaciones)):
                if title[0][alerta + corte[1]]=='Descalibrado':
                    descalibrado = descalibrado + str(product.curvas[corte[0]].values[alerta][0]) + ', '

                elif title[0][alerta + corte[1]]=='Revisión':
                    revision = revision + str(product.curvas[corte[0]].values[alerta][0]) + ', '

            if descalibrado=='' and revision=='':
                paragraph = 'Todos los cortes están calibrados.'
            if descalibrado!='':
                paragraph = 'Necesitan calibración: ' + descalibrado[:len(descalibrado)-2] +'. '
                aux_descal = aux_descal + descalibrado
            if revision!='':
                paragraph = paragraph + 'Necesitan revisión: ' + revision[:len(revision)-2] + '.'
                aux_revision = aux_revision + revision

            paragraph_html = html.P(paragraph, style={"color": "#ffffff", "fontSize": "40"})

            report_list_aux = []
            str1 = str(corte[0][0])[2:].capitalize()
            report_list_aux.append([(title[1] + ' por ' + str1, paragraph_html, 'product')])
            for linea in list(range(nro_combinaciones)):
                str2 = str(product.curvas[corte[0][0]].values[linea]).capitalize()
                report_list_aux.append([(str1 + ' ' + str2, title[2][corte[1] + linea], 'twelve columns')])
                 
            title[3].append(report_list_aux)
        
        else:

            # nro_combinaciones_comb = []
            # for nro in list(range(nro_combinaciones)):
            #     nro_combinaciones_comb.append(list(range(nro_combinaciones)))

            auxcorte = corte[1] + 0

            nro_combinaciones_comb = [list(range(5)), list(range(5)), list(range(5)), list(range(5)), list(range(5))]   

            for nro_combinacion in nro_combinaciones_comb:

                paragraph = ''
                descalibrado = ''
                revision = '' 
                filtro1value = product.curvas[filtro1].values[auxcorte-10]

                for alerta in nro_combinacion:
                    if title[0][alerta + auxcorte]=='Descalibrado':
                        descalibrado = descalibrado + filtro1value + ' - ' + str(product.curvas[filtro2].values[alerta]) + ', '

                    elif title[0][alerta + auxcorte]=='Revisión':
                        revision = revision + filtro1value + ' - ' + str(product.curvas[filtro2].values[alerta]) + ', '

                if descalibrado=='' and revision=='':
                    paragraph = 'Todos los cortes están calibrados.'
                if descalibrado!='':
                    paragraph = 'Necesitan calibración: ' + descalibrado[:len(descalibrado)-2] +'. '
                    aux_descal = aux_descal + descalibrado
                if revision!='':
                    paragraph = paragraph + 'Necesitan revisión: ' + revision[:len(revision)-2] + '.'
                    aux_revision = aux_revision + revision

                paragraph_html = html.P(paragraph, style={"color": "#ffffff", "fontSize": "40"})

                report_list_aux = []
                str0 = str(corte[0][0])[2:].capitalize()
                str1 = str(corte[0][1])[2:].capitalize()
                report_list_aux.append([(title[1] + ' para ' + str0 + ' ' + filtro1value + ' por ' + str1, paragraph_html, 'product')])
                for linea in nro_combinaciones_comb[0]:
                    str2 = str(product.curvas[filtro2].values[linea]).capitalize()
                    report_list_aux.append([(str1 + ' ' + str2, title[2][auxcorte + linea], 'twelve columns')])
                    # MAE
                    barplot = Barplot(product.stats, curva=title[5], grupo=corte[0][1])
                    title[4].append(barplot)

                auxcorte = auxcorte + 5

                title[3].append(report_list_aux)

        if title[1]=='PD':
            resumen_descalibrados_pd = resumen_descalibrados_pd + aux_descal
            resumen_revision_pd = resumen_revision_pd + aux_revision
        elif title[1]=='Cancelaciones':
            resumen_descalibrados_can = resumen_descalibrados_can + aux_descal
            resumen_revision_can = resumen_revision_can + aux_revision
        else:
            resumen_descalibrados_pre = resumen_revision_pre + aux_descal
            resumen_revision_pre = resumen_revision_pre + aux_revision

# To html
aux_resumen = [resumen_descalibrados_pd, resumen_descalibrados_can, resumen_descalibrados_pre, resumen_revision_pd, resumen_revision_can,
                resumen_revision_pre]
for aux in aux_resumen:
    if aux!='':
        aux = html.P(aux, style={"color": "#ffffff", "fontSize": "40"}, className='row')
    else:
        aux = html.P('Todos los cortes están calibrados', style={"color": "#ffffff", "fontSize": "40"})

aux2 = html.P(' ', style={"color": "#ffffff", "fontSize": "40"}, className='row')

report_list_resumen = [ [('Resumen de Alertas por Riesgo y Plazo', aux2,'product')],
                        [('Curvas de PD - Descalibrados', resumen_descalibrados_pd, 'product')],
                        [('Curvas de PD - Revisión', resumen_revision_pd, 'product')],
                        [('Curvas de Cancelaciones - Descalibrados', resumen_descalibrados_can, 'product')],
                        [('Curvas de Cancelaciones - Revisión', resumen_revision_can, 'product')],
                        [('Curvas de Prepagos - Descalibrados', resumen_descalibrados_pre, 'product')],
                        [('Curvas de Prepagos - Revisión', resumen_revision_pre, 'product')]
]

report_list_MAE_pd, report_list_MAE_can, report_list_MAE_pre = [], [], []
report_list_MAE = [[report_list_MAE_pd, 'PD', pd_MAE_graph_list], [report_list_MAE_can, 'Cancelaciones', can_MAE_graph_list], 
                    [report_list_MAE_pre, 'Prepagos', pre_MAE_graph_list]]

for report_list in report_list_MAE:
    range_MAE = [ [0], [1], list(range(2, comb_size[1]+2)) ]
    report_list_aux = []
    report_list_aux.append( [('Gráficos MAE - '+ report_list[1], aux2, 'product')] )
    for rango in range_MAE:
        for rango2 in rango:
            report_list_aux.append( [(MAE_titles[rango2], report_list[2][rango2], 'twelve columns')] )
    report_list[0].append(report_list_aux)


import dash
from dash.dependencies import Input, Output
from pages import overview

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('data').resolve()
ASSETS_PATH = PATH.joinpath('assets').resolve()

# 6. Layout **************************************************************************************************************************************************************

# Application
app = dash.Dash(
    __name__, meta_tags=[{'name': 'viewport', 'content': 'width=device-width'}]
)

# Describe the layout/UI of the app
app.layout = html.Div(
    [dcc.Location(id='url', refresh=False), html.Div(id='page-content')]
)

# Update page
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])

def display_page(pathname):
    
    return (
        overview.create_layout(app, report_list_resumen),
        overview.create_layout(app, report_list_pd[0]),
        overview.create_layout(app, report_list_can[0]),
        overview.create_layout(app, report_list_pre[0]),
        overview.create_layout(app, report_list_pd[1]),
        overview.create_layout(app, report_list_can[1]),
        overview.create_layout(app, report_list_pre[1]),
        overview.create_layout(app, report_list_pd[2]),
        overview.create_layout(app, report_list_can[2]),
        overview.create_layout(app, report_list_pre[2]),
        overview.create_layout(app, report_list_pd[3]),
        overview.create_layout(app, report_list_can[3]),
        overview.create_layout(app, report_list_pre[3]),
        overview.create_layout(app, report_list_pd[4]),
        overview.create_layout(app, report_list_can[4]),
        overview.create_layout(app, report_list_pre[4]),
        overview.create_layout(app, report_list_pd[5]),
        overview.create_layout(app, report_list_can[5]),
        overview.create_layout(app, report_list_pre[5]),
        overview.create_layout(app, report_list_pd[6]),
        overview.create_layout(app, report_list_can[6]),
        overview.create_layout(app, report_list_pre[6]),
        overview.create_layout(app, report_list_MAE_pd[0]),
        overview.create_layout(app, report_list_MAE_can[0]),
        overview.create_layout(app, report_list_MAE_pre[0]),
    )

if __name__=='__main__':
    app.run_server(debug=True)