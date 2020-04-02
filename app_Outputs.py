# 0. Librerias *****************************************************************************

import numpy as np
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error

#   Dash
import pathlib
import dash_core_components as dcc
import dash_html_components as html

# Otros Scripts
from utils_Outputs import Header, get_header, Plotgraph, Barplot
import funciones as f
from OutputsNoRevolvente import OutputsNoRevolvente
from OutputsNoRevolventeReal import OutputsNoRevolventeReal
from OutputsNoRevolventeTeorico import OutputsNoRevolventeTeorico

# 1. Lectura de Data - Reporte IF, EF, SALDO, MAE

csv_REAL_VEH = '\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\\7. Reporte_Outputs\Data\IFEFSAL_REALES.csv'
csv_IF_VEH = '\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\\7. Reporte_Outputs\Data\IF_TEORICO.csv'
csv_EF_VEH = '\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\\7. Reporte_Outputs\Data\EF_TEORICO.csv'
csv_SALDO_VEH = '\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\\7. Reporte_Outputs\Data\SALDO_TEORICO.csv'

if_graph_list, ef_graph_list, saldo_graph_list = [], [], []
if_alertas_list, ef_alertas_list, saldo_alertas_list = [], [], []
report_list_if, report_list_ef, report_list_saldo  = [], [], []
if_MAE_graph_list, ef_MAE_graph_list, saldo_MAE_graph_list = [], [], []
resumen_descalibrados_if, resumen_descalibrados_ef, resumen_descalibrados_saldo = '', '', ''
resumen_revision_if, resumen_revision_ef, resumen_revision_saldo = '', '', ''
comb_size = []
report_list_MAE_if, report_list_MAE_ef, report_list_MAE_saldo = [], [], []
MAE_titles = []

# 2. Setting de Filtros

filtro1 = 'c_riesgo'
filtro2 = 'c_plazo'
nro_comb_filtro1, nro_comb_filtro2, nro_comb_mixto = 0, 5, 10

cortes =  [[[filtro1], nro_comb_filtro1], [[filtro2], nro_comb_filtro2], [[filtro1, filtro2], nro_comb_mixto]]

# 3. Generación de Objetos

MAE_list = [['MAE_if', if_MAE_graph_list], ['MAE_ef', ef_MAE_graph_list], ['MAE_saldo', saldo_MAE_graph_list]]

