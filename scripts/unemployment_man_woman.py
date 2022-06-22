import pandas as pd
import plotly.express as px


emp=pd.read_csv('../data/employment.csv',sep=';')
cols=['Unemployed men','Unemployed women']

pd.options.plotting.backend = "plotly"
emp.plot(x='Period', y=cols)
df_melt = emp.melt(id_vars='Period', value_vars=cols)
fig=px.line(df_melt, x='Period' , y='value',color='variable' )
fig = px.line(df_melt, x="Period", y="value",title='Employment during covid',color='variable')
fig.update_xaxes(dtick=4)
fig.update_layout(hovermode="x", height=600, width=1000, template='plotly_white', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                  title = {'text': "Unemployment during pandemic by sex", 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
                  titlefont=dict(size=25),
                  yaxis=dict(tickfont={"size": 15}, titlefont={"color": "#673ab7"}, title = '<b>Unemployment rate in percentage points</b>'),
                  xaxis=dict(tickfont={"size": 15}, titlefont={"color": "#673ab7"}, title = '<b>Date</b>'),
                  legend=dict(font=dict(size = 15)),
                  legend_title_text='Sex') 

fig.write_html("../images/unemployment_man_woman.html")
