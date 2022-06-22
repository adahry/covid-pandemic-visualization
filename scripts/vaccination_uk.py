import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


df = pd.read_csv("../data/covid-data.csv")
UK = df.loc[df['location'] == 'United Kingdom']

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
    go.Scatter(x=UK['date'], y=UK["new_cases_smoothed_per_million"], name="New cases",line=dict(color='red')),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=UK['date'], y=UK["new_vaccinations_smoothed_per_million"], name="New vaccinations",line=dict(color='green')),
    secondary_y=True,
)

fig.update_layout(hovermode="x", height=600, width=1000, template='plotly_white', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                  title = {'text': "Vaccinations vs new cases", 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
                  titlefont=dict(size=25),
                  xaxis=dict(tickfont={"size": 15}, titlefont={"color": "#673ab7"}, title = '<b>Date</b>'),
                  legend=dict(font=dict(size = 15)),
                  legend_title_text='Legend')

fig.update_yaxes(dict(tickfont={"size": 15}, titlefont={"color": "#673ab7"}, title = '<b>New cases per million</b>'), secondary_y=False, color='red')
fig.update_yaxes(dict(tickfont={"size": 15}, titlefont={"color": "#673ab7"}, title = '<b>New vaccinations per million</b>'), secondary_y=True, color='green')

fig.write_html("../images/vaccination_uk.html")
