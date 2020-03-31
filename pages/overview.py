import dash_html_components as html


from utils_Monitoreo import Header, Plotgraph

import pandas as pd
import pathlib


def create_layout(app, report_list):
    rows = []
    for ii in range(len(report_list)): # numero de filas
        elems = []
        for jj in range(len(report_list[ii])):
            if report_list[ii][jj][2]=="product":
                aux = html.H5(report_list[ii][jj][0])
            else:
                aux = html.H6(report_list[ii][jj][0],className="subtitle padded")
            elems.append(
                html.Div(
                    [
                        aux
                        ,
                        report_list[ii][jj][1],
                    ],
                    className=report_list[ii][jj][2],
                )
            )
        rows.append( html.Div(
                        elems,
                        className="row",
                            )
                    )
    return html.Div(
            [
                html.Div([Header(app)]),
                # page 
                html.Div(   rows   ,
                            className="sub_page", ),
            ],
            className="page",
                        )
            

    # for range(report_list):

    # r0_e0 = report_list[0][0]

    # r1_e0 = report_list[1][0]
    # r1_e1 = report_list[1][1]
    
    # r2_e0 = report_list[2][0]
    
    # r3_e0 = report_list[3][0]
    # r3_e1 = report_list[3][1]

    # # Page layouts
    # # Row 3
    # row3 = html.Div(
    #                     [
    #                         html.Div(
    #                             [
    #                                 html.H5(r0_e0[0]),
    #                                 r0_e0[1],
    #                             ],
    #                             className="product",
    #                         )
    #                     ],
    #                     className="row",
    #                 )
    
    # # Row 4
    # row4 = html.Div(
    #                     [
    #                         html.Div(
    #                             [
    #                                 html.H6( r1_e0[0], className="subtitle padded"),
    #                                 r1_e0[1],
    #                             ],
    #                             className="six columns",
    #                         ),
    #                         html.Div(
    #                             [
    #                                 html.H6(r1_e1[0],  className="subtitle padded",),
    #                                 r1_e1[1],
    #                             ],
    #                             className="six columns",
    #                         ),
    #                     ],
    #                     className="row",
    #                     # style={"margin-bottom": "35px"},
    #                 )

    # # Row 5
    # row5 = html.Div(
    #                     [
    #                         html.Div(
    #                             [   html.H6(r2_e0[0], className="subtitle padded",),
    #                                 r2_e0[1],
    #                             ],
    #                             className="twelve columns",
    #                         ),
    #                     ],
    #                     className="row ",
    #                 )
    # row6 = html.Div(
    #                     [
    #                         html.Div(
    #                             [   html.H6( r3_e0[0], className="subtitle padded",),
    #                                 r3_e0[1],
    #                             ],
    #                             className="six columns",
    #                         ),
    #                         html.Div(
    #                             [   html.H6(  r3_e0[0], className="subtitle padded",),
    #                                 r3_e0[1],
    #                             ],
    #                             className="six columns",
    #                         ),
    #                     ],
    #                     className="row ",
    #                 )

    # return html.Div(
    #     [
    #         html.Div([Header(app)]),
    #         # page 1
    #         html.Div(   [ row3, row4, row5, row6],
    #                     className="sub_page", ),
    #     ],
    #     className="page",
    # )
