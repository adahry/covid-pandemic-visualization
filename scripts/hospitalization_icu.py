import pandas as pd 
import plotly.graph_objects as go
from plotly.subplots import make_subplots


df = pd.read_csv("../data/covid-data.csv")
UK = df.loc[df['location'] == 'United Kingdom']

fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(x=UK['date'], y=UK["hosp_patients"], name="Hospitalized patients",line=dict(color='black')),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=UK['date'], y=UK["icu_patients"], name="ICU patients",line=dict(color='red')),
    secondary_y=True,
)


fig.update_xaxes(title_text="Date")
fig.update_layout(hovermode="x", height=600, width=1000, template='plotly_white', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                  title = {'text': "Hospitalization and ICU", 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
                  titlefont=dict(size=25),
                  xaxis=dict(tickfont={"size": 15}, titlefont={"color": "#673ab7"}, title = '<b>Date</b>'),
                  legend=dict(font=dict(size = 15)),
                  legend_title_text='Legend')

fig.update_yaxes(dict(tickfont={"size": 15}, titlefont={"color": "#673ab7"}, title = '<b>Hospitalized patients</b>'), secondary_y=False, color='black')
fig.update_yaxes(dict(tickfont={"size": 15}, titlefont={"color": "#673ab7"}, title = '<b>ICU patietns</b>'), secondary_y=True, color='red')

fig.write_html("../images/hospitalization_icu.html")
