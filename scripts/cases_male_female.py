import pandas as pd
import plotly.graph_objects as gp


male=pd.read_csv("../data/male_2022-05-09.csv")
female=pd.read_csv("../data/female_2022-05-09.csv")

female['sex']='Female'
male['sex']='Male'

femalemale=pd.concat([female,male], ignore_index=True)
femalemale['age'].unique()
femalemale['age'] = femalemale['age'].replace(['5_to_9', '80_to_84', '65_to_69', '35_to_39', '10_to_14',
       '50_to_54', '85_to_89', '55_to_59', '45_to_49', '75_to_79',
       '0_to_4', '70_to_74', '30_to_34', '60_to_64', '25_to_29',
       '40_to_44', '15_to_19', '90+', '20_to_24'],['5-9', '80-84', '65-69', '35-39', '10-14',
       '50-54', '85-89', '55-59', '45-49', '75-79',
       '0-4', '70-74', '30-34', '60-64', '25-29',
       '40-44', '15-19', '90+', '20-24'])

myorder = ['0-4', '5-9', "10-14", "15-19","20-24","25-29","30-34","35-39","40-44","45-49","50-54","55-59","60-64","65-69","70-74","75-79","80-84","85-89","90+"]
femalemale['age'] = pd.Categorical(femalemale['age'], categories=myorder, ordered=True)
femalemale = femalemale.sort_values('age')

femalemale['date'] = pd.to_datetime(femalemale['date'])
most_recent_date = femalemale['date'].max()

df_to_plot=femalemale[femalemale['date']==most_recent_date]
male = df_to_plot[df_to_plot['sex'] =='Male']
female = df_to_plot[df_to_plot['sex'] =='Female']

fig = gp.Figure()

# Adding Male data to the figure
fig.add_trace(gp.Bar(y= male['age'], x = male['value'],
					name = 'Male',
					orientation = 'h',marker = {'color' : 'green'}))

# Adding Female data to the figure
fig.add_trace(gp.Bar(y = female['age'], x = female['value']* -1,
					name = 'Female', orientation = 'h',marker = {'color' : 'darkviolet'}))

# Updating the layout for our graph
fig.update_layout(barmode = 'relative',
				bargap = 0.0, bargroupgap = 0,
				xaxis = dict(range=[-1000000, 1000000],tickvals = [-1000000,-750000 ,-500000, -250000,
										0, 250000, 500000,750000 ,1000000],
								
							ticktext = ['1M','750k' ,'500k', '250k', '0',
										'250k', '500k','750k' ,'1M']
)
				)

fig.update_layout(hovermode="x", height=600, width=1000, template='plotly_white', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                  title = {'text': "Cases by age group and sex", 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
                  titlefont=dict(size=25),
                  yaxis=dict(tickfont={"size": 15}, titlefont={"color": "#673ab7"}, title = '<b>Age group</b>'),
                  xaxis=dict(tickfont={"size": 15}, titlefont={"color": "#673ab7"}, title = '<b>Number of cases</b>'),
                  legend=dict(font=dict(size = 15)),
                  legend_title_text='Sex')

fig.write_html("../images/cases_male_female.html")
