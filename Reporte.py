# Librerias
import pandas as pd
import numpy as np

# Funciones de Apoyo
import pathlib
import dash_core_components as dcc
import dash_html_components as html
from utils import Plotgraph, Barplot, Waterfallplot

# Clases
from InputsNoRevolvente import InputsNoRevolvente
from InputsNoRevolventeReal import InputsNoRevolventeReal
from InputsNoRevolventeTeorico import InputsNoRevolventeTeorico
from OutputsNoRevolvente import OutputsNoRevolvente
from OutputsNoRevolventeReal import OutputsNoRevolventeReal
from OutputsNoRevolventeTeorico import OutputsNoRevolventeTeorico

# Class - Reporte
class Reporte():
    
    # Constructor del Objeto
    def __init__(self, Real, Teorico, Tmin, filtro1, filtro2, nro_comb_filtro1=0, nro_comb_filtro2=4, nro_comb_mixto=7 ):

        cortes =  [[[filtro1], nro_comb_filtro1], [[filtro2], nro_comb_filtro2], [[filtro1, filtro2], nro_comb_mixto]]

        pd_graph_list, can_graph_list, pre_graph_list = [], [], []
        pd_alertas_list, can_alertas_list, pre_alertas_list = [], [], []
        report_list_pd, report_list_can, report_list_pre  = [], [], []
        pd_MAE_graph_list, can_MAE_graph_list, pre_MAE_graph_list = [], [], []
        resumen_descalibrados_pd, resumen_descalibrados_can, resumen_descalibrados_pre = '', '', ''
        resumen_revision_pd, resumen_revision_can, resumen_revision_pre = '', '', ''
        comb_size = []
        report_list_MAE_pd, report_list_MAE_can, report_list_MAE_pre, report_list_tmin = [], [], [], []
        MAE_titles = []
        tmin_graph_list = []
        MAE_list = [['MAE_pd', pd_MAE_graph_list], ['MAE_can', can_MAE_graph_list], ['MAE_pre', pre_MAE_graph_list]]

        # 2. Generación de Objetos:

        product = InputsNoRevolvente(Real, Teorico, completar=True)

        for corte in cortes:
            product = InputsNoRevolvente(Real, Teorico, completar=True)
            product.condensar(corte[0])
            product.optimizar()
            product.impactoTmin(Tmin)

            # MAE - [filtro1], [filtro2] // Sin combinación
            if corte[0]==[filtro1] or corte[0]==[filtro2]:
                for curva_MAE in MAE_list:
                    barplot = Barplot(product.stats, curva=curva_MAE[0], grupo=corte[0][0], step=len(product.curvas.index))
                    curva_MAE[1].append(barplot)
                comb_size.append(len(product.curvas.index))
                MAE_titles.append(str(corte[0][0])[2:].capitalize())

            # Títulos MAE
            if corte[0]==[filtro1]:
                valores = product.curvas[filtro1].values
            if corte[0]==[filtro2]:
                for valor in valores:
                    MAE_titles.append(filtro1[2:].capitalize() + ' ' + str(valor))
            
            nro_combinaciones = len(product.curvas.index)

            for combinacion in list(range(nro_combinaciones)):

                graph = Plotgraph(product.curvas, corte=combinacion)
                pd_graph_list.append(graph)
                graph2 = Plotgraph(product.curvas, curvas='Can', nombre='Cancelaciones', corte=combinacion)
                can_graph_list.append(graph2)
                graph3 = Plotgraph(product.curvas, curvas='Pre', nombre='Prepagos', corte=combinacion)
                pre_graph_list.append(graph3)
                if corte[0]==[filtro1, filtro2]:
                    waterfall = Waterfallplot(product.Tmin, combinacion=combinacion, mixto=True)
                else:
                    waterfall = Waterfallplot(product.Tmin, combinacion=combinacion, mixto=False)
                tmin_graph_list.append(waterfall)

                # Listado de Alertas:
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
                            [pre_alertas_list, 'Prepagos', pre_graph_list, report_list_pre, pre_MAE_graph_list, 'MAE_pre'], 
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
                    html_vacio = html.P('', style={"color": "#ffffff", "fontSize": "40"})

                    report_list_aux = []

                    str1 = str(corte[0][0])[2:].capitalize()
                    report_list_aux.append([(title[1] + ' por ' + str1, paragraph_html, 'product')])

                    for linea in list(range(nro_combinaciones)):
                        str2 = str(product.curvas[corte[0][0]].values[linea]).capitalize()
                        report_list_aux.append([(str1 + ' ' + str2, title[2][corte[1] + linea], 'twelve columns')]) 
                    title[3].append(report_list_aux)

                    if title[1]=='PD':
                        tmin_aux = []
                        tmin_aux.append([('Impacto en Tasa Mínima por ' + str1, html_vacio, 'product')])
                        for linea in list(range(nro_combinaciones)):
                            str2 = str(product.curvas[corte[0][0]].values[linea]).capitalize()
                            tmin_aux.append([(str1 + ' ' + str2, tmin_graph_list[corte[1] + linea], 'twelve columns')]) 
                        report_list_tmin.append(tmin_aux)
                
                else:

                    auxcorte = corte[1] + 0
                    auxcorte2 = 3
                    auxcorte3 = 0

                    nro_combinaciones_comb = [list(range(3)), list(range(3)), list(range(3)), list(range(2))]  

                    for nro_combinacion in nro_combinaciones_comb:

                        paragraph, descalibrado, revision = '', '', ''
                        filtro1value = product.curvas[filtro1].values[auxcorte-7]

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
                        for linea in nro_combinacion:
                            str2 = str(product.curvas[filtro2].values[linea]).capitalize()
                            report_list_aux.append([(str1 + ' ' + str2, title[2][auxcorte + linea], 'twelve columns')])
                        # MAE
                        barplot = Barplot(product.stats, curva=title[5], grupo=corte[0][1], inicio=auxcorte3, step=comb_size[1]+auxcorte3)
                        title[4].append(barplot)

                        title[3].append(report_list_aux)

                        if title[1]=='PD':
                            tmin_aux = []
                            tmin_aux.append([('Impacto en Tasa Mínima para ' + str0 + ' ' + filtro1value + ' por ' + str1, html_vacio, 'product')])
                            for linea in nro_combinacion:
                                str2 = str(product.curvas[filtro2].values[linea]).capitalize()
                                tmin_aux.append([(str1 + ' ' + str2, tmin_graph_list[auxcorte2 + linea], 'twelve columns')]) 
                            auxcorte2 += 3
                            report_list_tmin.append(tmin_aux)
                        
                        auxcorte += 3
                        auxcorte3 += comb_size[1]

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

        report_list_MAE = [[report_list_MAE_pd, 'PD', pd_MAE_graph_list], [report_list_MAE_can, 'Cancelaciones', can_MAE_graph_list], 
                            [report_list_MAE_pre, 'Prepagos', pre_MAE_graph_list]]

        for report_list in report_list_MAE:
            range_MAE = [ [0], [1], list(range(2, comb_size[0]+2)) ]
            report_list_aux = []
            report_list_aux.append( [('Gráficos MAE - '+ report_list[1], aux2, 'product')] )
            for rango in range_MAE:
                for rango2 in rango:
                    report_list_aux.append( [(MAE_titles[rango2], report_list[2][rango2], 'twelve columns')] )
            report_list[0].append(report_list_aux)

        ListaCompleta = [report_list_resumen, report_list_pd[0], report_list_can[0], report_list_pre[0], report_list_tmin[0],
                        report_list_pd[1], report_list_can[1], report_list_pre[1], report_list_tmin[1],
                        report_list_pd[2], report_list_can[2], report_list_pre[2], report_list_tmin[2],
                        report_list_pd[3], report_list_can[3], report_list_pre[3], report_list_tmin[3],
                        report_list_pd[4], report_list_can[4], report_list_pre[4], report_list_tmin[4],
                        report_list_pd[5], report_list_can[5], report_list_pre[5], report_list_tmin[5],
                        report_list_MAE_pd[0], report_list_MAE_can[0], report_list_MAE_pre[0]   ]

        ListaCorte1, ListaCorte2 = [], []
        for lista in range(1, 5):
            ListaCorte1.append(ListaCompleta[lista])
        for lista in range(5, 9):
            ListaCorte2.append(ListaCompleta[lista])

        self.ReporteCompleto = ListaCompleta
        self.ReporteCorte1 = ListaCorte1
        self.ReporteCorte2 = ListaCorte2

    def Stack(self, Stacker):
        Stacker.append([self.ReporteCorte1, self.ReporteCorte2, self.ReporteCompleto])