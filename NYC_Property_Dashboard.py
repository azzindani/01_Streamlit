
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
  page_title = 'NYC Property',
  page_icon = ':bar_chart:',
  layout = 'wide',
)


# 01 CREATING DASHBOARD TITLE

st.title(':bar_chart: New York City Property Dashboard')
st.markdown('<style>div,block-container{padding-top:0rem;}<style>', unsafe_allow_html = True)


# 02 IMPORTING DATASET

dataset_path = 'https://raw.githubusercontent.com/azzindani/00_Data_Source/main/Cleaned_NYC_Property_Sales.csv'
df = pd.read_csv(dataset_path, encoding = 'ISO-8859-1')
df['Zip Code'] = df['Zip Code'].astype('str')

gdf = gpd.read_file('https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/ny_new_york_zip_codes_geo.min.json')
gdf = gdf.rename(columns = {'ZCTA5CE10' : 'Zip Code'})
gdf['Zip Code'] = gdf['Zip Code'].astype('str')
gdf = gdf[['Zip Code', 'geometry']]


# 03 SETUP TEMPLATE & THEME

colors = px.colors.sequential.Magma_r
colors_2 = px.colors.sequential.Magma
explode = tuple([0.015] * 50)
latitude = 40.730610
longitude = -73.935242
chart_theme = 'plotly_dark'
streamlit_theme = 'streamlit'
margin = {'r' : 20, 't' : 40, 'l' : 20, 'b' : 10}
cmap = 'magma_r'
title_x = 0
title_font_size = 18


# 04 CREATING DATE PICKER

col_1, col_2 = st.columns((2))
df['Sale Date'] = pd.to_datetime(df['Sale Date'])

# Getting min & max date
start_date = pd.to_datetime(df['Sale Date']).min()
end_date = pd.to_datetime(df['Sale Date']).max()

with col_1:
  date_1 = pd.to_datetime(st.date_input('Start Date', start_date))

with col_2:
  date_2 = pd.to_datetime(st.date_input('End Date', end_date))

df = df[(df['Sale Date'] >= date_1) & (df['Sale Date'] <= date_2)] #'''


# 05 CREATING SIDEBAR FILTER

st.sidebar.header('Choose your Filter: ')

# Create borough sidebar

categories = [
  'Borough',
  'Tax Class At Present',
  'Building Class Category',
  'Top Building Class Category'
]

category = st.sidebar.selectbox('Select Category', categories)

prices = [
  'Sale Price',
  'Price / Sqft'
]

price = st.sidebar.selectbox('Select Price', prices)

lands = [
  'Land Square Feet',
  'Gross Square Feet'
]

land = st.sidebar.selectbox('Select Land', lands)

filtered_df = df[['Zip Code', 'Sale Date', 'Year Built', category, price, land]]

# 07 CREATING DASHBOARD

# create highlighted indicator

col_11, col_12, col_13 = st.columns((1, 1, 2))

