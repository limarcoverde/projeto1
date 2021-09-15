import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

import pandas as pd
import numpy as np

pio.templates.default = "plotly_white"

df = pd.read_csv('sales_with_extra_features.csv')
df['DATA'] = pd.to_datetime(df['DATA'])

DF_MES = df.loc[df.DATA.dt.to_period('Y')=='2019'].VENDAS.groupby(df.DATA.dt.to_period('M')).agg('mean')
DF_TRI = df.loc[df.DATA.dt.to_period('Y')=='2019'].VENDAS.groupby(df.DATA.dt.to_period('Q')).agg('mean')
DF_ANO = df.VENDAS.groupby(df.DATA.dt.to_period('Y')).agg('mean')


fig_1 = go.Figure()
fig_1.add_trace(go.Bar(x=DF_MES.index.astype('str'),y=DF_MES.values,name='Mês'))
fig_1.add_trace(go.Scatter(x=DF_MES.index.astype('str'),y=[DF_TRI[int(i/4)] for i in range(12)],name='Trimestre'))

fig_1.update_layout({   "title": 
                        {
                                "text": "Faturamento por Mês",
                                "x": 0.05,
                                "xanchor": "left",
                        },
                        "xaxis": 
                        {       
                                "fixedrange": True
                        },
                        "yaxis": {
                                "fixedrange": True
                        }#,"colorway": ["#17B897"],
                        })


fig_2 = make_subplots(rows=1,cols=2,column_widths=[0.7,0.3])

fig_2.update_layout(title='Faturamento por Trimestre')
fig_2.add_trace(go.Bar(x=DF_TRI.index.astype('str'),y=DF_TRI.values,name='Trimestre'),
                            row=1, col=1)


fig_2.update_layout(title='Faturamento por Ano')
fig_2.add_trace(go.Bar(y=DF_ANO.index.astype('str'),x=DF_ANO.values,orientation='h',name='Ano'),
                row=1, col=2)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

app.title = "Sales Analytics!"

def create_header():
        return html.Div(
                className="header",
                children=[
                        #html.P(children="🔥", className="header-emoji"),
                        html.H1(
                                className="header-title",
                                children="📈Sales Analytics", 
                        ),
                        html.P(
                                className="header-description",
                                children="Analise de vendas de um restaurante localizado no Rio Grande do sul no periodo de 2 anos.",
                        ),
                ],
        )        

def create_dropdownmenu():
        return html.Div(
                className="menu",
                children=[       
                        html.Div(
                                children=[
                                        html.Div(children="Type", className="menu-title"),
                                        dcc.Dropdown(
                                                id="period-filter",
                                                options=[{"label": period, "value": period} for period in ['M','Q','Y']],
                                                value="M",
                                                clearable=False,
                                                searchable=False,
                                                className="dropdown",
                                        ),
                                ],
                        ),
                        html.Div(
                                children=[
                                        html.Div(children="Slider", className="menu-title",id="title-slider"),
                                        dcc.RangeSlider(
                                                id='year-slider',
                                                min=2018,
                                                max=2020,
                                                value=[2018,2020],
                                                marks={str(year): str(year) for year in df.DATA.dt.to_period('Y').unique()},
                                                step=None
                                        )
                                ],
                        )
                ],
        )

def create_graphs_1_2():
        return html.Div(
                className="wrapper",
                children=[
                        html.Div(
                                className="card",
                                children=dcc.Graph(
                                        id="price-chart",
                                        config={"displayModeBar": False},
                                        #figure=fig_1
                                ),
                        ),
                        html.Div(
                        className="card",
                        children=dcc.Graph(
                                #id="volume-chart",
                                #config={"displayModeBar": False},
                                figure=fig_2
                        ),
                        ),
                ],
                )

def create_slider():
        return 

app.layout = html.Div(
        children=[
                create_header(),
                create_dropdownmenu(),
                create_graphs_1_2(),
                create_slider(),
                html.Div(
                        className="wrapper",
                        children=[
                                html.Div(
                                        className="card",
                                        children=dcc.Graph(
                                                id="price-chart2",
                                                config={"displayModeBar": False},
                                                #figure=fig_1
                                        ),
                                ),
                                html.Div(
                                className="card",
                                children=dcc.Graph(
                                        #id="volume-chart",
                                        #config={"displayModeBar": False},
                                        figure=fig_2
                                ),
                                ),
                        ],
                )
                
        
    ]
)

@app.callback(
    Output("price-chart", "figure"),
    [
        Input("period-filter", "value"),
        Input("year-slider", "value"),
    ],
)
def update_charts(period, year_slider):

        if(year_slider[0]==year_slider[1]):
                mask = (df.DATA >= str(year_slider[0])) 
        else:
                mask = ((df.DATA >= str(year_slider[0])) & (df.DATA <= str(year_slider[1])))
        #fig_1 = data.loc[mask, :]
        df_period = df.loc[mask].VENDAS.groupby(df.DATA.dt.to_period(period)).agg('mean')
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_period.index.astype('str'),y=df_period.values,name='Mês'))
        #fig_1.add_trace(go.Scatter(x=df_period.index.astype('str'),y=[DF_TRI[int(i/4)] for i in range(12)],name='Trimestre'))

        fig.update_layout({"title": 
                                {
                                        "text": "Faturamento por Mês",
                                        "x": 0.05,
                                        "xanchor": "left",
                                },
                                "xaxis": 
                                {       
                                        "fixedrange": True
                                },
                                "yaxis": {
                                        "fixedrange": True
                                }#,"colorway": ["#17B897"],
                                })

        
        return fig

if __name__ == "__main__":
        app.run_server(debug=True)