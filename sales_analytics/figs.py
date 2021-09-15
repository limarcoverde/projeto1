import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

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
