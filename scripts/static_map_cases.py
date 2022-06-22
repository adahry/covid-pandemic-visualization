import plotly
import pandas as pd
import json
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
d = {'North East': 'UKC',
    'North West': 'UKD',
    'Yorkshire and The Humber': 'UKE',
    'East Midlands': 'UKF',
    'West Midlands': 'UKG',
    'East of England': 'UKH',
    'London': 'UKI',
    'South East': 'UKJ',
    'South West': 'UKK',
    'Wales': 'UKL',
    'Scotland': 'UKM',
    'Northern Ireland': 'UKN'}

df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12])

dates = list(set(list(df['date'])))
dates.sort()
dates = dates[62:812]

df = df[df['date'].isin(dates)]
df['nuts118cd'] = df['areaName'].map(d)
df = df.groupby(['areaName', 'nuts118cd']).agg(
    Cases=('newCasesBySpecimenDate', sum))
df = df.dropna()
df.reset_index(inplace=True)
df = df.rename(columns = {'Cases': 'Number of cases'})


#Load GeoJson 
with open('../data/NUTS_Level_1_(January_2018)_Boundaries.json') as f:
    counties = json.load(f)

counties_corrected=rewind(counties,rfc7946=False)

fig = px.choropleth_mapbox(df, geojson=counties_corrected, locations='nuts118cd', featureidkey="properties.nuts118cd", color='Number of cases',
                            color_continuous_scale="OrRd",
                            width=900, height=800, hover_name=df['areaName'],
                            mapbox_style="carto-positron", zoom=4.5, center = {"lat": 55.5, "lon": -4})
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(
    title={'text': "Totals of reported cases from 01.04.2020 to 20.04.2022 by region",
            'y': 0.975,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
    font=dict(size=15),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)')

fig.write_html("../images/static_map_cases.html")