
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
  page_title = 'Superstore Dahsboard',
  page_icon = ':bar_chart:',
  layout = 'wide',
)


# 01 CREATING DASHBOARD TITLE

st.title(':bar_chart: Superstore Sales Dahsboard')
st.markdown('<style>div,block-container{padding-top:0rem;}<style>', unsafe_allow_html = True)


# 02 IMPORTING DATASET

dataset_path = 'https://raw.githubusercontent.com/azzindani/00_Data_Source/main/Cleaned_Global_Superstore_2018.csv'
df = pd.read_csv(dataset_path, encoding = 'ISO-8859-1')

gdf = gpd.read_file('https://raw.githubusercontent.com/azzindani/00_Data_Source/main/Countries_Geojson.geojson')
gdf = gdf.rename(columns = {'admin' : 'Country'})
gdf = gdf[['Country', 'adm0_a3', 'geometry']]


# 03 SETUP TEMPLATE & THEME

colors_1 = px.colors.sequential.Reds
colors_2 = px.colors.sequential.RdBu
explode = tuple([0.015] * 50)
latitude = 0
longitude = 0
chart_theme = 'plotly_dark'
streamlit_theme = 'streamlit'
margin = {'r' : 20, 't' : 40, 'l' : 20, 'b' : 10}
cmap = 'Reds'
title_x = 0
title_font_size = 18


# 04 CREATING DATE PICKER

col_1, col_2 = st.columns((2))
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Getting min & max date
start_date = pd.to_datetime(df['Order Date']).min()
end_date = pd.to_datetime(df['Order Date']).max()

with col_1:
  date_1 = pd.to_datetime(st.date_input('Start Date', start_date))

with col_2:
  date_2 = pd.to_datetime(st.date_input('End Date', end_date))

df = df[(df['Order Date'] >= date_1) & (df['Order Date'] <= date_2)] #'''


# 05 CREATING SIDEBAR FILTER

st.sidebar.header('Choose your Filter: ')

# Create market sidebar
market = st.sidebar.multiselect('Select Region', df['Market'].unique())

if not market:
  df_2 = df.copy()
else:
  df_2 = df[df['Market'].isin(market)]

# Create country sidebar
country = st.sidebar.multiselect('Select Country', df_2['Country'].unique())

if not country:
  df_3 = df_2.copy()
else:
  df_3 = df_2[df_2['Country'].isin(country)]

# Create state sidebar
state = st.sidebar.multiselect('Select State', df_3['State'].unique())

if not state:
  df_4 = df_3.copy()
else:
  df_4 = df_3[df_3['State'].isin(state)]

# Create city sidebar
city = st.sidebar.multiselect('Select City', df_4['City'].unique())


# 06 CREATING DATASET FILTER LOGIC

# Filter the data based on market, country, state, city

# None filter
if not market and not country and not state and not city:
  filtered_df = df

# Single filter
elif not country and not state and not city:
  filtered_df = df[df['Market'].isin(market)]
elif not market and not state and not city:
  filtered_df = df[df['Country'].isin(country)]
elif not market and not country and not city:
  filtered_df = df[df['State'].isin(state)]

# Multiple filter
elif country and state and city:
  filtered_df = df_4[df['Country'].isin(country) & df['State'].isin(state) & df['City'].isin(city)]
elif market and state and city:
  filtered_df = df_4[df['Market'].isin(market) & df['State'].isin(state) & df['City'].isin(city)]
elif market and country and city:
  filtered_df = df_4[df['Market'].isin(market) & df['Country'].isin(country) & df['City'].isin(city)]
elif market and country and state:
  filtered_df = df_4[df['Market'].isin(market) & df['Country'].isin(country) & df['State'].isin(state)]

elif market and country:
  filtered_df = df_4[df['Market'].isin(market) & df['Country'].isin(country)]
elif market and state:
  filtered_df = df_4[df['Market'].isin(market) & df['State'].isin(state)]
elif market and city:
  filtered_df = df_4[df['Market'].isin(market) & df['City'].isin(city)]

elif country and city:
  filtered_df = df_4[df['Country'].isinc(country) & df['City'].isin(city)]
elif state and city:
  filtered_df = df_4[df['State'].isin(state) & df['City'].isin(city)]

elif city:
  filtered_df = df_4[df_4['City'].isin(city)]

else:
  filtered_df = df_4[df_4['Market'].isin(market) & df_4['Country'].isin(country) & df_4['State'].isin(state) & df_4['City'].isin(city)]


# 07 CREATING DASHBOARD

# create highlighted indicator

col_11, col_12, col_13 = st.columns((1, 1, 4))

