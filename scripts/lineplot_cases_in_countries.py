import plotly
import plotly.graph_objects as go
import pandas as pd
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

d2 = {'North East': 'England',
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

country_pop = {'Wales': 3.169586,
             'Scotland': 5.466000,
             'Northern Ireland': 1.895510,
             'England': 56.550138}

df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12])
df['nuts118cd'] = df['areaName'].map(d)
df = df.groupby(['areaName', 'nuts118cd', 'date']).agg(
    Cases=('newCasesBySpecimenDate', sum))
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
               columns=[ 'areaName', 'nuts118cd', 'date', 'Cases']),
               ignore_index = True)

dates = list(set(list(df['date'])))
dates.sort()
dates = dates[62:812]

df['month'] = None
df['30 days up to and including'] = None

k = 1
for i in range(0,750,30):
    d = dates[i:i+30]
    df.loc[df["date"].isin(d), 'month'] = k
    df.loc[df["date"].isin(d), '30 days up to and including'] = d[29]
    k += 1
    
df = df.groupby(['areaName', 'nuts118cd', 'month', '30 days up to and including']).agg(
    Cases=('Cases', sum))
df.reset_index(inplace=True)

df['Nation'] = df['areaName'].map(d2)
df['Country_pop'] = df['Nation'].map(country_pop)

df = df.groupby(['Nation', '30 days up to and including', 'Country_pop']).agg(
    Cases=('Cases', sum))
df.reset_index(inplace=True)

df['Cases per 1,000,000 people'] = df['Cases'] / df['Country_pop']

df_tot = df.groupby(['30 days up to and including']).agg(
    Cases=('Cases', sum), Country_pop=('Country_pop', sum))
df_tot.reset_index(inplace=True)
df_tot['Cases per 1,000,000 people'] = df_tot['Cases'] / df_tot['Country_pop']
df_tot['Nation'] = 'total'
df = pd.concat([df, df_tot])


# Create figure
fig = go.Figure()

nations = ['England', 'Northern Ireland', 'Scotland', 'Wales', 'total']

for n in nations:
    # Add traces
    fig.add_trace(go.Scatter(x=df['30 days up to and including'], y=df[df['Nation'] == n]['Cases per 1,000,000 people'], name=n))

# Style all the traces
fig.update_traces(hoverinfo="name+x+text+name+y+text", line={"width": 2}, mode="lines")

# Update layout
fig.update_layout(hovermode="x", height=600, width=1000, template='plotly_white', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                  title = {'text': "New cases by country", 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
                  titlefont=dict(size=25),
                  yaxis=dict(tickfont={"size": 15}, titlefont={"color": "#673ab7"}, title = '<b>Total of cases per 100,000 people from 30 days</b>'),
                  xaxis=dict(tickfont={"size": 15}, titlefont={"color": "#673ab7"}, title = '<b>Date up to and including</b>'),
                  legend=dict(font=dict(size = 15)),
                  legend_title_text='Country')


fig.write_html("../images/lineplot_cases_in_countries.html")
