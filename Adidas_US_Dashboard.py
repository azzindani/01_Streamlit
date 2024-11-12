
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
  page_title = 'Adidas US',
  page_icon = ':bar_chart:',
  layout = 'wide',
)


# 01 CREATING DASHBOARD TITLE

st.title(':bar_chart: Adidas US Sales Dashboard')
st.markdown('<style>div,block-container{padding-top:0rem;}<style>', unsafe_allow_html = True)


# 02 IMPORTING DATASET

dataset_path = 'https://raw.githubusercontent.com/azzindani/00_Data_Source/main/Adidas_US_Sales.csv'
df = pd.read_csv(dataset_path, encoding = 'ISO-8859-1')

gdf = gpd.read_file('https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json')
gdf = gdf.rename(columns = {'name' : 'State'})
gdf = gdf[['State', 'geometry']]


# 03 SETUP TEMPLATE & THEME

colors_1 = px.colors.sequential.Aggrnyl_r
colors_2 = px.colors.sequential.Magma
explode = tuple([0.015] * 50)
latitude = 57
longitude = -113
chart_theme = 'plotly_dark'
streamlit_theme = 'streamlit'
margin = {'r' : 20, 't' : 40, 'l' : 20, 'b' : 10}
cmap = 'YlGn'
title_x = 0
title_font_size = 18


# 04 CREATING DATE PICKER

col_1, col_2 = st.columns((2))
df['Invoice Date'] = pd.to_datetime(df['Invoice Date'])

# Getting min & max date
start_date = pd.to_datetime(df['Invoice Date']).min()
end_date = pd.to_datetime(df['Invoice Date']).max()

with col_1:
  date_1 = pd.to_datetime(st.date_input('Start Date', start_date))

with col_2:
  date_2 = pd.to_datetime(st.date_input('End Date', end_date))

df = df[(df['Invoice Date'] >= date_1) & (df['Invoice Date'] <= date_2)] #'''


# 05 CREATING SIDEBAR FILTER

st.sidebar.header('Choose your Filter: ')

# Create region sidebar
region = st.sidebar.multiselect('Select Region', df['Region'].unique())

if not region:
  df_2 = df.copy()
else:
  df_2 = df[df['Region'].isin(region)]

# Create state sidebar
state = st.sidebar.multiselect('Select State', df_2['State'].unique())


# 06 CREATING DATASET FILTER LOGIC

# Filter the data based on region, state

# None filter
if not region and not state:
  filtered_df = df

# Single filter
elif not state:
  filtered_df = df[df['Region'].isin(region)]

elif not region:
  filtered_df = df[df['State'].isin(state)]

else:
  filtered_df = df_2[df_2['Region'].isin(region) & df_2['State'].isin(state)]


# 07 CREATING DASHBOARD

# create highlighted indicator

col_11, col_12, col_13 = st.columns((1, 1, 3))

