import plotly
import pandas as pd
import json
import plotly.express as px
from geojson_rewind import rewind
import warnings

plotly.offline.init_notebook_mode()
warnings.filterwarnings('ignore')


df1 = pd.read_csv('../data/East_Midlands_Deaths.csv')
df2 = pd.read_csv('../data/West_Midlands_Deaths.csv')
df3 = pd.read_csv('../data/East_of_England_Deaths.csv')
df4 = pd.read_csv('../data/London_Deaths.csv')
df5 = pd.read_csv('../data/North_East_Deaths.csv')
df6 = pd.read_csv('../data/North_West_Deaths.csv')
df7 = pd.read_csv('../data/Northern_Ireland_Deaths.csv')
df8 = pd.read_csv('../data/South_East_Deaths.csv')
df9 = pd.read_csv('../data/South_West_Deaths.csv')
df10 = pd.read_csv('../data/Yorkshire_and_The_Humber_Deaths.csv')
df11 = pd.read_csv('../data/Scotland_Deaths.csv')
df12 = pd.read_csv('../data/Wales_Deaths.csv')

population = pd.read_excel('../data/UK_Population_2020.xlsx')
population['Population per 1,000,000'] = population['Population'] / 1000000

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
df['nuts118cd'] = df['areaName'].map(d)
df = df.groupby(['areaName', 'nuts118cd', 'date']).agg(
    Deaths=('newDeaths28DaysByDeathDate', sum))
df = df.dropna()
df.reset_index(inplace=True)

dates = list(set(list(df['date'])))
dates.sort()
new = []
for date in dates:
    for k in d.keys():
        l = len(df[(df['date']==date) & (df['areaName']==k)])
        if l == 0:
            vals = [k, d[k], date, 0]
            new.append(vals)
df = df.append(pd.DataFrame(new,
               columns=[ 'areaName', 'nuts118cd', 'date', 'Deaths']),
               ignore_index = True)

dates = list(set(list(df['date'])))
dates.sort()
dates = dates[30:780]

df['month'] = None
df['30 days up to and including'] = None

k = 1
for i in range(0,750,30):
    d = dates[i:i+30]
    df.loc[df["date"].isin(d), 'month'] = k
    df.loc[df["date"].isin(d), '30 days up to and including'] = d[29]
    k += 1

df = df.groupby(['areaName', 'nuts118cd', 'month', '30 days up to and including']).agg(
    Deaths=('Deaths', sum))
df.reset_index(inplace=True)

df_to_plot = pd.merge(df, population, on="areaName")
df_to_plot['Deaths per 1,000,000 people'] = df_to_plot['Deaths'] / df_to_plot['Population per 1,000,000']

# Load GeoJson 
with open('../data/NUTS_Level_1_(January_2018)_Boundaries.json') as f:
    counties = json.load(f)

counties_corrected=rewind(counties,rfc7946=False)

# Create figure
fig = px.choropleth_mapbox(df_to_plot, geojson=counties_corrected, locations='nuts118cd', featureidkey="properties.nuts118cd", 
                    color='Deaths per 1,000,000 people', color_continuous_scale="RdPu", range_color=(0,600),
                    animation_frame="30 days up to and including", width=900, height=800, hover_name='areaName',
                    mapbox_style="carto-positron", zoom=4.5, center = {"lat": 55.5, "lon": -4})

fig.update_layout(
    title={'text': "<br>30-days totals of COVID-19 deaths per million people</br> from 01.04.2020 to 20.04.2022 by region",
        'y': 1,
        'x':0.4,
        'xanchor': 'center',
        'yanchor': 'top'},
    font=dict(size=15),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)')

fig.write_html("../images/interactive_map_deaths.html")

