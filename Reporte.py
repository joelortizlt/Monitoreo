import pandas as pd
import numpy as np
import pathlib
import dash_core_components as dcc
import dash_html_components as html
from utils import Plotgraph, Barplot, Waterfallplot, FanChart
from InputsNoRevolvente import InputsNoRevolvente
from InputsNoRevolventeReal import InputsNoRevolventeReal
from InputsNoRevolventeTeorico import InputsNoRevolventeTeorico
from OutputsNoRevolvente import OutputsNoRevolvente
from OutputsNoRevolventeReal import OutputsNoRevolventeReal
from OutputsNoRevolventeTeorico import OutputsNoRevolventeTeorico

class Reporte():
    # Constructor del Objeto
    def __init__(self, Real, Teorico, Tmin, mincosecha='', maxcosecha='', filtro1='C_SEGMENTO', 
                    filtro2='C_PLAZO', Producto='XXX', Fecha='XXX', colorListRGB= [ [200,222,255], [153,212,255], [0,99,174] ]):
        product = InputsNoRevolvente(Real, Teorico, mincosecha=mincosecha, maxcosecha=maxcosecha, completar=True)
        product.condensar([filtro1])
        nro_comb_filtro1, nro_comb_filtro2 = 0, len(product.curvas[filtro1].unique())
        product.condensar([filtro2])
        nro_comb_mixto = nro_comb_filtro2 + len(product.curvas[filtro2].unique())
        cortes =  [[[filtro1], nro_comb_filtro1], [[filtro2], nro_comb_filtro2], [[filtro1, filtro2], nro_comb_mixto]] # Valores a usar
        pd_graph_list, can_graph_list, pre_graph_list, comb_size, = [], [], [], []
        report_list_pd, report_list_can, report_list_pre, report_list_tmin  = [], [], [], []
        pd_MAE_graph_list, can_MAE_graph_list, pre_MAE_graph_list, tmin_graph_list, MAE_titles = [], [], [], [], []
        MAE_list = [['MAE_pd', pd_MAE_graph_list], ['MAE_can', can_MAE_graph_list], ['MAE_pre', pre_MAE_graph_list]]
        resumen_descalibrados_pd, resumen_descalibrados_can, resumen_descalibrados_pre = '', '', ''
        pd_alertas_list, can_alertas_list, pre_alertas_list = [], [], []
        resumen_revision_pd, resumen_revision_can, resumen_revision_pre = '', '', ''
        report_list_MAE_pd, report_list_MAE_can, report_list_MAE_pre = [], [], []
        pd_fanChart, can_fanChart, pre_fanChart = [], [], []
        report_list_PDFAN, report_list_CANFAN, report_list_PREFAN = [], [], []
        
        # Producto General
        product = InputsNoRevolvente(Real, Teorico, mincosecha=mincosecha, maxcosecha=maxcosecha, completar=True)
        product.condensar()
        product.optimizar()
        product.impactoTmin(Tmin)

        graph = Plotgraph(product.curvas, promedio=True)
        graph2 = Plotgraph(product.curvas, curvas='Can', nombre='Cancelaciones', promedio=True)
        graph3 = Plotgraph(product.curvas, curvas='Pre', nombre='Prepagos', promedio=True)
        barplot = Barplot(product.stats, grupo='Todos')    
        waterfall = Waterfallplot(df=product.TminProm, promedio=True)
        fanchart, fanchart2 = FanChart(df=product.ci_pd), FanChart(df=product.ci_can, nombre='Cancelaciones')
        fanchart3 = FanChart(df=product.ci_pre, nombre='Prepagos')

        aux = html.P('')

        Lista = [ [('Producto ' + str(Producto) + ' actualizado al ' + str(Fecha), aux, 'product')],
                [('Impacto en tasas', waterfall, 'six columns'), ('Curva de PD', fanchart, 'six columns'), ('Curva de Cancelaciones', fanchart2, 'six columns')],
                [('Intervalos de confianza', barplot, 'six columns'), ('Curva de Prepagos', fanchart3, 'six columns')]
        ]

        # Producto por Cortes
        for corte in cortes:
            product = InputsNoRevolvente(Real, Teorico, mincosecha=mincosecha, maxcosecha=maxcosecha, completar=True)
            product.condensar(corte[0])
            product.optimizar()
            product.impactoTmin(Tmin)

            if corte[0]==[filtro1] or corte[0]==[filtro2]: # MAE - [filtro1], [filtro2] // Sin combinación
                for curva_MAE in MAE_list:
                    barplot = Barplot(product.stats, curva=curva_MAE[0], grupo=corte[0][0], step=len(product.curvas.index))
                    curva_MAE[1].append(barplot)
                comb_size.append(len(product.curvas.index))
                MAE_titles.append(str(corte[0][0])[2:].capitalize())

            if corte[0]==[filtro1]: # Títulos MAE
                valores = product.curvas[filtro1].values
            if corte[0]==[filtro2]:
                for valor in valores:
                    MAE_titles.append(filtro1[2:].capitalize() + ' ' + str(valor))
            
            nro_combinaciones = len(product.curvas.index)
            for combinacion in list(range(nro_combinaciones)):

                pd_graph_list.append(Plotgraph(product.curvas, corte=combinacion)) # Plotgraph PD
                can_graph_list.append(Plotgraph(product.curvas, curvas='Can', nombre='Cancelaciones', corte=combinacion)) # Plotgraph Can
                pre_graph_list.append( Plotgraph(product.curvas, curvas='Pre', nombre='Prepagos', corte=combinacion)) # Plotgraph Pre
                waterfall_aux = True if corte[0]==[filtro1, filtro2] else False
                waterfall = Waterfallplot(product.Tmin, combinacion=combinacion, mixto=waterfall_aux) # Waterfallplot
                tmin_graph_list.append(waterfall)
                pd_fanChart.append(FanChart(product.ci_pd, corte=combinacion))
                can_fanChart.append(FanChart(product.ci_can, nombre='Cancelaciones', corte=combinacion))
                pre_fanChart.append(FanChart(product.ci_pre, nombre='Prepagos', corte=combinacion))

                # Listado de Alertas -> append al mismo vector -> 
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
            # Añadiendo Gráficos de Best Fit, MAE y FanChart [0, 1, 2 - Plotgraph, 3, 4 - BarPlot, 5, 6 - FanChart, 7]
            title_list = [[pd_alertas_list, 'PD', pd_graph_list, report_list_pd, pd_MAE_graph_list, 'MAE_pd', pd_fanChart, report_list_PDFAN], 
                            [can_alertas_list, 'Cancelaciones', can_graph_list, report_list_can, can_MAE_graph_list, 'MAE_can', can_fanChart, report_list_CANFAN],
                            [pre_alertas_list, 'Prepagos', pre_graph_list, report_list_pre, pre_MAE_graph_list, 'MAE_pre', pre_fanChart, report_list_PREFAN]
                        ]
            for title in title_list:
                paragraph, descalibrado, revision, aux_descal, aux_revision = '', '', '', '', ''

                # CORTE 1 Y CORTE 2 (SIN COMBINACIONES):
                if corte[0]==[filtro1] or corte[0]==[filtro2]:
                    # Listado de Alertas:
                    for alerta in list(range(nro_combinaciones)): # Análisis gráfico por gráfico
                        if title[0][alerta + corte[1]]=='Descalibrado':
                            descalibrado = descalibrado + str(product.curvas[corte[0]].values[alerta][0]) + ', '
                        elif title[0][alerta + corte[1]]=='Revisión':
                            revision = revision + str(product.curvas[corte[0]].values[alerta][0]) + ', '
                    if descalibrado=='' and revision=='': # Agregando análisis de Hoja (Corte Específico)
                        paragraph = 'Todos los cortes están calibrados.'
                    if descalibrado!='':
                        paragraph = 'Necesitan calibración: ' + descalibrado[:len(descalibrado)-2] +'. '
                        aux_descal = aux_descal + descalibrado
                    if revision!='':
                        paragraph = paragraph + 'Necesitan revisión: ' + revision[:len(revision)-2] + '.'
                        aux_revision = aux_revision + revision
                    paragraph_html = html.P(paragraph, style={"color": "#ffffff", "fontSize": "40"}) # To HTML
                    html_vacio = html.P('', style={"color": "#ffffff", "fontSize": "40"})

                    # Generación de vector para overview (visualización en Dash)
                    report_list_aux, report_list_aux2 = [], []
                    str1 = str(corte[0][0])[2:].capitalize()
                    report_list_aux.append([(title[1] + ' por ' + str1, paragraph_html, 'product')]) # Tit. Hoja Plotgraph
                    report_list_aux2.append([(title[1] + ' por ' + str1 + ' - Intervalos de Confianza', html_vacio, 'product')]) # Tit. Hoja FanChart
                    for linea in list(range(nro_combinaciones)):
                        str2 = str(product.curvas[corte[0][0]].values[linea]).capitalize() # Título de Gráfico
                        report_list_aux.append([(str1 + ' ' + str2, title[2][corte[1] + linea], 'twelve columns')]) # Plotgraph
                        report_list_aux2.append([(str1 + ' ' + str2, title[6][corte[1] + linea], 'twelve columns')]) # FanChart
                    title[3].append(report_list_aux) # Añadiendo hoja a su stack (report_list) para formar luego reportes específicos
                    title[7].append(report_list_aux2) # Añadiendo hoja a su stack (report_list_FAN) para formar luego reportes específicos  

                    # Tasa Mínima -> Solo corre una vez (if title[1]=='PD') - Generación de vector para overview (visualización en Dash)
                    if title[1]=='PD': 
                        tmin_aux = []
                        tmin_aux.append([('Impacto en Tasa Mínima por ' + str1, html_vacio, 'product')])
                        for linea in list(range(nro_combinaciones)):
                            str2 = str(product.curvas[corte[0][0]].values[linea]).capitalize()
                            tmin_aux.append([(str1 + ' ' + str2, tmin_graph_list[corte[1] + linea], 'twelve columns')]) 
                        report_list_tmin.append(tmin_aux) # Añadiendo hoja a su stack (report_list_TMIN) para formar luego reportes específicos

                # COMBINACIONES DE CORTE 1 Y CORTE 2 (ANÁLISIS GRANULAR)
                else: 

                    auxcorte = corte[1] + 0 # auxcorte = Número de inicio
                    auxcorte2 = nro_comb_mixto - nro_comb_filtro2 # auxcorte2 = Número de valores únicos del segundo filtro
                    auxcorte3 = 0
                    index_size, contador, nro_combinaciones_comb = len(product.curvas.index), 0, []
                    for comb in range(index_size): # Vector de número de combinaciones existentes para cada cruce
                        contador +=1
                        if product.curvas[filtro1][contador]!=product.curvas[filtro1][contador-1]:
                            nro_combinaciones_comb.append(list(range(contador)))
                            contador = 0 
                    
                    # Recorrido granular para cada combinación posible entre ambos filtros:
                    for nro_combinacion in nro_combinaciones_comb: # for 0, 1, 2 ..., n in range(n):

                        paragraph, descalibrado, revision = '', '', ''
                        filtro1value = product.curvas[filtro1].values[auxcorte-7]

                        # Listado de Alertas - Hoja Plotgraph
                        for alerta in nro_combinacion:
                            if title[0][alerta + auxcorte]=='Descalibrado':
                                descalibrado = descalibrado + str(filtro1value) + ' - ' + str(product.curvas[filtro2].values[alerta]) + ', '
                            elif title[0][alerta + auxcorte]=='Revisión':
                                revision = revision + str(filtro1value) + ' - ' + str(product.curvas[filtro2].values[alerta]) + ', '
                        if descalibrado=='' and revision=='':
                            paragraph = 'Todos los cortes están calibrados.'
                        if descalibrado!='':
                            paragraph = 'Necesitan calibración: ' + descalibrado[:len(descalibrado)-2] +'. '
                            aux_descal = aux_descal + descalibrado
                        if revision!='':
                            paragraph = paragraph + 'Necesitan revisión: ' + revision[:len(revision)-2] + '.'
                            aux_revision = aux_revision + revision
                        paragraph_html = html.P(paragraph, style={"color": "#ffffff", "fontSize": "40"}) # To HTML
                        
                        report_list_aux, report_list_aux2 = [], []
                        str0, str1 = str(corte[0][0])[2:].capitalize(), str(corte[0][1])[2:].capitalize()
                        report_list_aux.append([(title[1] + ' para ' + str0 + ' ' + str(filtro1value) + ' por ' + str1, paragraph_html, 'product')]) # Tit. Hoja Plotgraph
                        report_list_aux2.append([(title[1] + ' para ' + str0 + ' ' + str(filtro1value) + ' por ' + str1 + ' - Intervalos de COnfianza',
                                                     paragraph_html, 'product')]) # Tit. Hoja Fanchart
                        for linea in nro_combinacion:
                            str2 = str(product.curvas[filtro2].values[linea]).capitalize()
                            report_list_aux.append([(str1 + ' ' + str2, title[2][auxcorte + linea], 'twelve columns')]) # Plotgraph
                            report_list_aux2.append([(str1 + ' ' + str2, title[6][auxcorte + linea], 'twelve columns')]) # FanChart
                        # MAE
                        barplot = Barplot(product.stats, curva=title[5], grupo=corte[0][1], inicio=auxcorte3, step=comb_size[1]+auxcorte3)
                        title[4].append(barplot)

                        title[3].append(report_list_aux)
                        title[7].append(report_list_aux2)

                        if title[1]=='PD':
                            tmin_aux = []
                            tmin_aux.append([('Impacto en Tasa Mínima para ' + str0 + ' ' + str(filtro1value) + ' por ' + str1, html_vacio, 'product')])
                            for linea in nro_combinacion:
                                str2 = str(product.curvas[filtro2].values[linea]).capitalize()
                                tmin_aux.append([(str1 + ' ' + str2, tmin_graph_list[auxcorte2 + linea], 'twelve columns')]) 
                            auxcorte2 += nro_combinacion[-1]
                            report_list_tmin.append(tmin_aux)
                        
                        auxcorte += max(nro_combinacion)
                        auxcorte3 += max(nro_combinacion)

                if title[1]=='PD':
                    resumen_descalibrados_pd = resumen_descalibrados_pd + aux_descal
                    resumen_revision_pd = resumen_revision_pd + aux_revision
                elif title[1]=='Cancelaciones':
                    resumen_descalibrados_can = resumen_descalibrados_can + aux_descal
                    resumen_revision_can = resumen_revision_can + aux_revision
                else:
                    resumen_descalibrados_pre = resumen_revision_pre + aux_descal
                    resumen_revision_pre = resumen_revision_pre + aux_revision

        aux_resumen = [resumen_descalibrados_pd, resumen_descalibrados_can, resumen_descalibrados_pre, resumen_revision_pd, resumen_revision_can,
                        resumen_revision_pre] # To html
        for aux in aux_resumen:
            if aux!='':
                aux = html.P(aux, style={"color": "#ffffff", "fontSize": "40"}, className='row')
            else:
                aux = html.P('Todos los cortes están calibrados', style={"color": "#ffffff", "fontSize": "40"})

        start_date, end_date = str(mincosecha)[4:] + '-' + str(mincosecha)[:4], str(maxcosecha)[4:] + '-' + str(maxcosecha)[:4] # Fechas de Evaluación
        report_list_resumen = [ [('Resumen de Alertas por '+str0+' y '+str1+' para el Producto '+Producto+' - '+start_date+' al '+end_date, 
                                            html_vacio,'product')],
                                [('Curvas de PD - Descalibrados', resumen_descalibrados_pd, 'product')], [('Curvas de PD - Revisión', resumen_revision_pd, 'product')],
                                [('Curvas de Cancelaciones - Descalibrados', resumen_descalibrados_can, 'product')], [('Curvas de Cancelaciones - Revisión', resumen_revision_can, 'product')],
                                [('Curvas de Prepagos - Descalibrados', resumen_descalibrados_pre, 'product')], [('Curvas de Prepagos - Revisión', resumen_revision_pre, 'product')]   ]

        # # Hoja de MAE: (PD - Cancelaciones - Prepagos)
        # report_list_MAE = [[report_list_MAE_pd, 'PD', pd_MAE_graph_list], [report_list_MAE_can, 'Cancelaciones', can_MAE_graph_list], 
        #                     [report_list_MAE_pre, 'Prepagos', pre_MAE_graph_list]]
        # for report_list in report_list_MAE:
        #     range_MAE = [ [0], [1], list(range(2, len(report_list[2]) + 2)) ] # [Primer filtro]
        #     report_list_aux = []
        #     report_list_aux.append( [('Gráficos MAE - '+ report_list[1], aux2, 'product')] )
        #     for rango in range_MAE:
        #         for rango2 in rango:
        #             report_list_aux.append( [(MAE_titles[rango2], report_list[2][0], 'twelve columns')] )
        #     report_list[0].append(report_list_aux)

        # Reporte Completo
        ListaCompleta = []
        ListaCompleta.append(report_list_resumen) # ListaCompleta[0] = Resumen
        ListaReportes = [report_list_pd, report_list_can, report_list_pre, report_list_PDFAN, report_list_CANFAN, report_list_PREFAN, report_list_tmin]
        for elem in range(len(report_list_tmin)):
            for lista in ListaReportes:
                ListaCompleta.append(lista[elem])
        
        ListaCorte1, ListaCorte2 = [], [] # Reporte por Corte1 / Corte2
        for lista in range(1, 8): # Primeros 7 elementos -> Corte 1
            ListaCorte1.append(ListaCompleta[lista])
        for lista in range(8, 15): # Segundos 7 elementos -> Corte 2
            ListaCorte2.append(ListaCompleta[lista])

        self.ReporteProducto = [Lista]
        self.ReporteCompleto = ListaCompleta
        self.ReporteCorte1 = ListaCorte1
        self.ReporteCorte2 = ListaCorte2

    def Stack(self, Stacker):
        Stacker.append([self.ReporteProducto, self.ReporteCorte1, self.ReporteCorte2, self.ReporteCompleto])