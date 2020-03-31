# 0. Librerías *********************************************************

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash 

# 1. Funciones de Apoyo

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

def Plotgraph(df, curvas='PD', corte=0): # Gráfico de líneas --> 'PD', 'Cancelaciones', 'Prepago'

    # Texto en el gráfico
    columns_aux = ['pd_real','pd_teorica','pd_optima','can_real','can_teorica','can_optima','pre_real','pre_teorica','pre_optima']
    for column in columns_aux:

        plazo = len(df[column][corte]) - 1
        value = 0

        texto_aux = ['', '', '', '', '', value, '', '', '', '', '', value , '', '', '', '', '', value, '', '', '', '', '', value,
                    '', '', '', '', '', value, '', '', '', '', '', value, '', '', '', '', '', value, '', '', '', '', '', value,
                    '', '', '', '', '', value, '', '', '', '', '', value, '', '', '', '', '', value, '', '', '', '', '', value]

        texto = texto_aux[:plazo]

        range_texto_aux = []
        for t in range(1,plazo):
            if t%6==0:
                range_texto_aux.append(t)
        
        for obs in range_texto_aux:
            texto[obs-1] = round(df[column][corte][obs],3)
                
        if column=='pd_real':
            texto_pd_real = texto
        elif column=='pd_teorica':
            texto_pd_teorica = texto
        elif column=='pd_optima':
            texto_pd_best_fit = texto
        elif column=='can_real':
            texto_can_real = texto
        elif column=='can_teorica':
            texto_can_teorica = texto
        elif column=='can_optima':
            texto_can_best_fit = texto
        elif column=='pre_real':
            texto_pre_real = texto
        elif column=='pre_teorica':
            texto_pre_teorica = texto
        else:
            texto_pre_best_fit = texto

    # Data
    data = list()

    if curvas=='PD':
        # Curva Real
        real = go.Scatter(  
                            x = list(range(len(df['pd_real'][corte]))),
                            y = df['pd_real'][corte],
                            name = 'PD Real',
                            line_color = 'grey',
                            mode = 'lines+markers+text',
                            text = texto_pd_real,
                            textposition = 'bottom center',
                            textfont = dict(size=10, color='black', family='flexo medium')
                        )
        data.append(real)
        # Curva Teórica
        teorica = go.Scatter(
                                x = list(range(len(df['pd_teorica'][corte]))),
                                y = df['pd_teorica'][corte],
                                name = 'PD Teórica',
                                line_color = 'blue',
                                mode = 'lines+markers+text',
                                text = texto_pd_teorica,
                                textposition = 'top center',
                                textfont = dict(size=10, color='black', family='flexo medium')
                            )
        data.append(teorica)
        # Best Fit
        best_fit = go.Scatter(
                                x = list(range(len(df['pd_optima'][corte]))),
                                y = df['pd_optima'][corte],
                                name = 'PD Best Fit',
                                line_color = 'orange',
                                mode = 'lines+markers+text',
                                text = texto_pd_best_fit,
                                textposition = 'top center',
                                textfont = dict(size=10, color='black', family='flexo medium')
                            )
        data.append(best_fit)

    elif curvas=='Cancelaciones':
        # Curva Real
        real = go.Scatter(  
                            x = list(range(len(df['can_real'][corte]))),
                            y = df['can_real'][corte],
                            name = 'Cancelaciones Real',
                            line_color = 'grey',
                            mode = 'lines+markers+text',
                            text = texto_can_real,
                            textposition = 'bottom center',
                            textfont = dict(size=10, color='black', family='flexo medium')
                        )
        data.append(real)
        # Curva Teórica
        teorica = go.Scatter(
                                x = list(range(len(df['can_teorica'][corte]))),
                                y = df['can_teorica'][corte],
                                name = 'Cancelaciones Teórica',
                                line_color = 'blue',
                                mode = 'lines+markers+text',
                                text = texto_can_teorica,
                                textposition = 'top center',
                                textfont = dict(size=10, color='black', family='flexo medium')
                            )
        data.append(teorica)
        # Best Fit
        best_fit = go.Scatter(
                                x = list(range(len(df['can_optima'][corte]))),
                                y = df['can_optima'][corte],
                                name = 'Cancelaciones Best Fit',
                                line_color = 'orange',
                                mode = 'lines+markers+text',
                                text = texto_can_best_fit,
                                textposition = 'top center',
                                textfont = dict(size=10, color='black', family='flexo medium')
                            )
        data.append(best_fit)
    
    elif curvas=='Prepago':
        # Curva Real
        real = go.Scatter(  
                            x = list(range(len(df['pre_real'][corte]))),
                            y = df['pre_real'][corte],
                            name = 'Prepago Real',
                            line_color = 'grey',
                            mode = 'lines+markers+text',
                            text = texto_pre_real,
                            textposition = 'bottom center',
                            textfont = dict(size=10, color='black', family='flexo medium')
                        )
        data.append(real)
        # Curva Teórica
        teorica = go.Scatter(
                                x = list(range(len(df['pre_teorica'][corte]))),
                                y = df['pre_teorica'][corte],
                                name = 'Prepago Teórica',
                                line_color = 'blue',
                                mode = 'lines+markers+text',
                                text = texto_pre_teorica,
                                textposition = 'top center',
                                textfont = dict(size=10, color='black', family='flexo medium')
                            )
        data.append(teorica)
        # Best Fit
        best_fit = go.Scatter(
                                x = list(range(len(df['pre_optima'][corte]))),
                                y = df['pre_optima'][corte],
                                name = 'Prepago Fit',
                                line_color = 'orange',
                                mode = 'lines+markers+text',
                                text = texto_pre_best_fit,
                                textposition = 'top center',
                                textfont = dict(size=10, color='black', family='flexo medium')
                            )
        data.append(best_fit)

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
                                                            'title': '%',
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
                                        orientation = 'h'),
                                go.Bar(x=df[curva_optima],
                                        y = df[grupo],
                                        orientation = 'h')]
        })