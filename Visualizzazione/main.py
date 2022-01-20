
""" Importazione librerie """
# Manipolazione

import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype
import datetime

# Visualizzazione
import dash
import plotly.express as px
import plotly.graph_objects as go

# Setup
path = './data_viz/'

""" 
Importazione e manipolazione dei Datasets
"""

# IQA vs tempo

# Importazione
aria_milano_96_21 = pd.read_csv(f'{path}aria_milano_96_21_normalizzato.csv',
                      parse_dates=['Data'],
                      dayfirst=True,
                      index_col = 0
                     )

# Correzione dei datatypes

# Interi
"""
for col in [
        'Biossido di Azoto_Count_sensori', 'Biossido di Azoto_Indice numerico',
        'Biossido di Zolfo_Count_sensori', 'Biossido di Zolfo_Indice numerico',
        'Ozono_Count_sensori', 'Ozono_Indice numerico',
        'PM10 (SM2005)_Count_sensori', 'PM10 (SM2005)_Indice numerico',
        'Particelle sospese PM2.5_Count_sensori',
        'Particelle sospese PM2.5_Indice numerico', 'IQA_numerico',
]:
    aria_milano_96_21[col] = aria_milano_96_21[col].astype('Int64')

# Float
for col in [
        'Biossido di Azoto_Valore_interesse',
        'Biossido di Azoto_Valore_interesse_std',
        'Biossido di Zolfo_Valore_interesse',
        'Biossido di Zolfo_Valore_interesse_std', 'Ozono_Valore_interesse',
        'Ozono_Valore_interesse_std', 'PM10 (SM2005)_Valore_interesse',
        'PM10 (SM2005)_Valore_interesse_std',
        'Particelle sospese PM2.5_Valore_interesse',
        'Particelle sospese PM2.5_Valore_interesse_std'
]:
    aria_milano_96_21[col] = aria_milano_96_21[col].astype('float64')
"""
# Categoriche ordinali
# Definisco le categorie e le ordino
IQA_type = CategoricalDtype(categories=[
    'Molto Buona', 'Buona', 'Accettabile', 'Scarsa', 'Molto Scarsa', 'ND'
],
                            ordered=True)

# Assegno
for col in [
        'Biossido di Azoto_Indice testuale',
        'Biossido di Zolfo_Indice testuale', 'Ozono_Indice testuale',
        'PM10 (SM2005)_Indice testuale',
        'Particelle sospese PM2.5_Indice testuale', 'IQA'
]:
    aria_milano_96_21[col] = aria_milano_96_21['IQA'].astype(IQA_type)


print(aria_milano_96_21.dtypes)
"""
Visualizzazione
"""
def discrete_colorscale(bvals, colors):
    """
    bvals - list of values bounding intervals/ranges of interest
    colors - list of rgb or hex colorcodes for values in [bvals[k], bvals[k+1]],0<=k < len(bvals)-1
    returns the plotly  discrete colorscale
    """
    if len(bvals) != len(colors) + 1:
        raise ValueError('len(boundary values) should be equal to  len(colors)+1')
    bvals = sorted(bvals)
    nvals = [(v - bvals[0]) / (bvals[-1] - bvals[0]) for v in bvals]  # normalized values

    dcolorscale = []  # discrete colorscale
    for k in range(len(colors)):
        dcolorscale.extend([[nvals[k], colors[k]], [nvals[k + 1], colors[k]]])
    return dcolorscale

bvals = [1, 2, 3, 4, 5, 6]
colors = ['#88F7E2', '#44D492', '#F5EB67' , '#FFA15C', '#FA233E']
dcolorsc = discrete_colorscale(bvals, colors[::-1])

fig = go.Figure(data=go.Heatmap(
        x= [aria_milano_96_21['Data'].dt.month, aria_milano_96_21['Data'].dt.day],
        y= aria_milano_96_21['Data'].dt.year))
fig.update_traces(z= aria_milano_96_21['IQA'], selector=dict(type='heatmap'))
fig.show()

fig = px.imshow(
        x= [aria_milano_96_21['Data'].dt.month, aria_milano_96_21['Data'].dt.day],
        y= aria_milano_96_21['Data'].dt.year)
fig.update_xaxes(side="top")
fig.show()
