# 0. Librerias ***********************************************

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

# 1. Funciones de Apoyo ***************************************

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
    columns_aux = ['if_real','if_teorico','if_optimo','ef_real','ef_teorico','ef_optimo','saldo_real','saldo_teorico','saldo_optimo']
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
                
        if column=='if_real':
            texto_pd_real = texto
        elif column=='if_teorico':
            texto_pd_teorica = texto
        elif column=='if_optimo':
            texto_pd_best_fit = texto
        elif column=='ef_real':
            texto_can_real = texto
        elif column=='ef_teorico':
            texto_can_teorica = texto
        elif column=='ef_optimo':
            texto_can_best_fit = texto
        elif column=='if_real':
            texto_pre_real = texto
        elif column=='if_teorico':
            texto_pre_teorica = texto
        else:
            texto_pre_best_fit = texto

    # Data
    data = list()

    if curvas=='PD':
        # Curva Real
        real = go.Scatter(  
                            x = list(range(len(df['if_real'][corte]))),
                            y = df['if_real'][corte],
                            name = 'IF Real',
                            line_color = 'grey',
                            mode = 'lines+markers+text',
                            text = texto_pd_real,
                            textposition = 'bottom center',
                            textfont = dict(size=10, color='black', family='flexo medium')
                        )
        data.append(real)
        # Curva Teórica
        teorica = go.Scatter(
                                x = list(range(len(df['if_teorico'][corte]))),
                                y = df['if_teorico'][corte],
                                name = 'IF Teórico',
                                line_color = 'blue',
                                mode = 'lines+markers+text',
                                text = texto_pd_teorica,
                                textposition = 'top center',
                                textfont = dict(size=10, color='black', family='flexo medium')
                            )
        data.append(teorica)
        # Best Fit
        best_fit = go.Scatter(
                                x = list(range(len(df['if_optimo'][corte]))),
                                y = df['if_optimo'][corte],
                                name = 'IF Best Fit',
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
                            x = list(range(len(df['ef_real'][corte]))),
                            y = df['ef_real'][corte],
                            name = 'EF Real',
                            line_color = 'grey',
                            mode = 'lines+markers+text',
                            text = texto_can_real,
                            textposition = 'bottom center',
                            textfont = dict(size=10, color='black', family='flexo medium')
                        )
        data.append(real)
        # Curva Teórica
        teorica = go.Scatter(
                                x = list(range(len(df['ef_teorico'][corte]))),
                                y = df['ef_teorico'][corte],
                                name = 'EF Teórico',
                                line_color = 'blue',
                                mode = 'lines+markers+text',
                                text = texto_can_teorica,
                                textposition = 'top center',
                                textfont = dict(size=10, color='black', family='flexo medium')
                            )
        data.append(teorica)
        # Best Fit
        best_fit = go.Scatter(
                                x = list(range(len(df['ef_optimo'][corte]))),
                                y = df['ef_optima'][corte],
                                name = 'EF Best Fit',
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
                            x = list(range(len(df['saldo_real'][corte]))),
                            y = df['saldo_real'][corte],
                            name = 'Saldo Real',
                            line_color = 'grey',
                            mode = 'lines+markers+text',
                            text = texto_pre_real,
                            textposition = 'bottom center',
                            textfont = dict(size=10, color='black', family='flexo medium')
                        )
        data.append(real)
        # Curva Teórica
        teorica = go.Scatter(
                                x = list(range(len(df['saldo_teorico'][corte]))),
                                y = df['saldo_teorico'][corte],
                                name = 'Saldo Teórico',
                                line_color = 'blue',
                                mode = 'lines+markers+text',
                                text = texto_pre_teorica,
                                textposition = 'top center',
                                textfont = dict(size=10, color='black', family='flexo medium')
                            )
        data.append(teorica)
        # Best Fit
        best_fit = go.Scatter(
                                x = list(range(len(df['saldo_optimo'][corte]))),
                                y = df['saldo_optimo'][corte],
                                name = 'Saldo Best Fit',
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
                                                            'title': 'Monto',
                                                            'type': 'linear',
                                                            'zeroline': False,
                                                            'zerolinewidth': 4,
                                                        }
                                    )
                        },
                        config = {"displayModeBar": False}
    ) 


def Barplot(df, curva='MAE_if', grupo='c_riesgo'):

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