
import streamlit as st
import os
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import warnings
warnings.filterwarnings('ignore')

# 00 CREATING TAB TITLE

st.set_page_config(
  page_title = 'Invistico Airline Review',
  page_icon = ':airplane_departure:',
  layout = 'wide',
)


# 01 CREATING DASHBOARD TITLE

st.title(':airplane_departure: Invistico Airline Review Dashboard')
st.markdown('<style>div,block-container{padding-top:0rem;}<style>', unsafe_allow_html = True)


# 02 IMPORTING DATASET

dataset_path = 'https://raw.githubusercontent.com/azzindani/00_Data_Source/main/Invistico_Airline.csv'
df = pd.read_csv(dataset_path)

for x in df.columns:
  y = x.title()
  df = df.rename(columns = {x : y})

for x in df.columns:
  if df[x].dtypes == 'object':
    try:
      df[x] = df[x].str.strip()
    except:
      pass

for x in df.columns:
  if df[x].dtypes == 'object':
    for a in df[x].unique():
      b = a.title()
      df[x] = df[x].replace(a, b)
  else:
    pass

df = df.fillna(0)

df.loc[(df['Departure Delay In Minutes'] > 0), 'Departure Delay'] = 'Delayed'
df.loc[(df['Departure Delay In Minutes'] == 0), 'Departure Delay'] = 'Not Delayed'

df.loc[(df['Arrival Delay In Minutes'] > 0), 'Arrival Delay'] = 'Delayed'
df.loc[(df['Arrival Delay In Minutes'] == 0), 'Arrival Delay'] = 'Not Delayed'

sat_df = df[df['Satisfaction'] == 'Satisfied']
dis_df = df[df['Satisfaction'] == 'Dissatisfied']


# 03 SETUP TEMPLATE & THEME

colors_1 = px.colors.sequential.Purples_r
colors_2 = px.colors.sequential.Greens_r
colors_3 = px.colors.sequential.Reds_r
explode = tuple([0.015] * 50)
latitude = 0
longitude = 0
chart_theme = 'plotly_dark'
streamlit_theme = 'streamlit'
margin = {'r' : 20, 't' : 40, 'l' : 20, 'b' : 10}
cmap = 'rainbow'
title_x = 0
title_font_size = 18


# 07 CREATING DASHBOARD

# create highlighted indicator

col_11, col_12, col_13, col_14, col_15, col_16 = st.columns((1, 1, 1, 1, 1, 1))

