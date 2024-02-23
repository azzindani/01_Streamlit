
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
  page_title = 'Fatalities',
  #page_icon = ':bar_chart:',
  layout = 'wide',
)


# 01 CREATING DASHBOARD TITLE

st.title(':hospital: Palestinian & Israeli Fatalities based on Recorded Data')
st.markdown('<style>div,block-container{padding-top:0rem;}<style>', unsafe_allow_html = True)


# 02 IMPORTING DATASET

dataset_path = 'https://raw.githubusercontent.com/azzindani/00_Data_Source/main/Palestine_Israel_Fatalities_2000-2023.csv'
df = pd.read_csv(dataset_path)

df['gender'] = df['gender'].replace({'M' : 'Male', 'F' : 'Female'})

gdf = gpd.read_file('https://raw.githubusercontent.com/sepans/palestine_geodata/master/palestine.geo.json')


# 03 SETUP TEMPLATE & THEME

colors_1 = px.colors.sequential.Jet
colors_2 = px.colors.sequential.Jet
explode = tuple([0.015] * 50)
latitude = 0
longitude = 0
chart_theme = 'plotly_dark'
streamlit_theme = 'streamlit'
margin = {'r' : 20, 't' : 40, 'l' : 20, 'b' : 10}
cmap = 'jet'
title_x = 0
title_font_size = 18


# 04 CREATING DATE PICKER

col_1, col_2 = st.columns((2))
df['date_of_event'] = pd.to_datetime(df['date_of_event'])

# Getting min & max date
start_date = pd.to_datetime(df['date_of_event']).min()
end_date = pd.to_datetime(df['date_of_event']).max()

with col_1:
  date_1 = pd.to_datetime(st.date_input('Start Date', start_date))

with col_2:
  date_2 = pd.to_datetime(st.date_input('End Date', end_date))

df = df[(df['date_of_event'] >= date_1) & (df['date_of_event'] <= date_2)] #'''


# 05 CREATING SIDEBAR FILTER


# 06 CREATING DATASET FILTER LOGIC


# 07 CREATING DASHBOARD

# create highlighted indicator

col_11, col_12, col_13, col_14 = st.columns((1, 1, 1, 1))

chart_df_1 = df.groupby(by = ['citizenship'], as_index = False,)[['name']].count()
chart_df_1 = chart_df_1.rename(columns = {'citizenship' : 'Citizenship', 'name' : 'Deaths'})
chart_df_1 = chart_df_1[chart_df_1['Citizenship'] == 'Palestinian']

