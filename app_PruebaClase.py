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

ReporteStack= [] # Lista donde se añaden los 4 report_list (Producto, Corte1, Corte2, Completo)

lista = [  ['C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_GAHI\INPUTS_REAL.csv',
            'C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_GAHI\INPUTS_TEORICO.csv',
            'C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_GAHI\TMIN.csv',
            'C_SEGMENTO', 'C_PLAZO']
            ]
            # Se pueden añadir más listas para una segunda iteración del "elem"

for elem in lista:
    REAL, TEORICO, TMIN = pd.read_csv(elem[0]), pd.read_csv(elem[1]), pd.read_csv(elem[2])
    reporte = Reporte(Real=REAL, Teorico=TEORICO, Tmin=TMIN, filtro1=elem[3], filtro2=elem[4], Producto='GAHI', Fecha='XXXX')
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

def display_page(pathname):

    resultado = list()
    for hoja in range(len(ReporteStack[0][2])): # [producto][#Reporte] --> [Producto, Corte1, Corte2, Completo]
        resultado.append(overview.create_layout(app, ReporteStack[0][2][hoja]))

    # resultado.append(overview.create_layout(app, ReporteStack[0][0]))

    return tuple(resultado)

if __name__=='__main__':
    app.run_server(debug=True)