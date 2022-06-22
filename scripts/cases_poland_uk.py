import pandas as pd 
import plotly.express as px

df = pd.read_csv("../data/covid-data.csv")
Poland = df.loc[df['location'] == 'Poland']
UK = df.loc[df['location'] == 'United Kingdom']


PolandUK = Poland.append(UK, ignore_index=True)
fig = px.line(PolandUK, x="date", y="new_cases_smoothed_per_million",color='location' ,title='Nuber of cases',template='plotly_white')
fig.update_layout(hovermode="x", height=600, width=1000, template='plotly_white', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                  title = {'text': "Number of cases in Poland vs UK", 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
                  titlefont=dict(size=25),
                  yaxis=dict(tickfont={"size": 15}, titlefont={"color": "#673ab7"}, title = '<b>Cases per million</b>'),
                  xaxis=dict(tickfont={"size": 15}, titlefont={"color": "#673ab7"}, title = '<b>Date</b>'),
                  legend=dict(font=dict(size = 15)),
                  legend_title_text='Nation')

fig.write_html("../images/cases_poland_uk.html")
