
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
  page_title = 'Bike Sales',
  page_icon = ':bar_chart:',
  layout = 'wide',
)


# 01 CREATING DASHBOARD TITLE

st.title(':bar_chart: Bike Sales Dashboard')
st.markdown('<style>div,block-container{padding-top:0rem;}<style>', unsafe_allow_html = True)


# 02 IMPORTING DATASET

dataset_path = 'https://raw.githubusercontent.com/azzindani/00_Data_Source/main/Europe_Bike_Sales.csv'
df = pd.read_csv(dataset_path, encoding = 'ISO-8859-1')

df['Country'] = df['Country'].replace({
    'United States' : 'United States of America',
})

gdf = gpd.read_file('https://raw.githubusercontent.com/azzindani/00_Data_Source/main/Countries_Geojson.geojson')
gdf = gdf.rename(columns = {'admin' : 'Country'})
gdf = gdf[['Country', 'adm0_a3', 'geometry']]


# 03 SETUP TEMPLATE & THEME

colors_1 = px.colors.sequential.Rainbow
colors_2 = px.colors.sequential.Rainbow
explode = tuple([0.015] * 50)
latitude = 0
longitude = 0
chart_theme = 'plotly_dark'
streamlit_theme = 'streamlit'
margin = {'r' : 20, 't' : 40, 'l' : 20, 'b' : 10}
cmap = 'rainbow'
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

st.sidebar.header('Choose your Filter: ')

# Create country sidebar
country = st.sidebar.multiselect('Select Country', df['Country'].unique())

if not country:
  df_2 = df.copy()
else:
  df_2 = df[df['Country'].isin(country)]

# Create state sidebar
state = st.sidebar.multiselect('Select State', df_2['State'].unique())


# 06 CREATING DATASET FILTER LOGIC

# Filter the data based on country, state

# None filter
if not country and not state:
  filtered_df = df

# Single filter
elif not state:
  filtered_df = df[df['Country'].isin(country)]

elif not county:
  filtered_df = df[df['State'].isin(state)]

else:
  filtered_df = df_2[df_2['Country'].isin(country) & df_2['State'].isin(state)]


# 07 CREATING DASHBOARD

# create highlighted indicator

col_11, col_12, col_13 = st.columns((1, 1, 3))

