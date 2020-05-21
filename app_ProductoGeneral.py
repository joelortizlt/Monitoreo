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
from utils import Header, get_header, Plotgraph, Barplot, Waterfallplot, FanChart
from InputsNoRevolvente import InputsNoRevolvente
from InputsNoRevolventeReal import InputsNoRevolventeReal
from InputsNoRevolventeTeorico import InputsNoRevolventeTeorico

# 1. Lectura de Data - Reporte PD, CAN, PRE, MAE

# Elección de Producto
REAL = pd.read_csv('C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_Hipotecario\Hipot_Reales.csv')
TEORICO = pd.read_csv('C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_Hipotecario\Hipot_Inputs.csv')
TMIN = pd.read_csv('C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_Hipotecario\Hipot_Precios.csv')
mincosecha, maxcosecha = 201701, 201912
producto = 'Hipotecario'

# for oculto:
    # REAL = pd.read_csv('C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_GAHI\Gahi_Reales.csv')
    # TEORICO = pd.read_csv('C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_GAHI\Gahi_Inputs.csv')
    # TMIN = pd.read_csv('C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_GAHI\Gahi_Precios.csv')
    # mincosecha, maxcosecha = 201701, 201912
    # producto = 'GAHI'
    # REAL = pd.read_csv('C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_CEF\CEFCB_Reales.csv')
    # TEORICO  = pd.read_csv('C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_CEF\CEFCB_Inputs.csv')
    # TMIN = pd.read_csv('C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_CEF\CEFCB_Precios.csv')
    # mincosecha, maxcosecha = 201701, 201912
    # producto = 'Crédito Efectivo'
    # REAL = pd.read_csv('C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_Vehicular\Vehicular_Reales.csv')
    # TEORICO = pd.read_csv('C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_Vehicular\Vehicular_Inputs.csv')
    # TMIN = pd.read_csv('C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_Vehicular\Vehicular_Precios.csv')
    # mincosecha, maxcosecha = 201701, 201912
    # producto = 'Vehicular'
    # REAL = pd.read_csv('C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_PymeNR\PymeNR_Reales.csv')
    # TEORICO = pd.read_csv('C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_PymeNR\PymeNR_Inputs.csv')
    # TMIN = pd.read_csv('C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_PymeNR\PymeNR_Precios.csv')
    # mincosecha, maxcosecha = 201701, 201912
    # producto = 'Pyme Reactivo'
    # REAL = pd.read_csv('C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_MiVivienda\Mivivienda_Reales.csv')
    # TEORICO = pd.read_csv('C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_MiVivienda\Mivivienda_Inputs.csv')
    # TMIN = pd.read_csv('C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_MiVivienda\Mivivienda_Precios.csv')
    # mincosecha, maxcosecha = 201701, 201912
    # producto = 'Mi Vivienda'

# Generación del Reporte General por Producto
pd_MAE, can_MAE, pre_MAE = [], [], []

product = InputsNoRevolvente(REAL, TEORICO, mincosecha=mincosecha, maxcosecha=maxcosecha, completar=True)
product.condensar()
product.optimizar()
product.impactoTmin(TMIN)

# Gráficos
graph = Plotgraph(product.curvas, promedio=True)
graph2 = Plotgraph(product.curvas, curvas='Can', nombre='Cancelaciones', promedio=True)
graph3 = Plotgraph(product.curvas, curvas='Pre', nombre='Prepagos', promedio=True)
fanchart, fanchart2 = FanChart(df=product.ci_pd), FanChart(df=product.ci_can, nombre='Cancelaciones')
fanchart3 = FanChart(df=product.ci_pre, nombre='Prepagos')
MAE_list = [['MAE_pd', pd_MAE], ['MAE_can', can_MAE], ['MAE_pre', pre_MAE]]
barplot = Barplot(product.stats, grupo='Todos')    
waterfall = Waterfallplot(df=product.TminProm, promedio=True)

aux = html.P('') # 
start_date, end_date = str(mincosecha)[4:] + '-' + str(mincosecha)[:4], str(maxcosecha)[4:] + '-' + str(maxcosecha)[:4] # Fechas de Evaluación
report_list_resumen = [ [('Producto ' + producto + ' del ' + start_date + ' al ' + end_date, aux, 'product')],
                        [('Impacto en tasas', waterfall, 'six columns'), ('Curva de PD', fanchart, 'six columns'), ('Curva de Cancelaciones', fanchart2, 'six columns')],
                        [('MAE', barplot, 'six columns'), ('Curva de Prepagos', fanchart3, 'six columns')]
]

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
    )

if __name__=='__main__':
    app.run_server(debug=True)

