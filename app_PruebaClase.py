# %%
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

lista = [  
        #    ['C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_Hipotecario\Hipot_Reales.csv',
        #     'C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_Hipotecario\Hipot_Inputs.csv',
        #     'C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_Hipotecario\Hipot_Precios.csv',
        #     201701, 201712, 'C_SEGMENTO', 'C_MALAVENTA', 'Hipotecario'],
           ['C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_GAHI\Gahi_Reales.csv',
            'C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_GAHI\Gahi_Inputs.csv',
            'C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_GAHI\Gahi_Precios.csv',
            201701, 201912, 'C_SEGMENTO', 'C_PLAZO', 'GAHI'],
        #    ['C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_CEF\CEFCB_Reales.csv',
        #     'C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_CEF\CEFCB_Inputs.csv',
        #     'C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_CEF\CEFCB_Precios.csv',
        #     201701, 201712, 'C_SEGMENTO', 'C_MALAVENTA', 'Crédito Efectivo'],
          ['C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_Vehicular\Vehicular_Reales.csv',
            'C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_Vehicular\Vehicular_Inputs.csv',
            'C:\\Users\\usuario\Desktop\Pricing_BCP\Proyectos\Data_Vehicular\Vehicular_Precios.csv',
            201701, 201912, 'C_SEGMENTO', 'C_MALAVENTA', 'Vehicular']
            ]
            # Se pueden añadir más listas para una segunda iteración del "elem"

for elem in lista:
    REAL, TEORICO, TMIN = pd.read_csv(elem[0]), pd.read_csv(elem[1]), pd.read_csv(elem[2])
    reporte = Reporte(Real=REAL, Teorico=TEORICO, Tmin=TMIN, MinCosecha=elem[3] , MaxCosecha=elem[4] , 
                        filtro1=elem[5], filtro2=elem[6], Producto=elem[7], Fecha='XXX')
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
    for hoja in range(len(ReporteStack[1][3])): # [producto][#Reporte] --> [Producto, Corte1, Corte2, Completo]
        resultado.append(overview.create_layout(app, ReporteStack[1][3][hoja])) # [0][0][hoja] necesita revisión --> corre en otro script

    # resultado.append(overview.create_layout(app, ReporteStack[0][0]))

    return tuple(resultado)

if __name__=='__main__':
    app.run_server(debug=True)