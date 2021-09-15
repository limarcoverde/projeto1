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

from figs import *
from layout import *

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

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.title = "Sales Analytics!"

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