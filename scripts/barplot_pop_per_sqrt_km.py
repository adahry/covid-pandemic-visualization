import plotly
import pandas as pd
from urllib.request import urlopen
import numpy as np
import plotly.express as px
from geojson_rewind import rewind
import warnings

plotly.offline.init_notebook_mode()
warnings.filterwarnings('ignore')



df1 = pd.read_csv('../data/East_Midlands_cases.csv')
df2 = pd.read_csv('../data/West_Midlands_cases.csv')
df3 = pd.read_csv('../data/East_of_England_cases.csv')
df4 = pd.read_csv('../data/London_cases.csv')
df5 = pd.read_csv('../data/North_East_cases.csv')
df6 = pd.read_csv('../data/North_West_cases.csv')
df7 = pd.read_csv('../data/Northern_Ireland_cases.csv')
df8 = pd.read_csv('../data/South_East_cases.csv')
df9 = pd.read_csv('../data/South_West_cases.csv')
df10 = pd.read_csv('../data/Yorkshire_and_The_Humber_cases.csv')
df11 = pd.read_csv('../data/Scotland_cases.csv')
df12 = pd.read_csv('../data/Wales_cases.csv')

size_area = {'Wales': 20779,
             'Scotland': 77910,
             'Northern Ireland': 14130,
             'England': 130279}

d = {'North East': 'England',
    'North West': 'England',
    'Yorkshire and The Humber': 'England',
    'East Midlands': 'England',
    'West Midlands': 'England',
    'East of England': 'England',
    'London': 'England',
    'South East': 'England',
    'South West': 'England',
    'Wales': 'Wales',
    'Scotland': 'Scotland',
    'Northern Ireland': 'Northern Ireland'}

population = pd.read_excel('../data/UK_Population_2020.xlsx')
population['Population per 1,000,000'] = population['Population'] / 1000000

population_to_plot = pd.read_excel('../data/UK_Population_2020.xlsx')
population_to_plot['Nation'] = population_to_plot['areaName'].map(d)
population_to_plot = population_to_plot.groupby(['Nation']).agg(
    Population=('Population', sum))
population_to_plot.reset_index(inplace=True)
population_to_plot['Area'] = population_to_plot['Nation'].map(size_area)
population_to_plot['Population per 1 sqrt km'] = population_to_plot['Population'] / population_to_plot['Area']

fig = px.bar(population_to_plot, x="Nation", y="Population per 1 sqrt km", color="Nation", template='plotly_white')
fig.update_layout(height=600, width=1000, template='plotly_white', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                  title = {'text': "Population per 1 sqrt km in different UK countries", 'y': 0.95, 'x':0.45, 'xanchor': 'center', 'yanchor': 'top'},
                  titlefont=dict(size=25),
                  yaxis=dict(tickfont={"size": 15}, titlefont={"color": "#673ab7"}, title = '<b>Population per 1 sqrt km</b>'),
                  xaxis=dict(tickfont={"size": 15}, titlefont={"color": "#673ab7"}, title = '<b>Country</b>'),
                  legend=dict(font=dict(size = 15)),
                  legend_title_text='Nation')

fig.write_html("../images/barplot_pop_per_sqrt_km.html")