with col_11:
  title = 'Total Customer'
  #st.subheader(title)
  fig = go.Figure(go.Indicator(
    mode = 'number+delta',
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = df['Satisfaction'].count(),
    number = {'valueformat' : ','},
  ))

  fig.update_layout(
    #paper_bgcolor = 'lightgray',
    height = 200,
    margin = margin,
    title = title,
    titlefont = dict(size = title_font_size),
    title_x = title_x,
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

chart_df_1 = df.groupby(by = ['Satisfaction'], as_index = False,)[['Gender']].count()
chart_df_1 = chart_df_1.rename(columns = {'Gender' : 'Customer'})

with col_12:
  title = 'Customer Satisfaction'
  #st.subheader(title)
  fig = px.pie(
    chart_df_1,
    values = 'Customer',
    names = 'Satisfaction',
    hole = 0.5,
    template = chart_theme,
    color_discrete_sequence = colors_1,
  )
  fig.update_traces(
    text = chart_df_1['Satisfaction'],
    textposition = 'inside',
    pull = explode,
  )
  fig.update_layout(
    height = 400,
    margin = margin,
    title = title,
    titlefont = dict(size = title_font_size),
    title_x = title_x,
    legend = dict(yanchor = 'top', y = 0, xanchor = 'left', x = 0),
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

chart_df_2 = df.groupby(by = ['Gender'], as_index = False,)[['Satisfaction']].count()
chart_df_2 = chart_df_2.rename(columns = {'Satisfaction' : 'Customer'})

with col_13:
  title = 'Customer by Gender'
  #st.subheader(title)
  fig = px.pie(
    chart_df_2,
    values = 'Customer',
    names = 'Gender',
    hole = 0.5,
    template = chart_theme,
    color_discrete_sequence = colors_1,
  )
  fig.update_traces(
    text = chart_df_2['Gender'],
    textposition = 'inside',
    pull = explode,
  )
  fig.update_layout(
    height = 400,
    margin = margin,
    title = title,
    titlefont = dict(size = title_font_size),
    title_x = title_x,
    legend = dict(yanchor = 'top', y = 0, xanchor = 'left', x = 0),
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)


chart_df_3 = df.groupby(by = ['Customer Type'], as_index = False,)[['Satisfaction']].count()
chart_df_3 = chart_df_3.rename(columns = {'Satisfaction' : 'Customer'})

with col_14:
  title = 'Customer by Customer Type'
  #st.subheader(title)
  fig = px.pie(
    chart_df_3,
    values = 'Customer',
    names = 'Customer Type',
    hole = 0.5,
    template = chart_theme,
    color_discrete_sequence = colors_1,
  )
  fig.update_traces(
    text = chart_df_3['Customer Type'],
    textposition = 'inside',
    pull = explode,
  )
  fig.update_layout(
    height = 400,
    margin = margin,
    title = title,
    titlefont = dict(size = title_font_size),
    title_x = title_x,
    legend = dict(yanchor = 'top', y = 0, xanchor = 'left', x = 0),
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

chart_df_4 = df.groupby(by = ['Type Of Travel'], as_index = False,)[['Satisfaction']].count()
chart_df_4 = chart_df_4.rename(columns = {'Satisfaction' : 'Customer'})

with col_15:
  title = 'Customer by Type Of Travel'
  #st.subheader(title)
  fig = px.pie(
    chart_df_4,
    values = 'Customer',
    names = 'Type Of Travel',
    hole = 0.5,
    template = chart_theme,
    color_discrete_sequence = colors_1,
  )
  fig.update_traces(
    text = chart_df_4['Type Of Travel'],
    textposition = 'inside',
    pull = explode,
  )
  fig.update_layout(
    height = 400,
    margin = margin,
    title = title,
    titlefont = dict(size = title_font_size),
    title_x = title_x,
    legend = dict(yanchor = 'top', y = 0, xanchor = 'left', x = 0),
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

chart_df_5 = df.groupby(by = ['Class'], as_index = False,)[['Satisfaction']].count()
chart_df_5 = chart_df_5.rename(columns = {'Satisfaction' : 'Customer'})

with col_16:
  title = 'Customer by Class'
  #st.subheader(title)
  fig = px.pie(
    chart_df_5,
    values = 'Customer',
    names = 'Class',
    hole = 0.5,
    template = chart_theme,
    color_discrete_sequence = colors_1,
  )
  fig.update_traces(
    text = chart_df_5['Class'],
    textposition = 'inside',
    pull = explode,
  )
  fig.update_layout(
    height = 400,
    margin = margin,
    title = title,
    titlefont = dict(size = title_font_size),
    title_x = title_x,
    legend = dict(yanchor = 'top', y = 0, xanchor = 'left', x = 0),
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

with col_11:
  title = 'Total Flight Distance (km)'
  #st.subheader(title)
  fig = go.Figure(go.Indicator(
    mode = 'number+delta',
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = df['Flight Distance'].sum(),
    number = {'valueformat' : ',.2s'},
  ))

  fig.update_layout(
    #paper_bgcolor = 'lightgray',
    height = 200,
    margin = margin,
    title = title,
    titlefont = dict(size = title_font_size),
    title_x = title_x,
    legend = dict(yanchor = 'top', y = 0, xanchor = 'left', x = 0),
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

col_21, col_22 = st.columns((1, 1))

with col_21:
  st.header('Satisfied Customer', divider = 'rainbow')

with col_22:
  st.header('Dissatisfied Customer', divider = 'rainbow')

col_31, col_32, col_33, col_34, col_35, col_36 = st.columns((1, 1, 1, 1, 1, 1))

with col_31:
  title = 'Satisfied Customer'
  #st.subheader(title)
  fig = go.Figure(go.Indicator(
    mode = 'number+delta',
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = sat_df['Satisfaction'].count(),
    number = {'valueformat' : ','},
  ))

  fig.update_layout(
    #paper_bgcolor = 'lightgray',
    height = 150,
    margin = margin,
    title = title,
    titlefont = dict(size = title_font_size),
    title_x = title_x,
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

chart_df_6 = sat_df.groupby(by = ['Gender'], as_index = False,)[['Satisfaction']].count()
chart_df_6 = chart_df_6.rename(columns = {'Satisfaction' : 'Customer'})

with col_32:
  title = 'Satisfied Customer by Gender'
  #st.subheader(title)
  fig = px.pie(
    chart_df_6,
    values = 'Customer',
    names = 'Gender',
    hole = 0.5,
    template = chart_theme,
    color_discrete_sequence = colors_2,
  )
  fig.update_traces(
    text = chart_df_6['Gender'],
    textposition = 'inside',
    pull = explode,
  )
  fig.update_layout(
    height = 300,
    margin = margin,
    title = title,
    titlefont = dict(size = title_font_size),
    title_x = title_x,
    legend = dict(yanchor = 'top', y = 0, xanchor = 'left', x = 0),
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

chart_df_7 = sat_df.groupby(by = ['Customer Type'], as_index = False,)[['Satisfaction']].count()
chart_df_7 = chart_df_7.rename(columns = {'Satisfaction' : 'Customer'})

with col_33:
  title = 'Satisfied Customer by Customer Type'
  #st.subheader(title)
  fig = px.pie(
    chart_df_7,
    values = 'Customer',
    names = 'Customer Type',
    hole = 0.5,
    template = chart_theme,
    color_discrete_sequence = colors_2,
  )
  fig.update_traces(
    text = chart_df_7['Customer Type'],
    textposition = 'inside',
    pull = explode,
  )
  fig.update_layout(
    height = 300,
    margin = margin,
    title = title,
    titlefont = dict(size = title_font_size),
    title_x = title_x,
    legend = dict(yanchor = 'top', y = 0, xanchor = 'left', x = 0),
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

with col_31:
  title = 'Total Flight Distance (km)'
  #st.subheader(title)
  fig = go.Figure(go.Indicator(
    mode = 'number+delta',
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = sat_df['Flight Distance'].sum(),
    number = {'valueformat' : ',.2s'},
  ))

  fig.update_layout(
    #paper_bgcolor = 'lightgray',
    height = 150,
    margin = margin,
    title = title,
    titlefont = dict(size = title_font_size),
    title_x = title_x,
    legend = dict(yanchor = 'top', y = 0, xanchor = 'left', x = 0),
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

with col_34:
  title = 'Dissatisfied Customer'
  #st.subheader(title)
  fig = go.Figure(go.Indicator(
    mode = 'number+delta',
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = dis_df['Satisfaction'].count(),
    number = {'valueformat' : ','},
  ))

  fig.update_layout(
    #paper_bgcolor = 'lightgray',
    height = 150,
    margin = margin,
    title = title,
    titlefont = dict(size = title_font_size),
    title_x = title_x,
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

chart_df_8 = dis_df.groupby(by = ['Gender'], as_index = False,)[['Satisfaction']].count()
chart_df_8 = chart_df_8.rename(columns = {'Satisfaction' : 'Customer'})

with col_35:
  title = 'Dissatisfied Customer by Gender'
  #st.subheader(title)
  fig = px.pie(
    chart_df_8,
    values = 'Customer',
    names = 'Gender',
    hole = 0.5,
    template = chart_theme,
    color_discrete_sequence = colors_3,
  )
  fig.update_traces(
    text = chart_df_8['Gender'],
    textposition = 'inside',
    pull = explode,
  )
  fig.update_layout(
    height = 300,
    margin = margin,
    title = title,
    titlefont = dict(size = title_font_size),
    title_x = title_x,
    legend = dict(yanchor = 'top', y = 0, xanchor = 'left', x = 0),
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

chart_df_9 = dis_df.groupby(by = ['Customer Type'], as_index = False,)[['Satisfaction']].count()
chart_df_9 = chart_df_9.rename(columns = {'Satisfaction' : 'Customer'})

with col_36:
  title = 'Dissatisfied Customer by Customer Type'
  #st.subheader(title)
  fig = px.pie(
    chart_df_9,
    values = 'Customer',
    names = 'Customer Type',
    hole = 0.5,
    template = chart_theme,
    color_discrete_sequence = colors_3,
  )
  fig.update_traces(
    text = chart_df_9['Customer Type'],
    textposition = 'inside',
    pull = explode,
  )
  fig.update_layout(
    height = 300,
    margin = margin,
    title = title,
    titlefont = dict(size = title_font_size),
    title_x = title_x,
    legend = dict(yanchor = 'top', y = 0, xanchor = 'left', x = 0),
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

with col_34:
  title = 'Total Flight Distance (km)'
  #st.subheader(title)
  fig = go.Figure(go.Indicator(
    mode = 'number+delta',
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = dis_df['Flight Distance'].sum(),
    number = {'valueformat' : ',.2s'},
  ))

  fig.update_layout(
    #paper_bgcolor = 'lightgray',
    height = 150,
    margin = margin,
    title = title,
    titlefont = dict(size = title_font_size),
    title_x = title_x,
    legend = dict(yanchor = 'top', y = 0, xanchor = 'left', x = 0),
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

col_41, col_42, col_43, col_44 = st.columns((1, 1, 1, 1))

chart_df_10 = sat_df.groupby(by = ['Type Of Travel'], as_index = False,)[['Satisfaction']].count()
chart_df_10 = chart_df_10.rename(columns = {'Satisfaction' : 'Customer'})

with col_41:
  title = 'Satisfied Customer by Type Of Travel'
  #st.subheader(title)
  fig = px.pie(
    chart_df_10,
    values = 'Customer',
    names = 'Type Of Travel',
    hole = 0.5,
    template = chart_theme,
    color_discrete_sequence = colors_2,
  )
  fig.update_traces(
    text = chart_df_10['Type Of Travel'],
    textposition = 'inside',
    pull = explode,
  )
  fig.update_layout(
    height = 300,
    margin = margin,
    title = title,
    titlefont = dict(size = title_font_size),
    title_x = title_x,
    legend = dict(yanchor = 'top', y = 0, xanchor = 'left', x = 0),
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

chart_df_11 = sat_df.groupby(by = ['Class'], as_index = False,)[['Satisfaction']].count()
chart_df_11 = chart_df_11.rename(columns = {'Satisfaction' : 'Customer'})

with col_42:
  title = 'Satisfied Customer by Class'
  #st.subheader(title)
  fig = px.pie(
    chart_df_11,
    values = 'Customer',
    names = 'Class',
    hole = 0.5,
    template = chart_theme,
    color_discrete_sequence = colors_2,
  )
  fig.update_traces(
    text = chart_df_11['Class'],
    textposition = 'inside',
    pull = explode,
  )
  fig.update_layout(
    height = 300,
    margin = margin,
    title = title,
    titlefont = dict(size = title_font_size),
    title_x = title_x,
    legend = dict(yanchor = 'top', y = 0, xanchor = 'left', x = 0),
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

chart_df_12 = dis_df.groupby(by = ['Type Of Travel'], as_index = False,)[['Satisfaction']].count()
chart_df_12 = chart_df_12.rename(columns = {'Satisfaction' : 'Customer'})

with col_43:
  title = 'Dissatisfied Customer by Type Of Travel'
  #st.subheader(title)
  fig = px.pie(
    chart_df_12,
    values = 'Customer',
    names = 'Type Of Travel',
    hole = 0.5,
    template = chart_theme,
    color_discrete_sequence = colors_3,
  )
  fig.update_traces(
    text = chart_df_12['Type Of Travel'],
    textposition = 'inside',
    pull = explode,
  )
  fig.update_layout(
    height = 300,
    margin = margin,
    title = title,
    titlefont = dict(size = title_font_size),
    title_x = title_x,
    legend = dict(yanchor = 'top', y = 0, xanchor = 'left', x = 0),
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

chart_df_13 = dis_df.groupby(by = ['Class'], as_index = False,)[['Satisfaction']].count()
chart_df_13 = chart_df_13.rename(columns = {'Satisfaction' : 'Customer'})

with col_44:
  title = 'Dissatisfied Customer by Class'
  #st.subheader(title)
  fig = px.pie(
    chart_df_13,
    values = 'Customer',
    names = 'Class',
    hole = 0.5,
    template = chart_theme,
    color_discrete_sequence = colors_3,
  )
  fig.update_traces(
    text = chart_df_13['Class'],
    textposition = 'inside',
    pull = explode,
  )
  fig.update_layout(
    height = 300,
    margin = margin,
    title = title,
    titlefont = dict(size = title_font_size),
    title_x = title_x,
    legend = dict(yanchor = 'top', y = 0, xanchor = 'left', x = 0),
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

col_51, col_52 = st.columns((1, 1))

chart_df_14 = df.groupby(by = 'Satisfaction', as_index = False,)[['Seat Comfort',
       'Departure/Arrival Time Convenient', 'Food And Drink', 'Gate Location',
       'Inflight Wifi Service', 'Inflight Entertainment', 'Online Support',
       'Ease Of Online Booking', 'On-Board Service', 'Leg Room Service',
       'Baggage Handling', 'Checkin Service', 'Cleanliness', 'Online Boarding']].mean()

with col_51:
  title = 'Satisfied Customer Review'
  fig = go.Figure()
  fig.add_trace(go.Scatterpolar(
      r = chart_df_14.loc[1].to_list()[1:],
      theta = chart_df_14.columns[1:],
      fill = 'toself',
      name = 'Satisfied',
      fillcolor = colors_2[1],
      opacity = 0.6,
      line = dict(color = colors_2[2]),
  ))
  fig.update_layout(
    polar = dict(
      radialaxis = dict(
        visible = True,
        range = [0, 5]
      )),
    showlegend = False
  )
  fig.update_layout(
    height = 500,
    margin = margin,
    title = title,
    titlefont = dict(size = title_font_size),
    title_x = title_x,
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

with col_52:
  title = 'Dissatisfied Customer Review'
  fig = go.Figure()
  fig.add_trace(go.Scatterpolar(
      r = chart_df_14.loc[0].to_list()[1:],
      theta = chart_df_14.columns[1:],
      fill = 'toself',
      name = 'Dissatisfied',
      fillcolor = colors_3[1],
      opacity = 0.6,
      line = dict(color = colors_3[2]),
  ))
  fig.update_layout(
    polar = dict(
      radialaxis = dict(
        visible = True,
        range = [0, 5]
      )),
    showlegend = False
  )
  fig.update_layout(
    height = 500,
    margin = margin,
    title = title,
    titlefont = dict(size = title_font_size),
    title_x = title_x,
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

with col_51:
  title = 'Satisfied CustomerAge and Flight Distance Distribution'
  fig_1 = px.scatter(
    sat_df,
    x = 'Age',
    y = 'Flight Distance',
    #color = 'Type Of Travel',
    height = 800,
    template = chart_theme,
    color_discrete_sequence = colors_2,
    trendline = 'ols',
    marginal_x = 'histogram',
    marginal_y = 'box',
  )
  fig_1.update_layout(
    title = title,
    titlefont = dict(size = title_font_size),
    xaxis = dict(title = 'Age', titlefont = dict(size = 14)),
    yaxis = dict(title = 'Flight Distance (km)', titlefont = dict(size = 14), tickformat = ','),
    title_x = title_x,
  )
  st.plotly_chart(fig_1, use_container_width = True, theme = streamlit_theme)

with col_52:
  title = 'Dissatisfied CustomerAge and Flight Distance Distribution'
  fig_1 = px.scatter(
    dis_df,
    x = 'Age',
    y = 'Flight Distance',
    #color = 'Type Of Travel',
    height = 800,
    template = chart_theme,
    color_discrete_sequence = colors_3,
    trendline = 'ols',
    marginal_x = 'histogram',
    marginal_y = 'box',
  )
  fig_1.update_layout(
    title = title,
    titlefont = dict(size = title_font_size),
    xaxis = dict(title = 'Age', titlefont = dict(size = 14)),
    yaxis = dict(title = 'Flight Distance (km)', titlefont = dict(size = 14), tickformat = ','),
    title_x = title_x,
  )
  st.plotly_chart(fig_1, use_container_width = True, theme = streamlit_theme)
