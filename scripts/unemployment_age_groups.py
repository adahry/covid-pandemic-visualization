import pandas as pd
import plotly.express as px


unemp=pd.read_csv('../data/Figure_8__The_decrease_in_unemployment_was_driven_by_those_unemployed_for_over_6_months.csv',skiprows=6)
unemp=unemp.iloc[20:]
cols=unemp.columns[1:].tolist()

pd.options.plotting.backend = "plotly"
unemp.plot(x='Period', y=cols)
df_melt = unemp.melt(id_vars='Period', value_vars=cols)
fig=px.line(df_melt, x='Period' , y='value',color='variable' )
fig = px.line(df_melt, x="Period", y="value",title='Unemployment in the UK',color='variable',template='plotly_white')

fig.add_vline(x=20, line_width=2, line_dash="dash", line_color="black", annotation_text="Pandemic starts", annotation_position="top left")
fig.update_yaxes(dtick=250)
fig.update_xaxes(dtick=5)
fig.update_layout(hovermode="x", height=600, width=1000, template='plotly_white', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                  title = {'text': "Unemployment in the UK", 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
                  titlefont=dict(size=25),
                  yaxis=dict(tickfont={"size": 15}, titlefont={"color": "#673ab7"}, title = '<b>Number of people in thousands</b>'),
                  xaxis=dict(tickfont={"size": 15}, titlefont={"color": "#673ab7"}, title = '<b>Date</b>'),
                  legend=dict(font=dict(size = 15)),
                  legend_title_text='Period') 

fig.write_html("../images/unemployment_age_groups.html")
