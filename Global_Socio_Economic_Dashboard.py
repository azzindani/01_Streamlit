
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
  page_title = 'Global Socio Economic',
  page_icon = ':globe_with_meridians:',
  layout = 'wide',
)


# 01 CREATING DASHBOARD TITLE

st.title(':globe_with_meridians: Global Socio Economic Dashboard')
st.markdown('<style>div,block-container{padding-top:0rem;}<style>', unsafe_allow_html = True)


# 02 IMPORTING DATASET

dataset_path = 'https://raw.githubusercontent.com/azzindani/00_Data_Source/main/Global_Socio_Economic.csv'
df = pd.read_csv(dataset_path)
df['Year'] = df['Year'].astype(int)
df = df.fillna(0)

gdf = gpd.read_file('https://raw.githubusercontent.com/azzindani/00_Data_Source/main/Countries_Geojson.geojson')
gdf = gdf.rename(columns = {'admin' : 'Country'})
gdf = gdf[['Country', 'adm0_a3', 'geometry']]

for x in df.columns:
  y = x.title()
  df = df.rename(columns = {x : y})

for x in df.columns:
  if df[x].dtypes == 'object':
    try:
      df[x] = df[x].str.strip()
    except:
      pass

df['Country'] = df['Country'].replace({
    "Cote d'Ivoire" : 'Ivory Coast',
    'Bahamas, The' : 'The Bahamas',
    'Brunei Darussalam' : 'Brunei',
    'Congo, Dem. Rep.' : 'Democratic Republic of the Congo',
    'Guinea-Bissau' : 'Guinea Bissau',
    'Hong Kong SAR, China' : 'Hong Kong S.A.R.',
    'Macao SAR, China' : 'Macao S.A.R',
    'Tanzania' : 'United Republic of Tanzania',
    'Egypt, Arab Rep.' : 'Egypt',
    'Venezuela, RB' : 'Venezuela',
    'Viet Nam' : 'Vietnam',
    'Yemen, Rep.' : 'Yemen',
    'Turkiye' : 'Turkey',
    'Virgin Islands (U.S.)' : 'United States Virgin Islands',
    'St. Vincent and the Grenadines' : 'Saint Vincent and the Grenadines',
    'Timor-Leste' : 'East Timor',
    'Syrian Arab Republic' : 'Syria',
    'Serbia' : 'Republic of Serbia',
    'Slovak Republic' : 'Slovakia',
    'Gambia, The' : 'Gambia',
    'Iran, Islamic Rep.' : 'Iran',
    'Kyrgyz Republic' : 'Kyrgyzstan',
    'Korea, Rep.' : 'South Korea',
    "Korea, Dem. People's Rep." : 'North Korea',
    'North Macedonia' : 'Macedonia',
    'St. Martin (French part)' : 'Saint Martin',
    'Russian Federation' : 'Russia',
    'Sint Maarten (Dutch part)' : 'Sint Maarten',
    'Cabo Verde' : 'Cape Verde',
    'Curacao' : 'Curaçao',
    'West Bank and Gaza' : 'Palestine',
    'Lao PDR' : 'Laos',
    'St. Lucia' : 'Saint Lucia',
    'St. Kitts and Nevis' : 'Saint Kitts and Nevis',
    'Micronesia, Fed. Sts.' : 'Federated States of Micronesia',
    'Congo, Rep.' : 'Republic of Congo',
    'Czechia' : 'Czech Republic',
    'Eswatini' : 'Swaziland',
    'United States' : 'United States of America',
})

drop = []

a = df['Country'].unique()
b = gdf['Country'].unique()

for i in a:
  if i not in b:
    drop.append(i)

for x in drop:
  df = df.drop(df[df['Country'] == x].index)


# 03 SETUP TEMPLATE & THEME

colors_1 = px.colors.sequential.Pinkyl
colors_2 = px.colors.sequential.Pinkyl_r
explode = tuple([0.015] * 50)
latitude = 20
longitude = 0
chart_theme = 'plotly_dark'
streamlit_theme = 'streamlit'
margin = {'r' : 20, 't' : 40, 'l' : 20, 'b' : 10}
cmap = 'pink'
title_x = 0
title_font_size = 18

col_1, col_2 = st.columns((1, 1))

# 05 CREATING FILTER

var_nums = df.columns[4:]

with col_1:
  var_num = st.selectbox('Select Variable', var_nums)

df = df[['Country', 'Year', var_num]]

default_year = df['Year'].max()

with col_2:
  year = st.multiselect('Select Year', df['Year'].unique(), default = default_year)

if year:
  sel_df = df[df['Year'].isin(year)]
else:
  sel_df = df


# 07 CREATING DASHBOARD

# create highlighted indicator

col_11, col_12 = st.columns((1, 2))

chart_df_1 = sel_df.groupby(by = ['Country'], as_index = False,)[[var_num]].sum()
chart_df_1 = chart_df_1.sort_values(by = var_num, ascending = False)[:10]
chart_df_1 = chart_df_1.sort_values(by = var_num, ascending = True)

with col_11:
  title = '10 Highest ' + var_num + ' Country'
  #st.subheader(title)
  fig = px.bar(
    chart_df_1,
    x = var_num,
    y = 'Country',
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

var_label = 'Country'
var_number = var_num

map_df = sel_df.groupby(['Country'])[var_num].sum()
map_df = map_df.reset_index()
map_df = map_df.fillna(0)

map_df = gdf.merge(map_df, on = 'Country')

map_df = map_df.set_index(var_label)

with col_12:
  title = 'Latest ' + var_num + ' Geospatial Data'
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
      zoom = 1,
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


default_country = 'India'

country = st.multiselect('Select Country', df['Country'].unique(), default = default_country)

if country:
  filtered_df = df[df['Country'].isin(country)]
else:
  filtered_df = df

# create time series chart

title = 'Yearly ' + var_num

linechart = pd.DataFrame(filtered_df.groupby(['Year', 'Country'])[[var_num]].sum()).reset_index()
linechart['Year'] = linechart['Year'].astype(str)

fig_1 = px.line(
  x = linechart['Year'],
  y = linechart[var_num],
  color = linechart['Country'],
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
  xaxis = dict(title = 'Year', titlefont = dict(size = 14)),
  yaxis = dict(title = var_num, titlefont = dict(size = 14), tickformat = ',.0f'),
)

st.plotly_chart(fig_1, use_container_width = True, theme = streamlit_theme)

with st.expander('View Data'):
  st.write(linechart.style.background_gradient(cmap = cmap))
  csv = linechart.to_csv(index = False).encode('utf-8')
  st.download_button('Download Data', data = csv, file_name = title + '.csv', mime = 'text/csv', help = 'Click here to download as CSV file')
