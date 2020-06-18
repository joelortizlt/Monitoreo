import pandas as pd
import numpy as np
import pathlib
import dash
import dash_core_components as dcc
import dash_html_components as html
from utils import Plotgraph, Barplot, Waterfallplot, FanChart, paragraph_alertas
from InputsRevolvente import InputsRevolvente
from InputsRevolventeReal import InputsRevolventeReal
from InputsRevolventeTeorico import InputsRevolventeTeorico
from OutputsNoRevolvente import OutputsNoRevolvente
from OutputsNoRevolventeReal import OutputsNoRevolventeReal
from OutputsNoRevolventeTeorico import OutputsNoRevolventeTeorico
import numpy as np
import pandas as pd
import pathlib
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from pages import overview
from Reporte import Reporte

pd_graph_list, can_graph_list, pre_graph_list, comb_size, = [], [], [], []
pd_MAE_graph_list, can_MAE_graph_list, pre_MAE_graph_list, tmin_graph_list, tir_graph_list = [], [], [], [], []
pd_fanChart, can_fanChart, pre_fanChart = [], [], []
report_list_pd, report_list_can, report_list_pre, report_list_tmin, report_list_tir  = [], [], [], [], []
report_list_MAE_pd, report_list_MAE_can, report_list_MAE_pre, MAE_titles = [], [], [], []
report_list_PDFAN, report_list_CANFAN, report_list_PREFAN = [], [], []
resumen_descalibrados_pd, resumen_descalibrados_can, resumen_descalibrados_pre = '', '', ''
resumen_revision_pd, resumen_revision_can, resumen_revision_pre = '', '', ''
pd_alertas_list, can_alertas_list, pre_alertas_list = [], [], []

Real = pd.read_csv('C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_TSN\TSN_Reales.csv')
Teorico = pd.read_csv('C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_TSN\TSN_Inputs.csv')
Tmin = pd.read_csv('C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_TSN\TSN_Precios.csv')

product = InputsRevolvente(Real, Teorico, completar=True)
cortes =  'C_LINEA'
pd_fanChart, can_fanChart, pre_fanChart = [], [], []
report_list_PDFAN, report_list_CANFAN, report_list_PREFAN = [], [], []
product.condensar([cortes])
product.optimizar()
product.impactoTmin(Tmin, impactoTIR=False)
product.impactoTmin(Tmin, impactoTIR=True)
html_vacio = html.P('')

nro_combinaciones = len(product.curvas.index)
for combinacion in list(range(nro_combinaciones)):
    can_fanChart.append(FanChart(product.ci_can, nombre='Cancelaciones', corte=combinacion))
    pre_fanChart.append(FanChart(product.ci_saldo, nombre='Saldos', corte=combinacion))

str1 = str(cortes)[2:].capitalize()
report_list = []
report_list.append([('Cancelaciones por ' + str1 + ' - Intervalos de Confianza', html_vacio, 'product')])
for linea in range(len(product.curvas.index)):  
    report_list.append([(str1 + ' por ' + product.ci_can['C_LINEA'][linea], can_fanChart[linea], 'twelve columns')])

report_list2 = []
report_list2.append([('Saldos por ' + str1 + ' - Intervalos de Confianza', html_vacio, 'product')])
for linea in range(len(product.curvas.index)):  
    report_list2.append([(str1 + ' por ' + product.ci_saldo['C_LINEA'][linea], pre_fanChart[linea], 'twelve columns')])

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

# Cambiar para visualizar [0] [1] [2] [3]
def display_page(pathname):
    return(
        overview.create_layout(app, report_list),
        overview.create_layout(app, report_list2) )

if __name__=='__main__':
    app.run_server(debug=True)