for corte in cortes:
    productR = OutputsNoRevolventeReal(csv_REAL_VEH)
    productR.condensar(corte[0])
    productT = OutputsNoRevolventeTeorico(csvif = csv_IF_VEH, csvef = csv_EF_VEH, csvsaldo = csv_SALDO_VEH)
    productT.condensar(corte[0])
    product = OutputsNoRevolvente(productR,productT)
    product.optimizar(0.001)
    product.curvas

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
        if_graph_list.append(graph)

        graph2 = Plotgraph(product.curvas, curvas='EF', corte=combinacion)
        ef_graph_list.append(graph2)

        graph3 = Plotgraph(product.curvas, curvas='Saldo', corte=combinacion)
        saldo_graph_list.append(graph3)

        # Listado de  alertas:
        for mae in MAE_list:

            if product.stats[mae[0]][combinacion] > 3:
                aux_lista = 'Descalibrado'
            elif product.stats[mae[0]][combinacion] >= 2.5 and product.stats[mae[0]][combinacion] < 3:
                aux_lista = 'Revisión'
            else:
                aux_lista = 'Calibrado'
                
            if mae[0]=='MAE_if':
                if_alertas_list.append(aux_lista)
            elif mae[0]=='MAE_ef':
                ef_alertas_list.append(aux_lista)
            elif mae[0]=='MAE_saldo':
                saldo_alertas_list.append(aux_lista)

    title_list = [[if_alertas_list, 'Ingreso Financiero', if_graph_list, report_list_if, if_MAE_graph_list, 'MAE_if'], 
                    [ef_alertas_list, 'Egreso Financiero', ef_graph_list, report_list_ef, ef_MAE_graph_list, 'MAE_ef'],
                    [saldo_alertas_list, 'Saldos', saldo_graph_list, report_list_saldo, saldo_MAE_graph_list, 'MAE_saldo'] 
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

        if title[1]=='Ingreso Financiero':
            resumen_descalibrados_if = resumen_descalibrados_if + aux_descal
            resumen_revision_if = resumen_revision_if + aux_revision
        elif title[1]=='Egreso Financiero':
            resumen_descalibrados_ef = resumen_descalibrados_ef + aux_descal
            resumen_revision_ef = resumen_revision_ef + aux_revision
        else:
            resumen_descalibrados_saldo = resumen_revision_saldo + aux_descal
            resumen_revision_saldo = resumen_revision_saldo + aux_revision

# To html
aux_resumen = [resumen_descalibrados_if, resumen_descalibrados_ef, resumen_descalibrados_saldo, resumen_revision_if, resumen_revision_ef,
                resumen_revision_saldo]
for aux in aux_resumen:
    if aux!='':
        aux = html.P(aux, style={"color": "#ffffff", "fontSize": "40"}, className='row')
    else:
        aux = html.P('Todos los cortes están calibrados', style={"color": "#ffffff", "fontSize": "40"})

aux2 = html.P(' ', style={"color": "#ffffff", "fontSize": "40"}, className='row')

report_list_resumen = [ [('Resumen de Alertas por Riesgo y Plazo', aux2,'product')],
                        [('Curvas de Ingresos Financieros - Descalibrados', resumen_descalibrados_if, 'product')],
                        [('Curvas de Ingresos Financieros - Revisión', resumen_revision_if, 'product')],
                        [('Curvas de Egresos Financieros - Descalibrados', resumen_descalibrados_ef, 'product')],
                        [('Curvas de Egresos Financieros - Revisión', resumen_revision_ef, 'product')],
                        [('Curvas de Saldos - Descalibrados', resumen_descalibrados_saldo, 'product')],
                        [('Curvas de Saldos - Revisión', resumen_revision_saldo, 'product')]
]

report_list_MAE = [[report_list_MAE_if, 'Ingresos Financieros', if_MAE_graph_list], [report_list_MAE_ef, 'Egresos Financieros', ef_MAE_graph_list], 
                    [report_list_MAE_saldo, 'Saldos', saldo_MAE_graph_list]]

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
        overview.create_layout(app, report_list_if[0]),
        overview.create_layout(app, report_list_ef[0]),
        overview.create_layout(app, report_list_saldo[0]),
        overview.create_layout(app, report_list_if[1]),
        overview.create_layout(app, report_list_ef[1]),
        overview.create_layout(app, report_list_saldo[1]),
        overview.create_layout(app, report_list_if[2]),
        overview.create_layout(app, report_list_ef[2]),
        overview.create_layout(app, report_list_saldo[2]),
        overview.create_layout(app, report_list_if[3]),
        overview.create_layout(app, report_list_ef[3]),
        overview.create_layout(app, report_list_saldo[3]),
        overview.create_layout(app, report_list_if[4]),
        overview.create_layout(app, report_list_ef[4]),
        overview.create_layout(app, report_list_saldo[4]),
        overview.create_layout(app, report_list_if[5]),
        overview.create_layout(app, report_list_ef[5]),
        overview.create_layout(app, report_list_saldo[5]),
        overview.create_layout(app, report_list_if[6]),
        overview.create_layout(app, report_list_ef[6]),
        overview.create_layout(app, report_list_saldo[6]),
        overview.create_layout(app, report_list_MAE_if[0]),
        overview.create_layout(app, report_list_MAE_ef[0]),
        overview.create_layout(app, report_list_MAE_saldo[0]),
    )

if __name__=='__main__':
    app.run_server(debug=True)

