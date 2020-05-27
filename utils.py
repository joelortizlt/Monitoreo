# Librerias

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas
import matplotlib

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

def paragraph_alertas(df, alert_list, range_nro_hojas, parametro1, parametro2, compilador_descal, compilador_rev,
                        Combinacion=False, ValorFiltro1=''):
    paragraph, descalibrado, revision = '', '', ''
    for alerta in range_nro_hojas: # Análisis gráfico por gráfico
        if alert_list[alerta + parametro1]=='Descalibrado':
            if Combinacion:
                descalibrado = descalibrado + str(ValorFiltro1) + ' - ' + str(df[parametro2].values[alerta]) + ', '
            else:
                descalibrado = descalibrado + str(df[parametro2].values[alerta][0]) + ', '
        elif alert_list[alerta + parametro1]=='Revisión':
            if Combinacion:
                revision = revision + str(ValorFiltro1) + ' - ' + str(df[parametro2].values[alerta]) + ', '
            else:
                revision = revision + str(df[parametro2].values[alerta][0]) + ', '
    if descalibrado=='' and revision=='': # Agregando análisis de Hoja (Corte Específico)
        paragraph = 'Todos los cortes están calibrados.'
    if descalibrado!='':
        paragraph = 'Necesitan calibración: ' + descalibrado[:len(descalibrado)-2] +'. '
        compilador_descal += descalibrado
    if revision!='':
        paragraph = paragraph + 'Necesitan revisión: ' + revision[:len(revision)-2] + '.'
        compilador_rev += revision
    paragraph_html = html.P(paragraph, style={"color": "#ffffff", "fontSize": "40"}) # To HTML
    return paragraph_html, compilador_descal, compilador_rev
    