with col_11:
  title = 'Total Sales'
  #st.subheader(title)
  fig = go.Figure(go.Indicator(
    mode = 'number+delta',
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = filtered_df['Sales'].sum(),
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
  title = 'Profit relative to Sales'
  #st.subheader(title)
  fig = go.Figure(go.Indicator(
    mode = 'gauge+number',
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = filtered_df['Profit'].sum(),
    gauge = {'axis' : {'range' : [None, df['Sales'].sum()]}, 'bar' : {'color' : colors_1[-2]}},
    #gauge = {'shape': "bullet"},
    #number = {'font_color': colors_1[1]},
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

map_df = filtered_df.groupby(['Country'])[['Sales']].sum()
map_df = map_df.reset_index()
map_df = gdf.merge(map_df, on = 'Country', how = 'left')
map_df = map_df.fillna(0)

with col_13:
  title = 'Geospatial Sales Data'
  #st.subheader(title)
  fig = go.Figure(data = go.Choropleth(
      locations = map_df['adm0_a3'],
      z = map_df['Sales'],
      colorscale = colors_1,
      colorbar_title = 'Total Sales',
      colorbar_tickprefix = '$',
      hovertemplate = map_df['Country'] + ' : ' + ['${:,.2f}'.format(x) for x in map_df['Sales']],
  ))
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

market_df_1 = filtered_df.groupby(by = 'Segment', as_index = False,)[['Sales']].sum()

with col_11:
  title = 'Segment wise Sales'
  #st.subheader(title)
  fig = px.pie(
    market_df_1,
    values = 'Sales',
    names = 'Segment',
    template = chart_theme,
    hole = 0.5,
    color_discrete_sequence = colors_2,
    title = title,
  )
  fig.update_traces(
    text = market_df_1['Segment'],
    textposition = 'inside',
    pull = explode,
  )
  fig.update_layout(
    height = 300,
    margin = margin,
    title = title,
    titlefont = dict(size = title_font_size),
    title_x = title_x,
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

  with st.expander('View Data'):
    st.write(market_df_1.style.background_gradient(cmap = cmap))
    csv = market_df_1.to_csv(index = False).encode('utf-8')
    st.download_button('Download Data', data = csv, file_name = title + '.csv', mime = 'text/csv', help = 'Click here to download as CSV file')

market_df_2 = filtered_df.groupby(by = 'Category', as_index = False,)[['Sales']].sum()

with col_12:
  title = 'Category wise Sales'
  #st.subheader(title)
  fig = px.pie(
    market_df_2,
    values = 'Sales',
    names = 'Category',
    template = chart_theme,
    hole = 0.5,
    color_discrete_sequence = colors_2,
    title = title,
  )
  fig.update_traces(
    text = market_df_2['Category'],
    textposition = 'inside',
    pull = explode,
  )
  fig.update_layout(
    height = 300,
    margin = margin,
    title = title,
    titlefont = dict(size = title_font_size),
    title_x = title_x,
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

  with st.expander('View Data'):
    st.write(market_df_2.style.background_gradient(cmap = cmap))
    csv = market_df_2.to_csv(index = False).encode('utf-8')
    st.download_button('Download Data', data = csv, file_name = title + '.csv', mime = 'text/csv', help = 'Click here to download as CSV file')

# create pie chart

col_21, col_22, col_23 = st.columns((1, 1, 1))

market_df_3 = filtered_df.groupby(by = 'Market', as_index = False,)[['Sales']].sum()

with col_21:
  title = 'Region Market wise Sales'
  #st.subheader(title)
  fig = px.pie(
    market_df_3,
    values = 'Sales',
    names = 'Market',
    hole = 0.5,
    template = chart_theme,
    color_discrete_sequence = colors_2,
  )
  fig.update_traces(
    text = market_df_3['Market'],
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
    st.write(market_df_3.style.background_gradient(cmap = cmap))
    csv = market_df_3.to_csv(index = False).encode('utf-8')
    st.download_button('Download Data', data = csv, file_name = title + '.csv', mime = 'text/csv', help = 'Click here to download as CSV file')

market_df_4 = filtered_df.groupby(by = ['Market'], as_index = False)[['Sales', 'Profit']].sum()

with col_22:
  title = 'Region Market Turnover'
  #st.subheader(title)
  fig = go.Figure(data = [
    go.Bar(
      name = 'Sales',
      x = market_df_4['Market'],
      y = market_df_4['Sales'],
      text = ['${:,.2f}'.format(x) for x in market_df_4['Sales']],
      marker = {'color': colors_2[0]}),
    go.Bar(
      name = 'Profit',
      x = market_df_4['Market'],
      y = market_df_4['Profit'],
      text = ['${:,.2f}'.format(x) for x in market_df_4['Profit']],
      marker = {'color': colors_2[2]}),
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
    st.write(market_df_4.style.background_gradient(cmap = cmap))
    csv = market_df_4.to_csv(index = False).encode('utf-8')
    st.download_button('Download Data', data = csv, file_name = title + '.csv', mime = 'text/csv', help = 'Click here to download as CSV file')

market_df_5 = filtered_df.groupby(by = ['Market', 'Category'], as_index = False)[['Sales']].sum()

with col_23:
  title = 'Region Market Category Outlook'
  #st.subheader(title)
  fig = px.bar(
    market_df_5,
    x = 'Market',
    y = 'Sales',
    text = ['${:,.2f}'.format(x) for x in market_df_5['Sales']],
    template = chart_theme,
    color = 'Category',
    barmode = 'group',
    color_discrete_sequence = colors_2,
    title = title,
  )
  fig.update_layout(
      height = 400,
      margin = margin,
      titlefont = dict(size = title_font_size),
      title_x = title_x,
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

  with st.expander('View Data'):
    st.write(market_df_5.style.background_gradient(cmap = cmap))
    csv = market_df_5.to_csv(index = False).encode('utf-8')
    st.download_button('Download Data', data = csv, file_name = title + '.csv', mime = 'text/csv', help = 'Click here to download as CSV file')

filtered_df['Month & Year'] = filtered_df['Order Date'].dt.to_period('M')

# create time series chart

#linechart = pd.DataFrame(filtered_df.groupby(filtered_df['Month & Year'].dt.strftime('%Y : %b'))[['Sales', 'Profit']].sum()).reset_index()
linechart = pd.DataFrame(filtered_df.groupby(filtered_df['Month & Year'])[['Sales', 'Profit']].sum()).reset_index()
linechart['Month & Year'] = linechart['Month & Year'].astype(str)

title = 'Time Series Sales & Profit Data'
#st.subheader(title)
fig_1 = go.Figure()
fig_1.add_trace(go.Scatter(
  x = linechart['Month & Year'],
  y = linechart['Sales'],
  mode = 'lines+markers',
  name = 'Sales',
  marker = {'color': colors_2[0]},
))
fig_1.add_trace(go.Scatter(
  x = linechart['Month & Year'],
  y = linechart['Profit'],
  mode = 'lines+markers',
  name = 'Profit',
  marker = {'color': colors_2[2]},
))
fig_1.update_layout(
  hovermode = 'x',
  height = 400,
  margin = margin,
  title = title,
  titlefont = dict(size = title_font_size),
  title_x = title_x,
)
st.plotly_chart(fig_1, use_container_width = True, theme = streamlit_theme)

with st.expander('View Data of Time Series'):
  st.write(linechart.T.style.background_gradient(cmap = cmap))
  csv = linechart.to_csv(index = False).encode('utf-8')
  st.download_button('Download Data', data = csv, file_name = title + '.csv', mime = 'text/csv')

# create treemap chart

title = 'Hierarchial View of Sales using Tree Map'
#st.subheader(title)
fig_2 = px.treemap(
  filtered_df,
  path = ['Country', 'Category', 'Sub-Category'],
  values = 'Sales',
  hover_data = ['Sales'],
  color = 'Sales',
  template = chart_theme,
  color_continuous_scale = colors_2,
)
fig_2.update_layout(
  height = 400,
  margin = margin,
  title = title,
  titlefont = dict(size = title_font_size),
  title_x = title_x,
)
st.plotly_chart(fig_2, use_container_width = True, theme = streamlit_theme)

col_31, col_32 = st.columns((2))

# create a scatter plot

with col_31:
  title = 'Relationship between Sales and Profits using Scatter Plot'
  fig = px.scatter(
    filtered_df,
    x = 'Sales',
    y = 'Profit',
    size = 'Quantity',
    color = 'Sub-Category',
    height = 500,
    template = chart_theme,
    color_discrete_sequence = colors_2,
  )
  fig.update_layout(
    title = title,
    titlefont = dict(size = title_font_size),
    xaxis = dict(title = 'Sales', titlefont = dict(size = 14), tickformat = '.2s'),
    yaxis = dict(title = 'Profit', titlefont = dict(size = 14), tickformat = '.2s'),
    title_x = title_x,
  )
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

with col_32:
  title = '<p style = "font-size : 18px; font-weight : bold;">Month wise Sub-Category Table Quantity Summary</p>'
  st.markdown(title, unsafe_allow_html = True)
  filtered_df['month'] = filtered_df['Order Date'].dt.month_name()
  sub_category_year = pd.pivot_table(data = filtered_df, values = 'Sales', index = ['Sub-Category'], columns = 'month').astype(int)
  st.write(sub_category_year.style.background_gradient(cmap = cmap))
  csv = sub_category_year.to_csv(index = False).encode('utf-8')
  st.download_button('Download Data', data = csv, file_name = title + '.csv', mime = 'text/csv', help = 'Click here to download as CSV file')

# Download original sample dataset

with st.expander('Sample Data'):
  st.write(filtered_df.iloc[:500, 1:20:2].style.background_gradient(cmap = cmap))
  csv = df.to_csv(index = False).encode('utf-8')
  st.download_button('Download Data', data = csv, file_name = 'Data.csv', mime = 'text/csv')
