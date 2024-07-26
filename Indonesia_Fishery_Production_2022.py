
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
  page_title = 'Perikanan Indonesia',
  page_icon = ':anchor:',
  layout = 'wide',
)


# 01 CREATING DASHBOARD TITLE

st.title(':whale: Produksi Perikanan Indonesia 2022 (Geospatial Analysis)')
st.markdown('<style>div,block-container{padding-top:0rem;}<style>', unsafe_allow_html = True)


# 02 IMPORTING DATASET

dataset_path = 'https://raw.githubusercontent.com/azzindani/00_Data_Source/main/Indonesia_Fishery_Production_2022.csv'
df = pd.read_csv(dataset_path)
df['Kabupaten/Kota'] = df['Kabupaten/Kota'].replace({'KABUPATEN ' : '', 'KOTA ' : '', 'ADM. ' : ''}, regex = True)
df = df.rename(columns = {'Volume Produksi' : 'Volume Produksi (Ton)', 'Nilai Produksi' : 'Nilai Produksi (Rupiah)'})

gdf = gpd.read_file('https://raw.githubusercontent.com/azzindani/00_Data_Source/main/Indonesia_Cities.geojson')
gdf = gdf.rename(columns = {'admin' : 'Country'})
gdf = gdf[['alt_name', 'geometry']]
gdf = gdf.rename(columns = {'alt_name' : 'Kabupaten/Kota'})
gdf['Kabupaten/Kota'] = gdf['Kabupaten/Kota'].replace({'KABUPATEN ' : '', 'KOTA ' : ''}, regex = True)

df['Kabupaten/Kota'] = df['Kabupaten/Kota'].replace({
  'LABUHANBATU UTARA' : 'LABUHAN BATU UTARA',
  'TOLI TOLI' : 'TOLI-TOLI',
  'PARE PARE' : 'PARE-PARE',
  'BAU BAU' : 'BAUBAU',
  'KAB MALUKU TENGGARA BARAT' : 'MALUKU TENGGARA BARAT',
  'PANGKAJENE KEPULAUAN' : 'PANGKAJENE DAN KEPULAUAN',
  'LABUHANBATU' : 'LABUHAN BATU',
  'BANYUASIN' : 'BANYU ASIN',
  'KEP. SERIBU' : 'KEPULAUAN SERIBU',
  'PAHUWATO' : 'POHUWATO',
  'MUKO MUKO' : 'MUKOMUKO',
  'TULANG BAWANG' : 'TULANGBAWANG',
  'TOJO UNA UNA' : 'TOJO UNA-UNA',
  'KEP. SIAU TAGULANDANG BIARO' : 'SIAU TAGULANDANG BIARO',
  'KARANGASEM' : 'KARANG ASEM',
  'FAK FAK' : 'FAK-FAK',
}) #'''

gdf['Kabupaten/Kota'] = gdf['Kabupaten/Kota'].replace({
  'BARU' : 'KOTABARU',
}) #'''


# 03 SETUP TEMPLATE & THEME

colors_1 = px.colors.sequential.Reds
colors_2 = px.colors.sequential.RdBu
explode = tuple([0.015] * 50)
latitude = -2
longitude = 117
chart_theme = 'plotly_dark'
streamlit_theme = 'streamlit'
margin = {'r' : 10, 't' : 10, 'l' : 10, 'b' : 10}
cmap = 'magma_r'
title_x = 0
title_font_size = 18


# 04 CREATING SIDEBAR FILTER

st.sidebar.header('Pilih Filter: ')

# Create variable sidebar

themes = ['carto-positron', 'open-street-map', 'carto-darkmatter', 'white-bg']
theme = st.sidebar.selectbox('Pilih Teme', themes)

vars = ['Volume Produksi (Ton)', 'Nilai Produksi (Rupiah)']
var_number = st.sidebar.selectbox('Pilih Variable', vars)

df = df[['Kabupaten/Kota', 'Pelabuhan', 'Jenis Kapal', 'Jenis Alat Tangkap', 'WPP', 'Jenis Ikan', var_number]]

# Create Pelabuhan sidebar
pelabuhan = st.sidebar.multiselect('Pelabuhan', df['Pelabuhan'].unique())

if not pelabuhan:
  df_2 = df.copy()
else:
  df_2 = df[df['Pelabuhan'].isin(pelabuhan)]

