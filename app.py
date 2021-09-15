import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_auth

import pandas as pd
import numpy as np

df = pd.read_csv('sales_with_extra_features.csv')
df['DATA'] = pd.to_datetime(df['DATA'])

DF_MES = df.loc[df.DATA.dt.to_period('Y')=='2019'].VENDAS.groupby(df.DATA.dt.to_period('M')).agg('mean')
DF_TRI = df.loc[df.DATA.dt.to_period('Y')=='2019'].VENDAS.groupby(df.DATA.dt.to_period('Q')).agg('mean')
DF_ANO = df.VENDAS.groupby(df.DATA.dt.to_period('Y')).agg('mean')


fig_1 = go.Figure()
fig_1.add_trace(go.Bar(x=DF_MES.index.astype('str'),y=DF_MES.values,name='Mês'))
fig_1.add_trace(go.Scatter(x=DF_MES.index.astype('str'),y=[DF_TRI[int(i/4)] for i in range(12)],name='Trimestre'))



fig_2 = make_subplots(rows=1,cols=2,column_widths=[0.7,0.3])

fig_2.update_layout(title='Faturamento por Trimestre')
fig_2.add_trace(go.Bar(x=DF_TRI.index.astype('str'),y=DF_TRI.values,name='Trimestre'),
                            row=1, col=1)


fig_2.update_layout(title='Faturamento por Ano')
fig_2.add_trace(go.Bar(y=DF_ANO.index.astype('str'),x=DF_ANO.values,orientation='h',name='Ano'),
                row=1, col=2)


pio.templates.default = "plotly_white"

# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {
    'Tomas': '123'
}

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)
server = app.server

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.title = "Sales Analytics!"

def CreateHeader():
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




app.layout = html.Div(
        children=[
                CreateHeader(),

                CreateMenu(
                        className="menu-header",
                        children=[
                                 CreateDropDownMenu(
                                                id="agg-filter",
                                                title="Agregador",
                                                options=[{"label": period, "value": p} for p,period in [('mean','Média'),('sum','Total'),('std','Desvio Padrão')]],
                                                value="sum"),
                                CreateDropDownMenu(
                                                id="period-filter",
                                                title="Período",
                                                options=[{"label": period, "value": p} for p,period in [('M','Mês'),('Q','Trimestre'),('Y','Ano')]],
                                                value="M")
                        ]),
                CreateGraph("price-chart","Média de vendas"),
                CreateMenu([ 
                        CreateSlider(
                                        id='year-slider',
                                        title="Slider",
                                        min=2018,
                                        max=2020,
                                        value=[2018,2020],
                                        marks={str(year): str(year) for year in df.DATA.dt.to_period('Y').unique()})
                ]),
        ]
)

@app.callback(
    Output("price-chart", "figure"),
    [
        Input("agg-filter", "value"),
        Input("period-filter", "value"),
        Input("year-slider", "value"),
    ],
)
def update_chart_filter_slider(agg,period, year_slider):

        if(year_slider[0]==year_slider[1]):
                mask = (df.DATA.dt.to_period('Y') == str(year_slider[0])) 
        else:
                mask = ((df.DATA >= str(year_slider[0])) & (df.DATA < str(year_slider[1]+1)))

        df_period = df.loc[mask].VENDAS.groupby(df.DATA.dt.to_period(period)).agg(agg)

        fig = go.Figure()

        fig.add_trace(  go.Bar( x=df_period.index.astype('str'),
                                y=df_period.values))
        

        return fig

if __name__ == "__main__":
        app.run_server(debug=True)