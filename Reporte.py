import pandas as pd
import numpy as np
import pathlib
import dash_core_components as dcc
import dash_html_components as html
from utils import Plotgraph, Barplot, Waterfallplot, FanChart, paragraph_alertas
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
        # Obteniendo parámetros de ejecución (inicio_comb_filtro2, inicio_comb_mixto)
        product = InputsNoRevolvente(Real, Teorico, mincosecha=mincosecha, maxcosecha=maxcosecha, completar=True)
        product.condensar([filtro1])
        inicio_comb_filtro2 = len(product.curvas[filtro1].unique())
        product.condensar([filtro2])
        inicio_comb_mixto = inicio_comb_filtro2 + len(product.curvas[filtro2].unique())
        cortes =  [[[filtro1], 0], [[filtro2], inicio_comb_filtro2], [[filtro1, filtro2], inicio_comb_mixto]] # <-- Valores a usar
        # Listas que se van a rellenar con los bucles (se muestran en el reporte los report_list)
        pd_graph_list, can_graph_list, pre_graph_list, comb_size, = [], [], [], []
        pd_MAE_graph_list, can_MAE_graph_list, pre_MAE_graph_list, tmin_graph_list = [], [], [], []
        pd_fanChart, can_fanChart, pre_fanChart = [], [], []
        report_list_pd, report_list_can, report_list_pre, report_list_tmin  = [], [], [], []
        report_list_MAE_pd, report_list_MAE_can, report_list_MAE_pre, MAE_titles = [], [], [], []
        report_list_PDFAN, report_list_CANFAN, report_list_PREFAN = [], [], []
        resumen_descalibrados_pd, resumen_descalibrados_can, resumen_descalibrados_pre = '', '', ''
        resumen_revision_pd, resumen_revision_can, resumen_revision_pre = '', '', ''
        pd_alertas_list, can_alertas_list, pre_alertas_list = [], [], []
        MAE_list = [['MAE_pd', pd_MAE_graph_list], ['MAE_can', can_MAE_graph_list], ['MAE_pre', pre_MAE_graph_list]] # <-- Valores a usar
        
        # Producto General -- [Lista]
        product.condensar()
        product.optimizar()
        product.impactoTmin(Tmin)
        graph = Plotgraph(product.curvas, promedio=True)
        graph2 = Plotgraph(product.curvas, curvas='Can', nombre='Cancelaciones', promedio=True)
        graph3 = Plotgraph(product.curvas, curvas='Pre', nombre='Prepagos', promedio=True)
        barplot, waterfall = Barplot(product.stats, grupo='Todos'),  Waterfallplot(df=product.TminProm, promedio=True)    
        fanchart, fanchart2 = FanChart(df=product.ci_pd), FanChart(df=product.ci_can, nombre='Cancelaciones')
        fanchart3 = FanChart(df=product.ci_pre, nombre='Prepagos')
        html_vacio = html.P('')
        Lista = [ [('Producto ' + str(Producto) + ' actualizado al ' + str(Fecha), html_vacio, 'product')],
                [('Impacto en tasas', waterfall, 'six columns'), ('Curva de PD', fanchart, 'six columns'), ('Curva de Cancelaciones', fanchart2, 'six columns')],
                [('Intervalos de confianza', barplot, 'six columns'), ('Curva de Prepagos', fanchart3, 'six columns')]
        ]

        # Producto por Cortes [ListaCorte1, ListaCorte2, ListaCompleta]
        for corte in cortes:
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
                pd_fanChart.append(FanChart(product.ci_pd, corte=combinacion))
                can_fanChart.append(FanChart(product.ci_can, nombre='Cancelaciones', corte=combinacion))
                pre_fanChart.append(FanChart(product.ci_pre, nombre='Prepagos', corte=combinacion))
                waterfall_aux = True if corte[0]==[filtro1, filtro2] else False
                waterfall = Waterfallplot(product.Tmin, combinacion=combinacion, mixto=waterfall_aux) # Waterfallplot
                tmin_graph_list.append(waterfall)

                # Listado de Alertas -> append a la lista correspondiente 
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

                aux_descal, aux_revision = '', ''
                # CORTE 1 Y CORTE 2 (SIN COMBINACIONES):
                if corte[0]==[filtro1] or corte[0]==[filtro2]:
                    # Listado de Alertas:
                    paragraph_html, aux_descal, aux_revision = paragraph_alertas(product.curvas, title[0],list(range(nro_combinaciones)), corte[1], 
                                                                                    corte[0], aux_descal, aux_revision)

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
                    nro_valores_filtro2 = inicio_comb_mixto - inicio_comb_filtro2 # + 1 nro_valores_filtro2 = Número de valores únicos del segundo filtro
                    aux_barplot, rep = 0, 0

                    nro_combinaciones_comb = []
                    unicos_filtro1 = product.curvas[filtro1].unique() # Nro de combinaciones para cada elemento del primer filtro
                    for ElemFiltro1 in unicos_filtro1:
                        nro_combinaciones_comb.append(list(range(list(product.curvas[filtro1].values).count(ElemFiltro1))))

                    # Recorrido granular para cada combinación posible entre ambos filtros:
                    for nro_combinacion in nro_combinaciones_comb: # for 0, 1, 2 ..., n in range(n):

                        ValorFiltro1 = str(unicos_filtro1[rep])
                        paragraph_html, aux_descal, aux_revision = paragraph_alertas(product.curvas, title[0], nro_combinacion, auxcorte, filtro2, 
                                                                aux_descal, aux_revision, Combinacion=True, ValorFiltro1=ValorFiltro1)
                        
                        report_list_aux, report_list_aux2 = [], []
                        str0, str1 = str(corte[0][0])[2:].capitalize(), str(corte[0][1])[2:].capitalize()
                        report_list_aux.append([(title[1] + ' para ' + str0 + ' ' + str(ValorFiltro1) + ' por ' + str1, paragraph_html, 'product')]) # Tit. Hoja Plotgraph
                        report_list_aux2.append([(title[1] + ' para ' + str0 + ' ' + str(ValorFiltro1) + ' por ' + str1 + ' - Intervalos de Confianza',
                                                     paragraph_html, 'product')]) # Tit. Hoja Fanchart
                        for linea in nro_combinacion:
                            str2 = str(product.curvas[filtro2].values[linea]).capitalize()
                            report_list_aux.append([(str1 + ' ' + str2, title[2][auxcorte + linea], 'twelve columns')]) # Plotgraph
                            report_list_aux2.append([(str1 + ' ' + str2, title[6][auxcorte + linea], 'twelve columns')]) # FanChart
                        # MAE
                        barplot = Barplot(product.stats, curva=title[5], grupo=corte[0][1], inicio=aux_barplot, step=comb_size[1]+aux_barplot)
                        title[4].append(barplot)

                        title[3].append(report_list_aux)
                        title[7].append(report_list_aux2)

                        if title[1]=='PD': # T min: 1 sola vez
                            tmin_aux = []
                            tmin_aux.append([('Impacto en Tasa Mínima para ' + str0 + ' ' + str(ValorFiltro1) + ' por ' + str1, html_vacio, 'product')])
                            for linea in nro_combinacion:
                                str2 = str(product.curvas[filtro2].values[linea]).capitalize()
                                tmin_aux.append([(str1 + ' ' + str2, tmin_graph_list[nro_valores_filtro2 + linea], 'twelve columns')]) 
                            nro_valores_filtro2 += nro_combinacion[-1]
                            report_list_tmin.append(tmin_aux)
                        
                        auxcorte += max(nro_combinacion)
                        aux_barplot += max(nro_combinacion)
                        rep +=1

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

        # Hoja de MAE: (PD - Cancelaciones - Prepagos)
        report_list_MAE = [[report_list_MAE_pd, 'PD', pd_MAE_graph_list], [report_list_MAE_can, 'Cancelaciones', can_MAE_graph_list], 
                            [report_list_MAE_pre, 'Prepagos', pre_MAE_graph_list]]
        range_MAE_title = range(len(report_list_MAE[0][2]))
        for report_list in report_list_MAE:
            report_list_aux = []
            report_list_aux.append( [('Gráficos MAE - '+ report_list[1], html_vacio, 'product' ) ] )
            for rango in range_MAE_title:
                report_list_aux.append( [(MAE_titles[rango], report_list[2][rango], 'twelve columns')] )
            report_list[0].append(report_list_aux)

        # Reporte Completo
        ListaCompleta = []
        ListaCompleta.append(report_list_resumen) # ListaCompleta[0] = Resumen
        ListaReportes = [report_list_pd, report_list_can, report_list_pre, report_list_PDFAN, report_list_CANFAN, report_list_PREFAN, report_list_tmin]
        for combinacion in range(len(report_list_tmin)): # in range(número listas final: 2 + numero de combinaciones entre ambos cortes)
            for lista in ListaReportes:
                ListaCompleta.append(lista[combinacion])
        ListaCompleta.append(report_list_MAE_pd[0])
        ListaCompleta.append(report_list_MAE_can[0])
        ListaCompleta.append(report_list_MAE_pre[0])

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