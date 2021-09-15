import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
from sklearn.metrics import r2_score
import numpy as np
import pandas as pd
from sklearn.feature_selection import RFE
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor

import pandas as pd
import numpy as np

pio.templates.default = "plotly_white"

df = pd.read_csv('sales_with_extra_features.csv')
df['DATA'] = pd.to_datetime(df['DATA'])

X = df.drop(['VENDAS','DATA'],axis=1)
Y = df['VENDAS'].values

X_train = X[df.DATA < '2020'] 
X_test  = X[df.DATA >= '2020'] 
Y_train = Y[df.DATA < '2020'] 
Y_test  = Y[df.DATA >= '2020'] 

pipelines = []
pipelines.append(('LR', Pipeline([('LR',LinearRegression())])))
#pipelines.append(('LASSO', Pipeline([('LASSO', Lasso())])))
pipelines.append(('EN', Pipeline([('EN', ElasticNet())])))
pipelines.append(('KNN', Pipeline([('KNN', KNeighborsRegressor())])))
pipelines.append(('DTR', Pipeline([('CART', DecisionTreeRegressor())])))
#pipelines.append(('GBM', Pipeline([('GBM', GradientBoostingRegressor())])))


results_1 = []

fig_1 = go.Figure()
#fig_1.add_trace(go.Scatter(y=Y_test,name='True',mode='lines+markers'))

for name, model in pipelines:

    model.fit(X_train, Y_train)
    model_score = model.score(X_train,Y_train)
    
    Y_pred = model.predict(X_test)
    
    model_r2score =  r2_score(Y_test, Y_pred)
    
    cv_results = cross_val_score(model, X_train, Y_train, cv=5)
    cv_mean = cv_results.mean()
    cv_std = cv_results.std()
    fig_1.add_trace(go.Bar(y=Y_test-Y_pred,name=name))

    results_1.append((name,model_score,model_r2score,cv_mean,cv_std))

fig_1.update_yaxes(range=[-70,70])

aux = pd.DataFrame(results_1,columns=['model','score','r2score','CV(mean)','CV(std)']).round(2).sort_values('score',ascending=False)

fig_2 = go.Figure(data=[go.Table(
        header=dict(values=['<b>'+x+'</b>' for x in aux.columns],
                    fill_color='LightSlateGrey',
                    line_color='darkslategray',
                    align=['left','center'],
                    font=dict(color='white', size=12)),

        cells=dict(values=aux.values.T,
                   fill_color='lightgrey',
                   align = ['left', 'center'])
)])


pipelines = []
pipelines.append(('ScaledLR',   Pipeline([('Scaler',  StandardScaler()),('LR',LinearRegression())])))
#pipelines.append(('ScaledLASSO',Pipeline([('Scaler',  StandardScaler()),('LASSO', Lasso())])))
pipelines.append(('ScaledEN',   Pipeline([('Scaler',  StandardScaler()),('EN', ElasticNet())])))
pipelines.append(('ScaledKNN',  Pipeline([('Scaler',  StandardScaler()),('KNN', KNeighborsRegressor())])))
pipelines.append(('ScaledDTR',  Pipeline([('Scaler', StandardScaler()),('DTR', DecisionTreeRegressor())])))
#pipelines.append(('ScaledGBM',  Pipeline([('Scaler',  StandardScaler()),('GBM', GradientBoostingRegressor())])))

fig_3 =go.Figure()

#fig_3.add_trace(go.Scatter(y=Y_test,name='True'))

results_2 = []

for name, model in pipelines:

        model.fit(X_train, Y_train)
        model_score = model.score(X_train,Y_train)
        
        Y_pred = model.predict(X_test)
        
        model_r2score =  r2_score(Y_test, Y_pred)
        
        cv_results = cross_val_score(model, X_train, Y_train, cv=5)
        cv_mean = cv_results.mean()
        cv_std = cv_results.mean()
    
    
        results_2.append((name,model_score,model_r2score,cv_mean,cv_std))
  
        fig_3.add_trace(go.Bar(y=Y_test-Y_pred,name=name))


aux = pd.DataFrame(results_2,columns=['model','score','r2score','CV(mean)','CV(std)']).round(2).sort_values('score',ascending=False)

fig_4 = go.Figure(data=[go.Table(
        header=dict(values=['<b>'+x+'</b>' for x in aux.columns],
                    fill_color='LightSlateGrey',
                    line_color='darkslategray',
                    align=['left','center'],
                    font=dict(color='white', size=12)),

        cells=dict(values=aux.values.T,
                   fill_color='lightgrey',
                   align = ['left', 'center'])
)])