with col_11:
  title = 'Revenue'
  #st.subheader(title)
  fig = go.Figure(go.Indicator(
    mode = 'number+delta',
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = filtered_df['Revenue'].sum(),
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
  title = 'Units Sold'
  #st.subheader(title)
  fig = go.Figure(go.Indicator(
    mode = 'number+delta',
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = filtered_df['Order_Quantity'].sum(),
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

map_df = filtered_df.groupby(['Country'])['Revenue'].sum()
map_df = map_df.reset_index()
map_df = map_df.rename(columns = {'Revenue' : 'Revenue (USD)'})
map_df = gdf.merge(map_df, on = 'Country')

var_label = 'Country'
var_number = 'Revenue (USD)'

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
      zoom = 0.3,
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

# create pie chart

chart_df_1 = filtered_df.groupby(by = ['Age_Group'], as_index = False,)[['Order_Quantity']].sum()

with col_11:
  title = 'Unit Sold by Age Group'
  fig = px.bar(
    chart_df_1,
    y = 'Age_Group',
    x = 'Order_Quantity',
    title = title,
    color_discrete_sequence = colors_1,
    text_auto = ',.0f',
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

chart_df_2 = filtered_df.groupby(by = ['Product_Category'], as_index = False)[['Order_Quantity']].sum()

with col_12:
  title = 'Unit Sold by Product Category'
  fig = px.bar(
    chart_df_2,
    y = 'Product_Category',
    x = 'Order_Quantity',
    title = title,
    color_discrete_sequence = colors_1,
    text_auto = ',.0f',
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

chart_df_3 = filtered_df.groupby(by = ['Country'], as_index = False,)[['Revenue']].sum()

with col_21:
  title = 'Revenue Ratio by Country'
  #st.subheader(title)
  fig = px.pie(
    chart_df_3,
    values = 'Revenue',
    names = 'Country',
    hole = 0.5,
    template = chart_theme,
    color_discrete_sequence = colors_1,
  )
  fig.update_traces(
    text = chart_df_3['Country'],
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

chart_df_4 = filtered_df.groupby(by = ['Country', 'Product_Category'], as_index = False)[['Revenue', 'Profit']].sum()

with col_22:
  title = 'Product Category by Country'
  fig = px.bar(
    chart_df_4,
    x = 'Country',
    y = 'Revenue',
    text = ['${:,.0f}'.format(x) for x in chart_df_4['Revenue']],
    color = 'Product_Category',
    template = chart_theme,
    color_discrete_sequence = colors_2,
    barmode = 'group',
    height = 500,
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
    st.write(chart_df_4.style.background_gradient(cmap = cmap))
    csv = chart_df_4.to_csv(index = False).encode('utf-8')
    st.download_button('Download Data', data = csv, file_name = title + '.csv', mime = 'text/csv', help = 'Click here to download as CSV file')

filtered_df['Profit Ratio'] = filtered_df['Profit'] / filtered_df['Revenue']
chart_df_5 = filtered_df.groupby(by = ['Sub_Category'], as_index = False,)[['Profit Ratio']].mean()

with col_23:
  title = 'Profit Ratio by Sub Category'
  #st.subheader(title)
  fig = px.bar(
    chart_df_5,
    x = 'Sub_Category',
    y = 'Profit Ratio',
    #text = ['{:,.2f}'.format(x) for x in chart_df_5['Profit Ratio']],
    template = chart_theme,
    color_discrete_sequence = colors_2,
    title = title,
    text_auto = '.2%',
  )
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

chart_df_6 = filtered_df.groupby(by = ['Sub_Category'], as_index = False,)[['Revenue', 'Profit']].sum()

title = 'Sales & Operating Profit by Product'
#st.subheader(title)
fig = go.Figure(data = [
  go.Bar(
    name = 'Revenue',
    x = chart_df_6['Sub_Category'],
    y = chart_df_6['Revenue'],
    text = ['${:,.0f}'.format(x) for x in chart_df_4['Revenue']],
    marker = {'color': colors_2[0]}),
  go.Bar(
    name = 'Profit',
    x = chart_df_6['Sub_Category'],
    y = chart_df_6['Profit'],
    text = ['${:,.0f}'.format(x) for x in chart_df_6['Profit']],
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
  st.write(chart_df_6.style.background_gradient(cmap = cmap))
  csv = chart_df_6.to_csv(index = False).encode('utf-8')
  st.download_button('Download Data', data = csv, file_name = title + '.csv', mime = 'text/csv', help = 'Click here to download as CSV file')

filtered_df['Profit Ratio'] = filtered_df['Profit'] / filtered_df['Revenue']

filtered_df['Month & Year'] = filtered_df['Date'].dt.to_period('M')
linechart = pd.DataFrame(filtered_df.groupby(df['Month & Year'])[['Revenue', 'Profit']].sum()).reset_index()
linechart['Month & Year'] = linechart['Month & Year'].astype(str)

# create time series chart

title = 'Time Series Sales & Profit Data'
#st.subheader(title)
fig_1 = go.Figure()
fig_1.add_trace(go.Scatter(
  x = linechart['Month & Year'],
  y = linechart['Revenue'],
  mode = 'lines+markers',
  name = 'Revenue',
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

# create treemap chart

title = 'Hierarchial View of Sales using Tree Map'
#st.subheader(title)
fig_2 = px.treemap(
  filtered_df,
  path = ['Country', 'Product_Category', 'Sub_Category'],
  values = 'Revenue',
  hover_data = ['Revenue'],
  color = 'Revenue',
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

# create scatter plot chart

title = 'Relationship between Product Unit Price and Unit Sold using Scatter Plot'
fig_3 = px.scatter(
  filtered_df,
  x = 'Unit_Price',
  y = 'Customer_Age',
  color = 'Product_Category',
  height = 600,
  template = chart_theme,
  color_discrete_sequence = colors_1,
  #trendline = 'ols',
  marginal_x = 'histogram',
  #marginal_y = 'box',
  facet_col = 'Customer_Gender'
)
fig_3.update_layout(
  title = title,
  titlefont = dict(size = title_font_size),
  xaxis = dict(title = 'Unit Price (USD)', titlefont = dict(size = 14)),
  yaxis = dict(title = 'Customer_Age', titlefont = dict(size = 14)),
  title_x = title_x,
)
st.plotly_chart(fig_3, use_container_width = True, theme = streamlit_theme)

# Download original sample dataset

with st.expander('Sample Data'):
  st.write(df.iloc[:500, 1:20:2].style.background_gradient(cmap = cmap))
  csv = df.to_csv(index = False).encode('utf-8')
  st.download_button('Download Data', data = csv, file_name = 'Data.csv', mime = 'text/csv')
