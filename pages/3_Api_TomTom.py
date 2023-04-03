import streamlit as st
import pandas as pd
from geopy.geocoders import TomTom
import unidecode
import numpy as np
import geopandas as gpd
import plotly.express as px
import time


st.set_page_config("Geocodificación API TomTom")
APP_TITLE = "Geocodificación API TomTom"

st.title(APP_TITLE)


df_ejemplo = pd.read_csv("archivo_ejemplo.csv", dtype=str, sep=";", encoding="latin-1")

def convert_df(df):
   return df.to_csv(index=False, sep=";").encode('latin-1')

csv = convert_df(df_ejemplo)


def CONSULTA_API_TOMTOM(api_key_input, df_input):
    api_key = api_key_input
    df = df_input
    df['direccion2'] = df['direccion'].apply(lambda x: unidecode.unidecode(x))
    df['direccion2']= df['direccion2'].replace('[^a-zA-Z0-9 ]', '', regex=True)
    df['comuna'] = df['comuna'].apply(lambda x: unidecode.unidecode(x))
    df['comuna']= df['comuna'].replace('[^a-zA-Z0-9 ]', '', regex=True)
    df['comuna'] = df['comuna'].str.title()
    df['comuna'] = df['comuna'].replace(r'\s+', ' ', regex=True)
    df['comuna'] = df['comuna'].replace(r"^ +| +$", r"", regex=True)
    df['direccion_completa'] = df['direccion2'] + ", " + df['comuna'] +", "+ df['region'] + ", Chile"
    df['direccion_completa']= df['direccion_completa'].apply(lambda x: unidecode.unidecode(x))

    df0 = df.drop_duplicates(subset=['direccion'])

    def get_address(x):
        if hasattr(x,'address') and (x.address is not None): 
            return x.address
    
    def get_latitude(x):
        if hasattr(x,'latitude') and (x.latitude is not None): 
            return x.latitude

    def get_longitude(x):
        if hasattr(x,'longitude') and (x.longitude is not None): 
            return x.longitude

    def get_TomTom_type(x):
        if hasattr(x,'raw') and (x.raw['type'] is not None): 
            return x.raw['type']

    geolocator = TomTom(api_key=api_key, timeout=1)
    geolocate_column = df0['direccion_completa'].apply(geolocator.geocode)
    df0['direccion_api'] = geolocate_column.apply(get_address)
    df0['tipo_ubicacion'] = geolocate_column.apply(get_TomTom_type)
    df0['lat'] = geolocate_column.apply(get_latitude)
    df0['long'] = geolocate_column.apply(get_longitude)

    df0.drop(['direccion2'],axis='columns', inplace=True)
    df0 = (df0[["direccion_completa", "direccion_api", "tipo_ubicacion", "lat", "long"]])

    df1 = pd.merge(df, df0, on="direccion_completa", how="left")
    df1.drop(['direccion2'],axis='columns', inplace=True)

    df1['long'] = pd.to_numeric(df1['long'],errors='coerce')
    df1['lat'] = pd.to_numeric(df1['lat'],errors='coerce')

    puntos = gpd.GeoDataFrame(
    df1, geometry=gpd.points_from_xy(df1.long , df1.lat))
    puntos.set_crs(epsg=4326, inplace=True)

    url = "https://www.dropbox.com/s/1n6fzddsb38bok5/comunas_chile_geo.zip?dl=1"

    comunas = gpd.read_file(url)

    puntos_j = gpd.sjoin(puntos, comunas, how="left", predicate='intersects')

    join = pd.DataFrame(puntos_j)

    join.drop(['geometry', 'index_right'], axis='columns', inplace=True)
                
    join['comuna_geo'] = join['comuna_geo'].astype(str)
    join['comuna_geo'] = join['comuna_geo'].apply(lambda x: unidecode.unidecode(x))

    join['comunas_rev'] = np.where(join['comuna'] == join['comuna_geo'], "coincide", "no coincide")

    join["api_consulta"] = 'Mapbox'

    return join



def display_map(df):
    fig = px.scatter_mapbox(df, lat='lat', lon='long', 
                            hover_data=["direccion_completa", "direccion_api", "tipo_ubicacion"], 
                            color="tipo_ubicacion",zoom=10, mapbox_style= 'carto-positron')
    return fig


container = st.container()

with container:
    st.download_button(
        "Descargue archivo de referencia",
        csv,
        "Archivo de referencia.csv",
        "text/csv",
        key='download-csv-Mapbox')

    uploaded_file = st.file_uploader("Elija un archivo csv para realizar la geocodificación", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file, dtype=str, sep=";", encoding="latin-1")
    
    api_key_input = st.text_input(label="Ingrese API key")
    if api_key_input:
        join = CONSULTA_API_TOMTOM(api_key_input, df)

        st.write("Comienza la geocodificación")

        with st.spinner('El proceso está terminando...'):
            time.sleep(5)
        st.success('Listo!')
        st.plotly_chart(display_map(join), use_container_width=True)

        csv_salida = convert_df(join)

        st.download_button(
        "Descargue resultado",
        csv_salida,
        "resultado_API_TOMTOM.csv",
        "text/csv",
        key='download-csv-tomtom')


