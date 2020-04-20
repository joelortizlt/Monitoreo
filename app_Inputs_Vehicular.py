# 0. Librerías 

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
import funciones as f
from utils import Header, get_header, Plotgraph, Barplot, Waterfallplot
from InputsNoRevolvente import InputsNoRevolvente
from InputsNoRevolventeReal import InputsNoRevolventeReal
from InputsNoRevolventeTeorico import InputsNoRevolventeTeorico

# 1. Lectura de Data - Reporte PD, CAN, PRE, MAE

xls_product = pd.ExcelFile('C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\\6. Reporte_Monitoreo\Data\Vehicular.xlsx')

pd_graph_list, can_graph_list, pre_graph_list = [], [], []
pd_alertas_list, can_alertas_list, pre_alertas_list = [], [], []
report_list_pd, report_list_can, report_list_pre  = [], [], []
pd_MAE_graph_list, can_MAE_graph_list, pre_MAE_graph_list = [], [], []
resumen_descalibrados_pd, resumen_descalibrados_can, resumen_descalibrados_pre = '', '', ''
resumen_revision_pd, resumen_revision_can, resumen_revision_pre = '', '', ''
comb_size = []
report_list_MAE_pd, report_list_MAE_can, report_list_MAE_pre = [], [], []
MAE_titles = []

# 2. Setting de Filtros

filtro1, filtro2 = 'c_riesgo', 'c_plazo'
nro_comb_filtro1, nro_comb_filtro2, nro_comb_mixto = 0, 5, 10

cortes =  [[[filtro1], nro_comb_filtro1], [[filtro2], nro_comb_filtro2], [[filtro1, filtro2], nro_comb_mixto]]

# 3. Generación de Objetos

MAE_list = [['MAE_pd', pd_MAE_graph_list], ['MAE_can', can_MAE_graph_list], ['MAE_pre', pre_MAE_graph_list]]

for corte in cortes:
    productR = InputsNoRevolventeReal(xls_product)
    productR.condensar(corte[0])
    productT = InputsNoRevolventeTeorico(xls_product)
    productT.condensar(corte[0])
    product = InputsNoRevolvente(productR,productT)
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

        graph2 = Plotgraph(product.curvas, curvas='Can', nombre='Cancelaciones', corte=combinacion)
        can_graph_list.append(graph2)

        graph3 = Plotgraph(product.curvas, curvas='Pre', nombre='Prepagos', corte=combinacion)
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

# 4. Dash

import dash
from dash.dependencies import Input, Output
from pages import overview

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('data').resolve()
ASSETS_PATH = PATH.joinpath('assets').resolve()

# 5. Layout

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