# Librerias

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

# Funciones de Apoyo - Reporting

def get_header(app):
    header = html.Div(
                [
                    html.Img(
                        src=app.get_asset_url("bcplogo.png"),
                        className="logo",
                    ),
                    # html.A(
                    #     html.Button("Learn More", id="learn-more-button"),
                    #     href="https://plot.ly/dash/pricing/",
                    # ),
                ],
                className="row",
            )
    return header

def Header(app):
    return html.Div([get_header(app), html.Br([])])

def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "Resumen",
                href="/dash-financial-report/overview",
                className="tab first",
            ),
            dcc.Link(
                "Monitoreo de inputs",
                href="/dash-financial-report/price-performance",
                className="tab",
            ),
            dcc.Link(
                "Monitoreo de outputs",
                href="/dash-financial-report/portfolio-management",
                className="tab",
            ),
            dcc.Link(
                "Acapite 0", href="/dash-financial-report/fees", className="tab"
            ),
            dcc.Link(
                "Acapite 1",
                href="/dash-financial-report/distributions",
                className="tab",
            ),
            dcc.Link(
                "Acapite 2",
                href="/dash-financial-report/news-and-reviews",
                className="tab",
            ),
        ],
        className="row all-tabs",
    )
    return menu

# Line Graph --> PD, Cancelaciones, Prepagos
def Plotgraph(df, curvas='PD', nombre='PD', corte=0, y_title='%'):

    # Text
    text_list = []
    value = 0
    text_aux = ['', '', '', '', '', value, '', '', '', '', '', value , '', '', '', '', '', value, '', '', '', '', '', value,
                    '', '', '', '', '', value, '', '', '', '', '', value, '', '', '', '', '', value, '', '', '', '', '', value,
                    '', '', '', '', '', value, '', '', '', '', '', value, '', '', '', '', '', value, '', '', '', '', '', value]
    
    curve_name = curvas.lower() # Lowercase
    columns_aux = [curve_name + '_real', curve_name + '_teorica', curve_name + '_optima']
    for column in columns_aux:
        plazo = len(df[column][corte]) - 1
        text = text_aux[:plazo]
        
        range_text_aux = []
        for t in range(1,plazo):
            if t%6==0:
                range_text_aux.append(t)
        for t in range_text_aux:
            text[t-1] = round(df[column][corte][t], 3)
        
        text_list.append(text)

    # Data
    data = list()
    data_settings_aux = [ [0, nombre + ' Real', 'grey', 'top center'], [1, nombre + ' Teórica', 'blue', 'top center'], 
                            [2, nombre + ' Óptima', 'orange', 'bottom center'] ]
    
    for name in data_settings_aux:
        curve_aux = go.Scatter( 
                                x = list(range(len(df[columns_aux[name[0]]][corte]))),
                                y = df[columns_aux[name[0]]][corte],
                                name = name[1],
                                line_color = name[2],
                                mode = 'lines+markers+text',
                                text = text_list[name[0]],
                                textposition = name[3],
                                textfont = dict(size=10, color='black', family='flexo medium')
        )
        data.append(curve_aux)
    
    return dcc.Graph(
                        figure = {
                                    'data': data,
                                    'layout': go.Layout(
                                                        autosize = True,
                                                        title = '',
                                                        font = {
                                                            'family': 'flexo medium', 
                                                            'size': 10
                                                        },
                                                        height = 180,
                                                        width = 700,
                                                        hovermode = 'closest',
                                                        legend = {
                                                            'x': -0.0277108433735,
                                                            'y': -0.142606516291,
                                                            'orientation': 'h',
                                                        },
                                                        margin = {
                                                            'r': 20,
                                                            't': 20,
                                                            'b': 20,
                                                            'l': 50
                                                        },
                                                        showlegend = True,
                                                        xaxis = {
                                                            'autorange': True,
                                                            'linecolor': 'rgb(0, 0, 0)',
                                                            'linewidth': 1,
                                                            'showgrid': False,
                                                            'showline': True,
                                                            'type': 'linear',
                                                        },
                                                        yaxis = {
                                                            'autorange': True,
                                                            'gridcolor': 'rgba(127, 127, 127, 0.2)',
                                                            'mirror': False,
                                                            'nticks': 4,
                                                            'showgrid': True,
                                                            'showline': True,
                                                            'ticklen': 10,
                                                            'ticks': 'outside',
                                                            'title': y_title,
                                                            'type': 'linear',
                                                            'zeroline': False,
                                                            'zerolinewidth': 4,
                                                        }
                                    )
                        },
                        config = {"displayModeBar": False}
    ) 
    
def Barplot(df, curva='MAE_pd', grupo='c_riesgo'):

    curva_optima = curva[:3] + 'op' + curva[3:]
    
    return dcc.Graph(
                figure={'data': [go.Bar(x = df[curva], 
                                        y = df[grupo],
                                        orientation = 'h',
                                        name = curva[:3]),
                                go.Bar(x=df[curva_optima],
                                        y = df[grupo],
                                        orientation = 'h',
                                        name = 'MAE Óptimo')],
                        'layout': go.Layout(yaxis={'type': 'category'})
        })       