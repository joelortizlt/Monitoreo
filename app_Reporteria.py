
# Librerias
import numpy as np
import pandas as pd
import pathlib
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from pages import overview
from Reporte import Reporte

# Para correr:
# --> 1. Indicar [RutaReal, RutaTeorico, RutaTMIN, MinCosecha, MaxCosecha, Filtro1, Filtro2, NombreProducto] // Filtros = 'C_FILTRO'
# --> 2. Nro de Reporte --> display_page (lines 93 y 94)

ReporteStack= [] # Lista donde se añaden los 4 report_list (ProductoSinCortes, Corte1, Corte2, Completo) de los 'n' productos.

lista = [  
            ['D:\Codes\Data\Hipot_Reales.csv', 'D:\Codes\Data\Hipot_Inputs.csv','D:\Codes\Data\Hipot_Precios.csv',
            201701, 201912, 'C_SEGMENTO', 'C_PLAZO', 'HIPOTECARIO'],
        ]  

for elem in lista:
    REAL, TEORICO, TMIN = pd.read_csv(elem[0]), pd.read_csv(elem[1]), pd.read_csv(elem[2])
    fecha = str(elem[4])[4:] + ' - ' + str(elem[4])[:4] 
    reporte = Reporte(Real=REAL, Teorico=TEORICO, Tmin=TMIN, mincosecha=elem[3] , maxcosecha=elem[4] , 
                        filtro1=elem[5], filtro2=elem[6], Producto=elem[7], Fecha=fecha)
    reporte.Stack(ReporteStack)

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

    resultado = list()
    for hoja in range(len(ReporteStack[0][3])): # [Producto][Reporte] --> [Producto, Corte1, Corte2, Completo]
        resultado.append(overview.create_layout(app, ReporteStack[0][3][hoja]))

    # resultado.append(overview.create_layout(app, ReporteStack[0][0])

    return tuple(resultado)

if __name__=='__main__':
    app.run_server(debug=True)