col = ['DS', 'DATA_FESTIVA', 'VESPERA_DATA_FESTIVA',
       'POS_DATA_FESTIVA', 'DATA_NAO_FESTIVA', 'NAO_FERIADO',
       'SEMANA_PAGAMENTO', 'SEMANA_DE_NAO_PAGAMENTO', 'BAIXA_TEMPORADA',
       'ALTA_TEMPORADA','PRECIPITACAO','UMIDADE','VENDAS_STD_TRIM','VENDAS_MEDIA_TRIM']

dfClean = df.drop(col,axis=1)
dfClean['CHOVEU'] = df.PRECIPITACAO.apply(lambda x : 1 if x!=0 else 0)

X = dfClean.drop(['VENDAS','DATA'],axis=1)
Y = dfClean['VENDAS'].values

X_train = X[dfClean.DATA < '2020'] 
X_test  = X[dfClean.DATA >= '2020'] 
Y_train = Y[dfClean.DATA < '2020'] 
Y_test  = Y[dfClean.DATA >= '2020'] 

pipelines=[]
#pipelines.append(('MLPR', Pipeline([('MLPR', MLPRegressor(max_iter=1000))])))
pipelines.append(('LR', Pipeline([('LR',LinearRegression())])))

results_3 = []

fig_5 =go.Figure()
fig_5.add_trace(go.Scatter(y=Y_test,name='True'))

for name, model in pipelines:

    model.fit(X_train, Y_train)
    model_score = model.score(X_train,Y_train)
    
    Y_pred = model.predict(X_test)
    
    model_r2score =  r2_score(Y_test, Y_pred)
    
    cv_results = cross_val_score(model, X_train, Y_train, cv=5)
    cv_mean = cv_results.mean()
    cv_std = cv_results.mean()
    
    results_3.append((name,model_score,model_r2score,cv_mean,cv_std))
  
    fig_5.add_trace(go.Scatter(y=Y_pred,name=name))


aux = pd.DataFrame(results_3,columns=['model','score','r2score','CV(mean)','CV(std)']).round(2).sort_values('score',ascending=False)

fig_6 = go.Figure(data=[go.Table(
        header=dict(values=['<b>'+x+'</b>' for x in aux.columns],
                    fill_color='LightSlateGrey',
                    line_color='darkslategray',
                    align=['left','center'],
                    font=dict(color='white', size=12)),

        cells=dict(values=aux.values.T,
                   fill_color='lightgrey',
                   align = ['left', 'center'])
)])


col = ['DS', 'DATA_FESTIVA', 'VESPERA_DATA_FESTIVA',
       'POS_DATA_FESTIVA', 'DATA_NAO_FESTIVA', 'NAO_FERIADO',
       'SEMANA_PAGAMENTO', 'SEMANA_DE_NAO_PAGAMENTO', 'BAIXA_TEMPORADA',
       'ALTA_TEMPORADA','PRECIPITACAO','UMIDADE','VENDAS_STD_TRIM','VENDAS_MEDIA_TRIM']

dfClean = df.drop(col,axis=1)
dfClean['CHOVEU'] = df.PRECIPITACAO.apply(lambda x : 1 if x!=0 else 0)
dfClean['CLASS'] = (dfClean.VENDAS//10)

X = dfClean.drop(['VENDAS','DATA'],axis=1)
Y = dfClean['CLASS'].values

X_train = X[dfClean.DATA < '2020'] 
X_test  = X[dfClean.DATA >= '2020'] 
Y_train = Y[dfClean.DATA < '2020'] 
Y_test  = Y[dfClean.DATA >= '2020'] 


pipelines=[]
pipelines.append(('LR',  Pipeline([('LR', LinearRegression())])))
pipelines.append(('DTR',  Pipeline([('DTR', DecisionTreeRegressor())])))

fig_7 =go.Figure()

fig_7.add_trace(go.Scatter(y=df[dfClean.DATA >= '2020'].VENDAS,name='True'))

results_4 = []

for name, model in pipelines:

        model.fit(X_train, Y_train)
        model_score = model.score(X_train,Y_train)
        
        Y_pred = model.predict(X_test)
        
        model_r2score =  r2_score(Y_test, Y_pred)
        
        cv_results = cross_val_score(model, X_train, Y_train, cv=5)
        cv_mean = cv_results.mean()
        cv_std = cv_results.mean()
        
        results_4.append((name,model_score,model_r2score,cv_mean,cv_std))
    




aux = pd.DataFrame(results_4,columns=['model','score','r2score','CV(mean)','CV(std)']).round(2).sort_values('score',ascending=False)

fig_8 = go.Figure(data=[go.Table(
        header=dict(values=['<b>'+x+'</b>' for x in aux.columns],
                    fill_color='LightSlateGrey',
                    line_color='darkslategray',
                    align=['left','center'],
                    font=dict(color='white', size=12)),

        cells=dict(values=aux.values.T,
                   fill_color='lightgrey',
                   align = ['left', 'center'])
)])