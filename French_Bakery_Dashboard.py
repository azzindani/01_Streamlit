
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
  page_title = 'French Bakery Sales',
  page_icon = ':bar_chart:',
  layout = 'wide',
)


# 01 CREATING DASHBOARD TITLE

st.title(':bar_chart: French Bakery Sales Dashboard')
st.markdown('<style>div,block-container{padding-top:0rem;}<style>', unsafe_allow_html = True)


# 02 IMPORTING DATASET

dataset_path = 'https://raw.githubusercontent.com/azzindani/00_Data_Source/main/French_Bakery_Sales.csv'
df = pd.read_csv(dataset_path)

df['unit_price'] = df['unit_price'].str.replace(' €', '')
df['unit_price'] = df['unit_price'].str.replace(',', '.')
df['unit_price'] = df['unit_price'].astype('float')

df['sales'] = df['Quantity'] * df['unit_price']

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
    pass #'''


# 03 SETUP TEMPLATE & THEME

colors_1 = px.colors.sequential.BuPu_r
colors_2 = px.colors.sequential.BuPu_r
explode = tuple([0.015] * 50)
latitude = 0
longitude = 0
chart_theme = 'Darkmint'
streamlit_theme = 'streamlit'
margin = {'r' : 20, 't' : 40, 'l' : 20, 'b' : 10}
cmap = 'BuPu_r'
title_x = 0
title_font_size = 18


# 04 CREATING DATE PICKER

col_1, col_2 = st.columns((2))
df['Date'] = pd.to_datetime(df['Date'])

# Getting min & max date
start_date = pd.to_datetime(df['Date']).min()
end_date = pd.to_datetime(df['Date']).max()

with col_1:
  date_1 = pd.to_datetime(st.date_input('Start Date', start_date))

with col_2:
  date_2 = pd.to_datetime(st.date_input('End Date', end_date))

df = df[(df['Date'] >= date_1) & (df['Date'] <= date_2)] #'''


# 05 CREATING SIDEBAR FILTER


# 06 CREATING DATASET FILTER LOGIC


# 07 CREATING DASHBOARD

# create highlighted indicator

col_11, col_12 = st.columns((1, 4))

with col_11:
  title = 'Total Sales'
  #st.subheader(title)
  fig = go.Figure(go.Indicator(
    mode = 'number+delta',
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = df['Sales'].sum(),
    number = {'prefix' : '€'},
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

chart_df_1 = df.groupby(by = ['Article'], as_index = False)[['Sales', 'Quantity']].sum()
chart_df_1 = chart_df_1.sort_values('Sales', ascending = True)
chart_df_1 = chart_df_1[:20]

with col_12:
  title = 'Sales Value (EUR) by Top 20 Product'
  fig = go.Figure()
  fig.add_trace(go.Bar(
    x = chart_df_1['Article'],
    y = chart_df_1['Sales'],
    name = 'Sales',
    marker = {'color': colors_2[0]},
  ))
  fig.add_trace(go.Scatter(
    x = chart_df_1['Article'],
    y = chart_df_1['Quantity'],
    mode = 'lines+markers',
    name = 'Quantity',
    marker = {'color': colors_2[3]},
  ))
  fig.update_layout(
    hovermode = 'x',
    height = 400,
    margin = margin,
    title = title,
    titlefont = dict(size = title_font_size),
    title_x = title_x,
  )
  fig.show()

  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

with col_11:
  title = 'Product Sold'
  #st.subheader(title)
  fig = go.Figure(go.Indicator(
    mode = 'number+delta',
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = df['Quantity'].sum(),
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

col_21, col_22 = st.columns((4, 1))

# create time series chart

df['Month & Year'] = df['Date'].dt.to_period('W')
linechart = pd.DataFrame(df.groupby(df['Month & Year'])[['Sales']].sum()).reset_index()
linechart['Month & Year'] = linechart['Month & Year'].astype(str)

with col_21:
  title = 'Weekly Sales Data'
  #st.subheader(title)
  fig_1 = go.Figure()
  fig_1.add_trace(go.Scatter(
    x = linechart['Month & Year'],
    y = linechart['Sales'],
    mode = 'lines+markers',
    name = 'Sales',
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

# Download original sample dataset

with col_22:
  title = '<p style = "font-size : 18px; font-weight : bold;">Sample Data</p>'
  st.markdown(title, unsafe_allow_html = True)
  st.write(df.iloc[:500, 1:20:2].style.background_gradient(cmap = cmap))
  csv = df.to_csv(index = False).encode('utf-8')
  st.download_button('Download Data', data = csv, file_name = 'Data.csv', mime = 'text/csv')