with col_11:
  title = 'Palestinian Deaths'
  #st.subheader(title)
  fig = go.Figure(go.Indicator(
    mode = 'number+delta',
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = chart_df_1['Deaths'].sum(),
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

chart_df_2 = df.groupby(by = ['citizenship'], as_index = False,)[['name']].count()
chart_df_2 = chart_df_2.rename(columns = {'citizenship' : 'Citizenship', 'name' : 'Deaths'})

with col_12:
  title = 'Death Ratio by Citizenship'
  #st.subheader(title)
  fig = px.pie(
    chart_df_2,
    values = 'Deaths',
    names = 'Citizenship',
    hole = 0.5,
    template = chart_theme,
    color_discrete_sequence = colors_1,
  )
  fig.update_traces(
    text = chart_df_2['Citizenship'],
    textposition = 'inside',
    pull = explode,
  )
  fig.update_layout(
    height = 400,
    margin = margin,
    title = title,
    titlefont = dict(size = title_font_size),
    title_x = title_x,
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

chart_df_3 = df.groupby(by = ['gender'], as_index = False,)[['name']].count()
chart_df_3 = chart_df_3.rename(columns = {'gender' : 'Gender', 'name' : 'Deaths'})

with col_13:
  title = 'Death Ratio by Gender'
  #st.subheader(title)
  fig = px.pie(
    chart_df_3,
    values = 'Deaths',
    names = 'Gender',
    hole = 0.5,
    template = chart_theme,
    color_discrete_sequence = colors_1,
  )
  fig.update_traces(
    text = chart_df_3['Gender'],
    textposition = 'inside',
    pull = explode,
  )
  fig.update_layout(
    height = 400,
    margin = margin,
    title = title,
    titlefont = dict(size = title_font_size),
    title_x = title_x,
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

chart_df_4 = df.groupby(by = ['killed_by'], as_index = False,)[['name']].count()
chart_df_4 = chart_df_4.rename(columns = {'killed_by' : 'Killed by', 'name' : 'Deaths'})

with col_14:
  title = 'Deaths Killed by'
  #st.subheader(title)
  fig = px.bar(
    chart_df_4,
    y = 'Killed by',
    x = 'Deaths',
    template = chart_theme,
    color_discrete_sequence = colors_2,
    title = title,
    text_auto = ',.0f',
  )
  fig.update_layout(
      height = 400,
      margin = margin,
      titlefont = dict(size = title_font_size),
      title_x = title_x,
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

chart_df_5 = df.groupby(by = ['citizenship'], as_index = False,)[['name']].count()
chart_df_5 = chart_df_5.rename(columns = {'citizenship' : 'Citizenship', 'name' : 'Deaths'})
chart_df_5 = chart_df_5[chart_df_5['Citizenship'] == 'Israeli']

with col_11:
  title = 'Israeli Deaths'
  #st.subheader(title)
  fig = go.Figure(go.Indicator(
    mode = 'number+delta',
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = chart_df_5['Deaths'].sum(),
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

col_21, col_22, col_23 = st.columns((1, 1, 2))

chart_df_6 = df.groupby(by = ['ammunition'], as_index = False,)[['name']].count()
chart_df_6 = chart_df_6.rename(columns = {'ammunition' : 'Ammunition', 'name' : 'Deaths'})

with col_21:
  title = 'Death Ratio by Ammunition'
  #st.subheader(title)
  fig = px.pie(
    chart_df_6,
    values = 'Deaths',
    names = 'Ammunition',
    hole = 0.5,
    template = chart_theme,
    color_discrete_sequence = colors_1,
  )
  fig.update_traces(
    text = chart_df_6['Ammunition'],
    textposition = 'inside',
    pull = explode,
  )
  fig.update_layout(
    height = 500,
    margin = margin,
    title = title,
    titlefont = dict(size = title_font_size),
    title_x = title_x,
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

  with st.expander('View Data'):
    st.write(chart_df_6.style.background_gradient(cmap = cmap))
    csv = chart_df_6.to_csv(index = False).encode('utf-8')
    st.download_button('Download Data', data = csv, file_name = title + '.csv', mime = 'text/csv', help = 'Click here to download as CSV file')

chart_df_7 = df.groupby(by = ['type_of_injury'], as_index = False,)[['name']].count()
chart_df_7 = chart_df_7.rename(columns = {'type_of_injury' : 'Type of Injury', 'name' : 'Deaths'})

with col_22:
  title = 'Death Ratio by Type of Injury'
  #st.subheader(title)
  fig = px.pie(
    chart_df_7,
    values = 'Deaths',
    names = 'Type of Injury',
    hole = 0.5,
    template = chart_theme,
    color_discrete_sequence = colors_1,
  )
  fig.update_traces(
    text = chart_df_7['Type of Injury'],
    textposition = 'inside',
    pull = explode,
  )
  fig.update_layout(
    height = 500,
    margin = margin,
    title = title,
    titlefont = dict(size = title_font_size),
    title_x = title_x,
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

  with st.expander('View Data'):
    st.write(chart_df_7.style.background_gradient(cmap = cmap))
    csv = chart_df_7.to_csv(index = False).encode('utf-8')
    st.download_button('Download Data', data = csv, file_name = title + '.csv', mime = 'text/csv', help = 'Click here to download as CSV file')

chart_df_8 = df.groupby(by = ['event_location_district'], as_index = False,)[['name']].count()
chart_df_8 = chart_df_8.rename(columns = {'event_location_district' : 'Event Location District', 'name' : 'Deaths'})

with col_23:
  title = 'Deaths by District'
  #st.subheader(title)
  fig = px.bar(
    chart_df_8,
    y = 'Event Location District',
    x = 'Deaths',
    template = chart_theme,
    color_discrete_sequence = colors_2,
    title = title,
    text_auto = ',.0f',
  )
  fig.update_layout(
      height = 500,
      margin = margin,
      titlefont = dict(size = title_font_size),
      title_x = title_x,
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

  with st.expander('View Data'):
    st.write(chart_df_8.style.background_gradient(cmap = cmap))
    csv = chart_df_8.to_csv(index = False).encode('utf-8')
    st.download_button('Download Data', data = csv, file_name = title + '.csv', mime = 'text/csv', help = 'Click here to download as CSV file')

col_31, col_32 = st.columns((1, 1))

# create time series chart

df['Month & Year'] = df['date_of_event'].dt.to_period('Y')
linechart = pd.DataFrame(df.groupby(['Month & Year', 'citizenship'])[['name']].count()).reset_index()
linechart = linechart.rename(columns = {'citizenship' : 'Citizenship', 'name' : 'Deaths'})
linechart['Month & Year'] = linechart['Month & Year'].astype(str)
linechart_1 = linechart[linechart['Citizenship'] == 'Palestinian']
linechart_2 = linechart[linechart['Citizenship'] == 'Israeli']

with col_31:
  title = 'Monthly Fatalities of Palestinian & Israeli'
  #st.subheader(title)
  fig_1 = go.Figure()
  fig_1.add_trace(go.Scatter(
    x = linechart_1['Month & Year'],
    y = linechart_1['Deaths'],
    mode = 'lines+markers',
    name = 'Palestinian',
    marker = {'color': colors_2[0]},
  ))
  fig_1.add_trace(go.Bar(
    x = linechart_2['Month & Year'],
    y = linechart_2['Deaths'],
    name = 'Israeli',
    marker = {'color': colors_2[3]},
  ))
  fig_1.update_layout(
    hovermode = 'x',
    height = 500,
    margin = margin,
    title = title,
    titlefont = dict(size = title_font_size),
    title_x = title_x,
  )
  st.plotly_chart(fig_1, use_container_width = True, theme = streamlit_theme)

  with st.expander('View Data'):
    st.write(linechart.style.background_gradient(cmap = cmap))
    csv = linechart.to_csv(index = False).encode('utf-8')
    st.download_button('Download Data', data = csv, file_name = title + '.csv', mime = 'text/csv', help = 'Click here to download as CSV file')

df['age'] = df['age'].fillna(0)
df['age'] = df['age'].astype('int')
chart_df_9 = df.groupby(by = ['age', 'killed_by'], as_index = False,)[['name']].count()
chart_df_9 = chart_df_9.rename(columns = {'age' : 'Age', 'killed_by' : 'Killed by', 'name' : 'Deaths'})

with col_32:
  title = 'Number of Deaths by Age'
  fig_3 = px.scatter(
    chart_df_9,
    x = 'Age',
    y = 'Deaths',
    color = 'Killed by',
    height = 500,
    template = chart_theme,
    color_discrete_sequence = colors_1,
  )
  fig_3.update_layout(
    title = title,
    titlefont = dict(size = title_font_size),
    xaxis = dict(title = 'Age', titlefont = dict(size = 14)),
    yaxis = dict(title = 'Deaths', titlefont = dict(size = 14)),
    title_x = title_x,
  )
  st.plotly_chart(fig_3, use_container_width = True, theme = streamlit_theme)

  with st.expander('View Data'):
    st.write(chart_df_9.style.background_gradient(cmap = cmap))
    csv = chart_df_9.to_csv(index = False).encode('utf-8')
    st.download_button('Download Data', data = csv, file_name = title + '.csv', mime = 'text/csv', help = 'Click here to download as CSV file')

# Download original sample dataset

with st.expander('Sample Data'):
  st.write(df.iloc[:500].style.background_gradient(cmap = cmap))
  csv = df.to_csv(index = False).encode('utf-8')
  st.download_button('Download Data', data = csv, file_name = 'Data.csv', mime = 'text/csv')
