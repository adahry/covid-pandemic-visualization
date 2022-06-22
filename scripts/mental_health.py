import pandas as pd
import plotly.express as px


mental=pd.read_csv('../data/WICH_Wellbeing_Wellbeing_Anxiety_all.csv')
mental=mental[mental['Category Type']=='Age group']
mental=mental.iloc[::-1]

mental['date'] = pd.to_datetime(mental['Time period'],format= '%d/%m/%Y' )

fig = px.line(mental, x="date", y="Value",color='Category' ,title='Level of anxiety',template='simple_white')
fig.add_annotation(
    x='2020-06-23'
    , y=40
    , text=f'1st lockdown end'
    , yanchor='bottom'
    , showarrow=False
    , arrowhead=1
    , arrowsize=1
    , arrowwidth=2
    , arrowcolor="LightSalmon"
    , ax=-20
    , ay=-30
    , font=dict(size=15, color="#696969")
    , align="center"
    ,)


fig.add_annotation(
    x='2021-09-14'
    , y=40
    , text=f'PM unveils Plan B for winter'
    , yanchor='bottom'
    , showarrow=False
    , arrowhead=1
    , arrowsize=1
    , arrowwidth=2
    , arrowcolor="LightSalmon"
    , ax=-20
    , ay=-30
    , font=dict(size=15, color="#696969")
    , align="center"
    ,)

fig.update_layout(shapes=
                  [dict(type= 'line',
                        yref= 'paper', y0= 0, y1= 0.95,
                        xref= 'x', x0='2021-09-14', x1='2021-09-14',
                        line=dict(color="#696969", 
                                  width=3,
                                  dash="dot")),                   dict(type= 'line',
                        yref= 'paper', y0= 0, y1= 0.95,
                        xref= 'x', x0='2020-06-21', x1='2020-06-21',
                        line=dict(color="#696969",
                                  width=3,
                                  dash="dot")
                       )])



fig.add_vrect(
    x0="2020-10-31", x1="2020-12-02", annotation_text="2nd lockdown", annotation_position="top right",  
              annotation_font_size=15,
              annotation_font_color="#696969",
    fillcolor="#E6E6FA", opacity=0.5,
    layer="below", line_width=0,
),
fig.add_vrect(
    x0="2021-01-06", x1="2021-03-08", annotation_text="3rd lockdown",annotation_position="top right",  
              annotation_font_size=15,
              annotation_font_color="#696969",
    fillcolor="#E6E6FA", opacity=0.5,
    layer="below", line_width=0,
)

fig.update_layout(hovermode="x", height=600, width=1000, template='plotly_white', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                  title = {'text': "Level of anxiety", 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
                  titlefont=dict(size=25),
                  yaxis=dict(tickfont={"size": 15}, titlefont={"color": "#673ab7"}, title = '<b>Average % of respondents</b>'),
                  xaxis=dict(tickfont={"size": 15}, titlefont={"color": "#673ab7"}, title = '<b>Date</b>'),
                  legend=dict(font=dict(size = 15)),
                  legend_title_text='Age group')

fig.write_html("../images/mental_health.html")
