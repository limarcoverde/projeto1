from pandas.core.frame import DataFrame
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html


def CreateHeader():
        return html.Div(
                className="header",
                children=[
                        #html.P(children="🔥", className="header-emoji"),
                        html.H1(
                                className="header-title",
                                children="📈Previsão de Vendas", 
                        ),
                        html.P(
                                className="header-description",
                                children="Analise e previsão de vendas de um restaurante localizado no Rio Grande do sul no periodo de 2 anos.",
                        ),
                ],
        )        

     
def CreateSlider(id,title,min,max,value,marks):
        return html.Div(
                children=[
                        html.Div(children=title, className="menu-title"),
                        dcc.RangeSlider(
                                id=id,#'year-slider',
                                min=min,
                                max=max,
                                value=value,
                                marks=marks,
                                step=None
                        )
                ],
        )       

def CreateDropDownMenu(id,title,options,value):     
        return html.Div(
                children=[
                        html.Div(children=title, className="menu-title"),
                        dcc.Dropdown(
                                id=id,#"period-filter",
                                options=options,#[{"label": period, "value": period} for period in ['M','Q','Y']],
                                value=value,#"M",
                                clearable=False,
                                searchable=False,
                                className="dropdown",
                        ),
                ],
        )




def CreateMenu(children,className="menu-body"):
        return html.Div(
                className=className,
                children=children
        )



def CreateGraph(id,title,fig=go.Figure()):
        return html.Div(
                className="wrapper",
                children=[
                        
                        html.Div(
                                className="card",
                                children=[
                                        html.Div(children=title, className="menu-card"),
                                        dcc.Graph(
                                        id=id,
                                        config={"displayModeBar": False},
                                        figure=fig
                                        )
                                ]
                        )
                ]
        )