# Create Jenis Kapal sidebar
kapal = st.sidebar.multiselect('Jenis Kapal', df_2['Jenis Kapal'].unique())

if not kapal:
  df_3 = df_2.copy()
else:
  df_3 = df_2[df_2['Jenis Kapal'].isin(kapal)]

# Create WPP sidebar
wpp = st.sidebar.multiselect('WPP', df_3['WPP'].unique())

if not wpp:
  df_4 = df_3.copy()
else:
  df_4 = df_3[df_3['WPP'].isin(wpp)]

# Create Jenis Ikan sidebar
ikan = st.sidebar.multiselect('Jenis Ikan', df_4['Jenis Ikan'].unique())


# 05 CREATING DATASET FILTER LOGIC

# None filter

if not pelabuhan and not kapal and not wpp and not ikan:
  filtered_df = df

# Single filter

elif not kapal and not wpp and not ikan:
  filtered_df = df[df['Pelabuhan'].isin(pelabuhan)]
elif not pelabuhan and not wpp and not ikan:
  filtered_df = df[df['Jenis Kapal'].isin(kapal)]
elif not pelabuhan and not kapal and not ikan:
  filtered_df = df[df['WPP'].isin(wpp)]
elif not pelabuhan and not kapal and not wpp:
  filtered_df = df[df['Jenis Ikan'].isin(ikan)]

# Multiple filter

elif kapal and wpp and ikan:
  filtered_df = df_4[df['Jenis Kapal'].isin(kapal) & df['WPP'].isin(wpp) & df['Jenis Ikan'].isin(ikan)]
elif pelabuhan and wpp and ikan:
  filtered_df = df_4[df['Pelabuhan'].isin(pelabuhan) & df['WPP'].isin(wpp) & df['Jenis Ikan'].isin(ikan)]
elif pelabuhan and kapal and ikan:
  filtered_df = df_4[df['Pelabuhan'].isin(pelabuhan) & df['Jenis Kapal'].isin(kapal) & df['Jenis Ikan'].isin(ikan)]
elif pelabuhan and kapal and wpp:
  filtered_df = df_4[df['Pelabuhan'].isin(pelabuhan) & df['Jenis Kapal'].isin(kapal) & df['WPP'].isin(wpp)]

elif pelabuhan and kapal:
  filtered_df = df_4[df['Pelabuhan'].isin(pelabuhan) & df['Jenis Kapal'].isin(kapal)]
elif pelabuhan and wpp:
  filtered_df = df_4[df['Pelabuhan'].isin(pelabuhan) & df['WPP'].isin(wpp)]
elif pelabuhan and ikan:
  filtered_df = df_4[df['Pelabuhan'].isin(pelabuhan) & df['Jenis Ikan'].isin(ikan)]

elif kapal and ikan:
  filtered_df = df_4[df['Jenis Kapal'].isin(kapal) & df['Jenis Ikan'].isin(ikan)]
elif wpp and ikan:
  filtered_df = df_4[df['WPP'].isin(wpp) & df['Jenis Ikan'].isin(ikan)]

elif ikan:
  filtered_df = df_4[df_4['Jenis Ikan'].isin(ikan)]

else:
  filtered_df = df_4[df_4['Pelabuhan'].isin(pelabuhan) & df_4['Jenis Kapal'].isin(kapal) & df_4['WPP'].isin(wpp) & df_4['Jenis Ikan'].isin(ikan)]


# 06 CREATING DASHBOARD

map_df = filtered_df.groupby(['Kabupaten/Kota'])[var_number].sum()
map_df = map_df.reset_index()
map_df = gdf.merge(map_df, on = 'Kabupaten/Kota')

var_label = 'Kabupaten/Kota'

map_df = map_df.set_index(var_label)

fig = px.choropleth_mapbox(
  data_frame = map_df,
  geojson = map_df.geometry,
  locations = map_df.index,
  color = var_number,
  color_continuous_scale = colors_1,
  #range_color = (0, 10),
  opacity = 0.5,
  center = {'lat' : latitude, 'lon' : longitude},
  mapbox_style = theme,
  zoom = 4.5,
)

fig.update_geos(
  fitbounds = 'locations',
  visible = False,
)
fig.update_layout(
  height = 800,
  margin = margin,
)
st.plotly_chart(fig, use_container_width = True, theme = streamlit_theme)