# Line Graph --> PD, Cancelaciones, Prepagos
def Plotgraph(df, curvas='PD', nombre='PD', corte=0, y_title='%', promedio=False):

    # Text
    text_list = []
    value = 0
    text_aux = ['', '', '', '', '', value, '', '', '', '', '', value , '', '', '', '', '', value, '', '', '', '', '', value,
                    '', '', '', '', '', value, '', '', '', '', '', value, '', '', '', '', '', value, '', '', '', '', '', value,
                    '', '', '', '', '', value, '', '', '', '', '', value, '', '', '', '', '', value, '', '', '', '', '', value]
    
    curve_name = curvas.lower() # Lowercase
    columns_aux = [curve_name + '_real', curve_name + '_teorico', curve_name + '_optimo']
    for column in columns_aux:
        plazo = len(df[column][corte]) - 1
        text = text_aux[:plazo]
        
        range_text_aux = []
        for t in range(1,plazo):
            if t%6==0:
                range_text_aux.append(t)
        for t in range_text_aux:
            text[t-1] = str(round(df[column][corte][t-1], 3)) + '%'
        
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
                                textfont = dict(size=14, color=name[2], family='flexo medium')
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
                                                        height = 260,
                                                        width = 700,
                                                        hovermode = 'closest',
                                                        # legend = {
                                                        #     'x': -0.0277108433735,
                                                        #     'y': -0.142606516291,
                                                        #     'orientation': 'h',
                                                        # },
                                                        margin = {
                                                            'r': 20,
                                                            't': 20,
                                                            'b': 20,
                                                            'l': 50
                                                        },
                                                        legend = dict(
                                                            x = 0,
                                                            y = 1,
                                                            traceorder = "normal",
                                                            font = dict(
                                                                family = "sans-serif",
                                                                size = 14,
                                                                color = "black"
                                                            ),
                                                            bgcolor = "LightSteelBlue",
                                                            bordercolor = "Black",
                                                            borderwidth = 2
                                                        ),
                                                        showlegend = True,
                                                        xaxis = {
                                                            'autorange': True,
                                                            'linecolor': 'rgb(0, 0, 0)',
                                                            'linewidth': 1,
                                                            'showgrid': False,
                                                            'showline': True,
                                                            'type': 'linear',
                                                            'title': 'Plazo (Meses)'
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
    
def Barplot(df, curva='MAE_pd', grupo='c_riesgo', inicio=0, step=3):

    curva_optima = curva[:3] + 'op' + curva[3:]
    
    if grupo=='Todos':
        ejey = ['PD', 'Cancelaciones', 'Prepagos']
        ejex = [df['MAE_pd'][0], df['MAE_can'][0], df['MAE_pre'][0]]
        ejexop = [df['MAEop_pd'][0], df['MAEop_can'][0], df['MAEop_pre'][0]]
        text_normal = [round(num, 4) for num in ejex]
        text_op = [round(num, 4) for num in ejexop]
    else:
        ejey = list(df[grupo].values)
        ejex = list(df[curva][inicio:step].values)
        ejexop = list(df[curva_optima][inicio:step].values)
        text_normal = [round(num, 4) for num in ejex]
        text_op = [round(num, 4) for num in ejexop]

    aux=0
    for elem in text_normal:
        text_normal[aux] = str(text_normal[aux]) + '%'
        text_op[aux] = str(text_op[aux]) + '%'
        aux = aux +1

    return dcc.Graph(
                figure={'data': [go.Bar(x = ejex, 
                                        y = ejey,
                                        orientation = 'h',
                                        name = curva[:3],
                                        text = text_normal,
                                        textposition = 'inside'),
                                go.Bar(x = ejexop,
                                        y = ejey,
                                        orientation = 'h',
                                        name = 'MAE Óptimo',
                                        text = text_op,
                                        textposition = 'inside',
                                        textfont_size = 14)],
                        'layout': go.Layout(yaxis = {'type': 'category'},
                                            height = 350,
                                            font = {'family': 'flexo medium'},
                                            margin=dict(
                                                            autoexpand=True,
                                                            l=100,
                                                            r=20,
                                                            t=20,
                                                        ))
        })

def Waterfallplot(df, combinacion=0, archivo='Inputs', mixto=False, promedio=False):

    if archivo=='Inputs':
        Curva1 = 'PD'
        Curva2 = 'Canc.'
        Curva3 = 'Prep.'
    else:
        Curva1 = 'Ing. Fin.',
        Curva2 = 'Egr. Fin.',
        Curva3 = 'Saldos'

    inicio = 3 if mixto else 2
    
    if promedio:
        inicio = 0
        height_number = 520
        text =  [str(round(df['Valor'].values[inicio],4)) + '%',
                str(round(df['Valor'].values[inicio+1],4)) + '%',
                str(round(df['Valor'].values[inicio+2],4)) + '%', 
                str(round(df['Valor'].values[inicio+3],4)) + '%', 
                str(round(df['Valor'].values[inicio+4],4)) + '%']
        y = [df['Valor'].values[inicio], df['Valor'].values[inicio+1], df['Valor'].values[inicio+2],
            df['Valor'].values[inicio+3], df['Valor'].values[inicio+4] ]
        limit = max(round(df['Valor'].values[inicio],4), round(df['Valor'].values[inicio+4],4)) + 0.03
    else:
        height_number = 260
        text =  [str(round(df.iloc[combinacion].values[inicio],4)) + '%',
                str(round(df.iloc[combinacion].values[inicio+1],4)) + '%',
                str(round(df.iloc[combinacion].values[inicio+2],4)) + '%', 
                str(round(df.iloc[combinacion].values[inicio+3],4)) + '%', 
                str(round(df.iloc[combinacion].values[inicio+4],4)) + '%']
        y =  [df.iloc[combinacion].values[inicio], df.iloc[combinacion].values[inicio+1], df.iloc[combinacion].values[inicio+2],
            df.iloc[combinacion].values[inicio+3], df.iloc[combinacion].values[inicio+4] ]
        limit = max(round(df.iloc[combinacion].values[inicio],4), round(df.iloc[combinacion].values[inicio+4],4)) + 0.03

    return dcc.Graph(
                figure={'data': [go.Waterfall(name = 'Variation',
                                    orientation = 'v',
                                    measure = ['absolute', 'relative', 'relative', 'relative', 'total'],
                                    x = ['T min Inicial', 'Δ ' + Curva1, 'Δ ' + Curva2, 'Δ ' + Curva3, 'T min Final'],
                                    textposition = 'outside',
                                    textfont_size = 14,
                                    text = text,
                                    y = y,
                                    connector = {'line': {'color': 'rgb(63, 63, 63)'}},
                                    decreasing = {"marker":{"color":"Maroon", "line":{"color":"red", "width":2}}},
                                    increasing = {"marker":{"color":"Teal"}},
                                    totals = {"marker":{"color":"deep sky blue", "line":{"color":'blue', "width":3}}}
                                )],
                        'layout': go.Layout(showlegend = True,
                                            height = height_number,
                                            yaxis = {'range': [0.015, limit], 'title': '%'},
                                            font = {'family': 'flexo medium'},
                                            margin=dict(
                                                            autoexpand=True,
                                                            l=100,
                                                            r=20,
                                                            t=20,
                                                        )
                                            )
                }
        )

def FanChart(df, nombre='PD', corte=0, dot_name='Real', line_name='Teórica', colorListRGB= [ [0,99,174], [153,212,255], [200,222,255] ]):

    columns = df.columns
    start_position = df.columns.get_loc('recuento')
    x = list(range(len(df[columns[start_position + 1]][corte])))
    yreal = df[columns[start_position + 1]][corte]
    ypred = df[columns[start_position + 2]][corte]
    yIntervLimits = list()
    intervNames = list()

    for ii in range(start_position + 3, len(columns), 2):
        yIntervLimits.append(df[columns[ii]][corte])
        yIntervLimits.append( [x1 - x2 for (x1, x2) in zip(df[columns[ii+1]][corte], df[columns[ii]][corte])] )
        intervNames.append(columns[ii])

    data = list()
    # Otros intervalos
    nn = 0
    for ii in range(0,len(yIntervLimits),2):
    # Nivel base
        data_aux = go.Scatter(
                x=x,
                y=  yIntervLimits[ii],
                hoverinfo='x+y',
                mode='lines',
                name='',
                fillcolor='rgba(255,255,255,0.0)',
                opacity=0.0,
                showlegend=False,
                line=dict(width=0.0, color='rgba(255, 255, 255, 0.0)'),
                stackgroup='level'+str(ii)
        )
    
        data.append(data_aux)
    # Nivel sombra
        color = 'rgb({d[0]}, {d[1]}, {d[2]})'.format(d=colorListRGB[nn])
        # ii+=1
        data_aux2 = go.Scatter(
                x=x,
                y= yIntervLimits[ii+1] ,
                hoverinfo='x+y',
                mode='lines',
                name=intervNames[nn],
                opacity=1,  
                line=dict(width=0.5, color=color),
                stackgroup='level'+str(ii)
        )
        nn+=1
        data.append(data_aux2)

    # puntos
    data_aux3 = go.Scatter(
            x=x,y=  yreal,
            mode='markers',
            name=dot_name,
            opacity=1,
            line=dict(width=.1, color='rgb(200, 10, 10)'),
            # stackgroup='one'
    )
    data.append(data_aux3)
    
    # line of y point estimation
    data_aux4 = go.Scatter(
            x=x,y=  ypred,
            mode='lines',
            name=line_name,
            opacity=0.7,
            line=dict(width=3, color='rgb(10, 10, 10)'),
            # stackgroup='one'
    )
    data.append(data_aux4)
    
    return dcc.Graph( figure={
                        'data': data,
                        'layout': go.Layout( 
                            xaxis_title='Plazo',
                            yaxis_title=nombre,
                            xaxis=dict(
                                showline=True,
                                showgrid=False,
                                showticklabels=True,
                                linecolor='rgb(204, 204, 204)',
                                linewidth=2,
                                ticks='outside',
                                tickfont=dict(
                                    family='Arial',
                                    size=12,
                                    color='rgb(82, 82, 82)',
                                ),
                            ),
                            yaxis=dict(
                                showgrid=False,
                                zeroline=False,
                                showline=True,
                                showticklabels=True,
                                linecolor='rgb(204, 204, 204)',
                                linewidth=2,
                                ticks='outside',
                                tickfont=dict(
                                    family='Arial',
                                    size=12,
                                    color='rgb(82, 82, 82)',
                                ),    
                            ),
                            height = 260,
                            width = 700,
                            autosize = False,
                            margin=dict(
                                autoexpand=True,
                                l=100,
                                r=20,
                                t=20,
                            ),
                            showlegend=True,
                            plot_bgcolor='white',
                            font = {'family': 'flexo medium', 'size': 12})
                    }                   
            )       