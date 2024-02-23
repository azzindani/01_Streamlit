
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
  page_title = 'US Unemployment',
  page_icon = ':male-office-worker:',
  layout = 'wide',
)


# 01 CREATING DASHBOARD TITLE

st.title(':male-office-worker: US Unemployment Dashboard')
st.markdown('<style>div,block-container{padding-top:0rem;}<style>', unsafe_allow_html = True)


# 02 IMPORTING DATASET

dataset_path = 'https://raw.githubusercontent.com/azzindani/00_Data_Source/main/US_Unemployment.csv'
df = pd.read_csv(dataset_path)
df = df.fillna(0)

gdf = gpd.read_file('https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json')
gdf = gdf.rename(columns = {'name' : 'State'})
gdf = gdf[['State', 'geometry']]

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

df['Month And Year'] = df['Month And Year'].replace({
    'January ' : '31-01-',
    'February ' : '28-02-',
    'March ' : '31-03-',
    'April ' : '30-04-',
    'May ' : '31-05-',
    'June ' : '30-06-',
    'July ' : '31-07-',
    'August ' : '31-08-',
    'September ' : '30-09-',
    'October ' : '31-10-',
    'November ' : '30-11-',
    'December ' : '31-12-',
}, regex = True)

df['Month And Year'] = pd.to_datetime(df['Month And Year'])
df['Year'] = df['Month And Year'].dt.to_period('Y')
df['Year'] = df['Year'].astype('str')
df['Year'] = df['Year'].astype('int')

df['State'] = df['State'].replace({
    'District Of Columbia' : 'District of Columbia',
})


# 03 SETUP TEMPLATE & THEME

colors_1 = px.colors.sequential.Blues
colors_2 = px.colors.sequential.Blues_r
explode = tuple([0.015] * 50)
latitude = 57
longitude = -113
chart_theme = 'plotly_dark'
streamlit_theme = 'streamlit'
margin = {'r' : 20, 't' : 40, 'l' : 20, 'b' : 10}
cmap = 'Blues'
title_x = 0
title_font_size = 18


col_1, col_2 = st.columns((1, 1))

# 05 CREATING FILTER

var_nums = df.columns[3:]

with col_1:
  var_num = st.selectbox('Select Variable', var_nums)

with col_2:
  year = st.slider(
    label = 'Select Year',
    min_value = df['Year'].min(),
    max_value = df['Year'].max(),
    value = df['Year'].max(),
  )

df = df[['State', 'Month And Year', 'Year', var_num]]
filtered_df = df[df['Year'] == year]


# 07 CREATING DASHBOARD

# create highlighted indicator

col_11, col_12 = st.columns((1, 2))

chart_df_1 = filtered_df.groupby(by = ['State'], as_index = False,)[[var_num]].sum()
chart_df_1 = chart_df_1.sort_values(by = var_num, ascending = False)[:10]

with col_11:
  title = '10 Highest ' + var_num + ' State'
  #st.subheader(title)
  fig = px.bar(
    chart_df_1,
    x = var_num,
    y = 'State',
    template = chart_theme,
    color_discrete_sequence = colors_2,
    title = title,
    text_auto = ',.0f',
  )
  fig.update_layout(
      height = 600,
      margin = margin,
      titlefont = dict(size = title_font_size),
      title_x = title_x,
  )
  fig.update_yaxes(categoryorder = 'total ascending')
  st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)

  with st.expander('View Data'):
    st.write(chart_df_1.style.background_gradient(cmap = cmap))
    csv = chart_df_1.to_csv(index = False).encode('utf-8')
    st.download_button('Download Data', data = csv, file_name = title + '.csv', mime = 'text/csv', help = 'Click here to download as CSV file')

var_label = 'State'
var_number = var_num

map_df = filtered_df.groupby(['State'])[var_num].sum()
map_df = map_df.reset_index()
map_df = map_df.fillna(0)
map_df = gdf.merge(map_df, on = 'State')
map_df = map_df.set_index(var_label)

with col_12:
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
      #width = 800,
      height = 600,
  )
  fig.update_geos(
      #fitbounds = 'locations',
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

# create time series chart

col_11, col_12 = st.columns((1, 1))

default_state = 'Florida'

with col_11:
  state = st.multiselect('Select State', df['State'].unique(), default = default_state)

if state:
  state_df = df[df['State'].isin(state)]
else:
  state_df = df

periods = ['M', 'Q', 'Y']

with col_12:
  period = st.selectbox('Select Period (M = Month, Q = Quarter, Y = Year)', periods)

title = 'Periodly ' + var_num

state_df['Period'] = state_df['Month And Year'].dt.to_period(period)
linechart = pd.DataFrame(state_df.groupby(['Period', 'State'])[[var_num]].sum()).reset_index()
linechart['Period'] = linechart['Period'].astype(str)

fig_1 = px.line(
  x = linechart['Period'],
  y = linechart[var_num],
  color = linechart['State'],
  markers = True,
)
fig_1.update_traces(
  #hovertemplate = '{:,.0f}'
)
fig_1.update_layout(
  hovermode = 'x',
  height = 400,
  margin = margin,
  title = title,
  titlefont = dict(size = title_font_size),
  title_x = title_x,
  xaxis = dict(title = 'Period', titlefont = dict(size = 14)),
  yaxis = dict(title = var_num, titlefont = dict(size = 14), tickformat = ',.0f'),
)

st.plotly_chart(fig_1, use_container_width = True, theme = streamlit_theme)

with st.expander('View Data'):
  st.write(linechart.style.background_gradient(cmap = cmap))
  csv = linechart.to_csv(index = False).encode('utf-8')
  st.download_button('Download Data', data = csv, file_name = title + '.csv', mime = 'text/csv', help = 'Click here to download as CSV file')