with col_11:
  title = 'Sales Value'
  #st.subheader(title)
  fig = go.Figure(go.Indicator(
    mode = 'number+delta',
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = df['Sale Price'].sum(),
    number = {'prefix' : '$'},
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

with col_12:
  title = 'Property Sold'
  #st.subheader(title)
  fig = go.Figure(go.Indicator(
    mode = 'number+delta',
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = df['Sale Price'].count(),
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

# create geospatial chart

map_df = filtered_df.groupby(['Zip Code'])[price].mean()
map_df = map_df.reset_index()
map_df = map_df.rename(columns = {price : 'Average ' + price + ' (USD)'})
map_df = gdf.merge(map_df, on = 'Zip Code')

var_label = 'Zip Code'
var_number = 'Average ' + price + ' (USD)'

map_df = map_df.set_index(var_label)

with col_13:
  title = 'Geospatial Sales Data'
  fig = px.choropleth_mapbox(
      data_frame = map_df,
      geojson = map_df.geometry,
      locations = map_df.index,
      color = var_number,
      color_continuous_scale = colors,
      #range_color = (0, 10),
      opacity = 0.5,
      center = {'lat' : latitude, 'lon' : longitude},
      mapbox_style = 'carto-positron',
      zoom = 9,
  )

  fig.update_geos(
      fitbounds = 'locations',
      visible = False,
  )
  fig.update_layout(
      height = 600,
      margin = margin,
      title = title,
      titlefont = dict(size = title_font_size),
      title_x = title_x,
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

# create bar chart

chart_df_1 = df.groupby(by = category, as_index = False,)[['Sale Price']].sum()
chart_df_1 = chart_df_1.rename(columns = {'Sale Price' : 'Sales (USD)'})

with col_11:
  title = 'Sales Value by ' + category
  fig = px.bar(
    chart_df_1.sort_values(by = 'Sales (USD)', ascending = True),
    y = category,
    x = 'Sales (USD)',
    title = title,
    color_discrete_sequence = colors[1:],
    text_auto = ',',
  )

  fig.update_traces(
      textfont_size = 12,
      textangle = 0,
      textposition = 'inside',
      cliponaxis = False
  )

  fig.update_xaxes(showspikes = True)
  fig.update_yaxes(showspikes = True)
  fig.update_layout(
    height = 300,
    margin = margin,
    title = title,
    titlefont = dict(size = title_font_size),
    title_x = title_x,
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

  with st.expander('View Data'):
    st.write(chart_df_1.style.background_gradient(cmap = cmap))
    csv = chart_df_1.to_csv(index = False).encode('utf-8')
    st.download_button('Download Data', data = csv, file_name = title + '.csv', mime = 'text/csv', help = 'Click here to download as CSV file')

chart_df_2 = df.groupby(by = category, as_index = False,)[['Sale Price']].count()
chart_df_2 = chart_df_2.rename(columns = {'Sale Price' : 'Qty'})

with col_12:
  title = 'Property Sold by ' + category
  fig = px.bar(
    chart_df_2.sort_values(by = 'Qty', ascending = True),
    y = category,
    x = 'Qty',
    title = title,
    color_discrete_sequence = colors[1:],
    text_auto = ',',
  )

  fig.update_traces(
      textfont_size = 12,
      textangle = 0,
      textposition = 'inside',
      cliponaxis = False
  )

  fig.update_xaxes(showspikes = True)
  fig.update_yaxes(showspikes = True)
  fig.update_layout(
    height = 300,
    margin = margin,
    title = title,
    titlefont = dict(size = title_font_size),
    title_x = title_x,
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

  with st.expander('View Data'):
    st.write(chart_df_2.style.background_gradient(cmap = cmap))
    csv = chart_df_2.to_csv(index = False).encode('utf-8')
    st.download_button('Download Data', data = csv, file_name = title + '.csv', mime = 'text/csv', help = 'Click here to download as CSV file')

col_21, col_22, col_23 = st.columns((1, 1, 1))

chart_df_3 = df.groupby(by = category, as_index = False,)[['Sale Price']].sum()

with col_21:
  title = 'Sales Outlook by ' + category
  fig = px.pie(
    chart_df_3,
    values = 'Sale Price',
    names = category,
    hole = 0.5,
    template = chart_theme,
    color_discrete_sequence = colors,
  )
  fig.update_traces(
    text = chart_df_3[category],
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

  with st.expander('View Data'):
    st.write(chart_df_3.style.background_gradient(cmap = cmap))
    csv = chart_df_3.to_csv(index = False).encode('utf-8')
    st.download_button('Download Data', data = csv, file_name = title + '.csv', mime = 'text/csv', help = 'Click here to download as CSV file')

filtered_df = filtered_df.sort_values(by = 'Sale Date')
filtered_df['Month & Year'] = filtered_df['Sale Date'].dt.to_period('M')
chart_df_4 = pd.DataFrame(filtered_df.groupby([filtered_df['Month & Year'], category])[[price]].mean()).reset_index()
chart_df_4['Month & Year'] = chart_df_4['Month & Year'].astype(str)
chart_df_4 = chart_df_4.rename(columns = {price : 'Average ' + price + ' (USD)'})

with col_22:
  title = 'Average ' + price + ' by ' + category
  fig = px.line(
    chart_df_4.sort_values(by = 'Average ' + price + ' (USD)', ascending = True),
    x = 'Month & Year',
    y = 'Average ' + price + ' (USD)',
    color = category,
    color_discrete_sequence = colors[1:],
  )

  fig.update_traces(
      textposition = 'bottom right'
  )

  fig.update_traces(mode = 'markers+lines', hovertemplate = None)
  fig.update_layout(hovermode = 'x')

  fig.update_xaxes(showspikes = True)
  fig.update_yaxes(showspikes = True)
  fig.update_layout(
    height = 400,
    margin = margin,
    title = title,
    titlefont = dict(size = title_font_size),
    title_x = title_x,
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

  with st.expander('View Data'):
    st.write(chart_df_4.style.background_gradient(cmap = cmap))
    csv = chart_df_4.to_csv(index = False).encode('utf-8')
    st.download_button('Download Data', data = csv, file_name = title + '.csv', mime = 'text/csv', help = 'Click here to download as CSV file')

with col_23:
  title = 'Average ' + price + ' by ' + category
  fig = px.bar(
    chart_df_4,
    x = 'Month & Year',
    y = 'Average ' + price + ' (USD)',
    color = category,
    title = title,
    color_discrete_sequence = colors[1:],
    text_auto = '.2s',
  )

  fig.update_traces(
      textfont_size = 12,
      textangle = 0,
      textposition = 'outside',
      cliponaxis = False
  )

  fig.update_xaxes(showspikes = True)
  fig.update_yaxes(showspikes = True)
  fig.update_layout(
    height = 400,
    margin = margin,
    title = title,
    titlefont = dict(size = title_font_size),
    title_x = title_x,
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

col_31, col_32 = st.columns((2, 1))

chart_df_5 = filtered_df[['Year Built', category, price, land]]

with col_31:
  title = 'Relationship between ' + price + ' and ' + land + ' using Scatter Plot'
  fig = px.scatter(
    chart_df_5,
    x = price,
    y = land,
    color = category,
    height = 400,
    template = chart_theme,
    color_discrete_sequence = colors,
  )
  fig.update_layout(
    title = title,
    titlefont = dict(size = title_font_size),
    xaxis = dict(title = price, titlefont = dict(size = 14), tickformat = '.2s'),
    yaxis = dict(title = land, titlefont = dict(size = 14)),
    title_x = title_x,
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

with col_32:
  title = '<p style = "font-size : 18px; font-weight : bold;">Month wise Category Table Quantity Summary</p>'
  st.markdown(title, unsafe_allow_html = True)
  filtered_df['month'] = filtered_df['Sale Date'].dt.month_name()
  filtered_df = filtered_df.sort_values(by = 'Sale Date')
  category_year = pd.pivot_table(data = filtered_df, values = price, index = category, columns = 'month')
  category_year = category_year.fillna(0)
  category_year = category_year.astype(int)
  category_year = category_year[[
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December'
  ]]
  st.write(category_year.style.background_gradient(cmap = cmap))
  csv = category_year.to_csv(index = False).encode('utf-8')
  st.download_button('Download Data', data = csv, file_name = title + '.csv', mime = 'text/csv', help = 'Click here to download as CSV file')

title = 'Relationship between ' + price + ' and Year Built using Scatter Plot'
fig_1 = px.scatter(
  chart_df_5,
  x = price,
  y = 'Year Built',
  color = category,
  height = 600,
  template = chart_theme,
  color_discrete_sequence = colors_2,
  trendline = 'ols',
  marginal_x = 'histogram',
  marginal_y = 'box',
)
fig_1.update_layout(
  title = title,
  titlefont = dict(size = title_font_size),
  xaxis = dict(title = price, titlefont = dict(size = 14), tickformat = '.2s'),
  yaxis = dict(title = 'Year Built', titlefont = dict(size = 14)),
  title_x = title_x,
)
st.plotly_chart(fig_1, use_container_width = True, theme = streamlit_theme)

# Download original sample dataset

with st.expander('Sample Data'):
  df = df.fillna(0)
  for x in df.columns:
    if df[x].dtypes == 'float64':
      try:
        df[x] = df[x].astype(int)
      except:
        pass
  st.write(df.iloc[:500, 1:20:2].style.background_gradient(cmap = cmap))
  csv = df.to_csv(index = False).encode('utf-8')
  st.download_button('Download Data', data = csv, file_name = 'Data.csv', mime = 'text/csv')