with col_11:
  title = 'Sales Value'
  #st.subheader(title)
  fig = go.Figure(go.Indicator(
    mode = 'number+delta',
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = filtered_df['Total Sales'].sum(),
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
  title = 'Unit Sold'
  #st.subheader(title)
  fig = go.Figure(go.Indicator(
    mode = 'number+delta',
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = filtered_df['Units Sold'].sum(),
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

map_df = df.groupby(['State'])['Total Sales'].sum()
map_df = map_df.reset_index()
map_df = map_df.rename(columns = {'Total Sales' : 'Sales Value (USD)'})
map_df = gdf.merge(map_df, on = 'State')

var_label = 'State'
var_number = 'Sales Value (USD)'

map_df = map_df.set_index(var_label)

with col_13:
  title = 'Geospatial Sales Data'
  fig = px.choropleth_mapbox(
      data_frame = map_df,
      geojson = map_df.geometry,
      locations = map_df.index,
      color = var_number,
      color_continuous_scale = colors_1,
      #range_color = (0, 10),
      opacity = 0.5,
      center = {'lat' : latitude, 'lon' : longitude},
      mapbox_style = 'carto-positron',
      zoom = 2,
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

# create market outlook chart

# create bar chart

chart_df_1 = filtered_df.groupby(by = 'Retailer', as_index = False,)[['Total Sales']].sum()
chart_df_1 = chart_df_1.sort_values(by = 'Retailer', ascending = False)

with col_11:
  title = 'Sales Value by Retailer'
  fig = px.bar(
    chart_df_1,
    y = 'Retailer',
    x = 'Total Sales',
    title = title,
    color_discrete_sequence = colors_1,
    text_auto = '$,.0f',
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

chart_df_2 = filtered_df.groupby(by = 'Sales Method', as_index = False,)[['Total Sales']].sum()
chart_df_2 = chart_df_2.sort_values(by = 'Sales Method', ascending = False)

with col_12:
  title = 'Sales Value by Sales Method'
  fig = px.bar(
    chart_df_2,
    y = 'Sales Method',
    x = 'Total Sales',
    title = title,
    color_discrete_sequence = colors_1,
    text_auto = '$,.0f',
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

chart_df_3 = filtered_df.groupby(by = ['Region'], as_index = False,)[['Total Sales']].sum()

with col_21:
  title = 'Sales Ration by Region'
  #st.subheader(title)
  fig = px.pie(
    chart_df_3,
    values = 'Total Sales',
    names = 'Region',
    hole = 0.5,
    template = chart_theme,
    color_discrete_sequence = colors_1,
  )
  fig.update_traces(
    text = chart_df_3['Region'],
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

chart_df_4 = filtered_df.groupby(by = ['Product'], as_index = False,)[['Total Sales', 'Operating Profit']].sum()
chart_df_4 = chart_df_4.sort_values(by = 'Product', ascending = False)

with col_22:
  title = 'Sales & Operating Profit by Product'
  #st.subheader(title)
  fig = go.Figure(data = [
    go.Bar(
      name = 'Total Sales',
      x = chart_df_4['Product'],
      y = chart_df_4['Total Sales'],
      text = ['${:,.0f}'.format(x) for x in chart_df_4['Total Sales']],
      marker = {'color': colors_1[0]}),
    go.Bar(
      name = 'Operating Margin',
      x = chart_df_4['Product'],
      y = chart_df_4['Operating Profit'],
      text = ['${:,.0f}'.format(x) for x in chart_df_4['Operating Profit']],
      marker = {'color': colors_1[1]}),
  ])

  fig.update_layout(
      template = chart_theme,
      #paper_bgcolor = 'LightSteelBlue',
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

chart_df_5 = filtered_df.groupby(by = ['Product', 'Sales Method'], as_index = False,)[['Operating Margin']].mean()
chart_df_5 = chart_df_5.sort_values(by = 'Product', ascending = False)

with col_23:
  title = 'Average Operating Margin'
  #st.subheader(title)
  fig = px.bar(
    chart_df_5,
    x = 'Product',
    y = 'Operating Margin',
    #text = ['{:,.2f}'.format(x) for x in chart_df_5['Operating Margin']],
    template = chart_theme,
    color = 'Sales Method',
    barmode = 'group',
    color_discrete_sequence = colors_1,
    title = title,
    text_auto = '.2%',
  )

  fig.update_xaxes(visible = True, showspikes = False)
  fig.update_yaxes(visible = True, showspikes = False)

  fig.update_layout(
      height = 400,
      margin = margin,
      titlefont = dict(size = title_font_size),
      title_x = title_x,
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

  with st.expander('View Data'):
    st.write(chart_df_5.style.background_gradient(cmap = cmap))
    csv = chart_df_5.to_csv(index = False).encode('utf-8')
    st.download_button('Download Data', data = csv, file_name = title + '.csv', mime = 'text/csv', help = 'Click here to download as CSV file')

chart_df_6 = filtered_df.groupby(by = 'Product', as_index = False,)[['Total Sales']].sum()
chart_df_6 = chart_df_6.sort_values(by = 'Product', ascending = False)

col_31, col_32 = st.columns((1, 1))

with col_31:
  title = 'Product Sales Value (USD)'
  fig = px.bar(
    chart_df_6,
    x = 'Product',
    y = 'Total Sales',
    title = title,
    color_discrete_sequence = colors_1,
    text_auto = '$,.0f',
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
    height = 400,
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

filtered_df['Month & Year'] = filtered_df['Invoice Date'].dt.to_period('M')
chart_df_7 = pd.DataFrame(filtered_df.groupby([filtered_df['Month & Year'], 'Product'])[['Units Sold']].mean()).reset_index()
chart_df_7['Month & Year'] = chart_df_7['Month & Year'].astype(str)

with col_32:
  title = 'Amount of Product Sold'
  fig = px.line(
    chart_df_7,
    x = 'Month & Year',
    y = 'Units Sold',
    color = 'Product',
    color_discrete_sequence = colors_1,
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
    st.write(chart_df_7.style.background_gradient(cmap = cmap))
    csv = chart_df_7.to_csv(index = False).encode('utf-8')
    st.download_button('Download Data', data = csv, file_name = title + '.csv', mime = 'text/csv', help = 'Click here to download as CSV file')

title = 'Relationship between Product Price and Unit Sold using Scatter Plot'
fig_1 = px.scatter(
  filtered_df,
  x = 'Price per Unit',
  y = 'Units Sold',
  color = 'Product',
  height = 600,
  template = chart_theme,
  color_discrete_sequence = colors_1,
  trendline = 'ols',
  marginal_x = 'histogram',
  marginal_y = 'box',
)
fig_1.update_layout(
  title = title,
  titlefont = dict(size = title_font_size),
  xaxis = dict(title = 'Price Per Unit (USD)', titlefont = dict(size = 14), tickformat = '.2s'),
  yaxis = dict(title = 'Units Sold', titlefont = dict(size = 14)),
  title_x = title_x,
)
st.plotly_chart(fig_1, use_container_width = True, theme = streamlit_theme)

# Download original sample dataset

with st.expander('Sample Data'):
  st.write(df.iloc[:500, 1:20:2].style.background_gradient(cmap = cmap))
  csv = df.to_csv(index = False).encode('utf-8')
  st.download_button('Download Data', data = csv, file_name = 'Data.csv', mime = 'text/csv')
