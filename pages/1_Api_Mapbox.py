import streamlit as st
import pandas as pd
from geopy.geocoders import MapBox
import unidecode
import numpy as np
import geopandas as gpd
import plotly.express as px
import time



st.set_page_config("Geocodificación API Mapbox")


st.markdown("""<p style="text-align:center;"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Mapbox_logo_2019.svg/1280px-Mapbox_logo_2019.svg.png"
alt="whatever" width="220" height= "70"></p>""", unsafe_allow_html=True)

st.markdown("---")

df_ejemplo = pd.read_csv("archivo_ejemplo.csv", dtype=str, sep=";", encoding="latin-1")
df_region = pd.read_csv("regiones_chile.csv", dtype=str, sep=";", encoding="latin-1")
opciones_region = list(df_region['regiones'].drop_duplicates())

def convert_df(df):
    return df.to_csv(index=False, sep=";").encode('latin-1')
    #return df.to_csv(index=False, sep=";").encode('cp1252')
    #return df.to_csv(index=False, sep=";").encode('utf-8')

csv = convert_df(df_ejemplo)

@st.cache_data()
def CONSULTA_API_MAPBOX(api_key_input, df_input, reg_select):
    api_key = api_key_input
    df = df_input
    df['direccion'] = df['direccion'].astype(str)
    df['direccion2'] = df['direccion'].apply(lambda x: unidecode.unidecode(x))
    df['direccion2']= df['direccion2'].replace('[^a-zA-Z0-9 ]', '', regex=True)
    df['comuna'] = df['comuna'].apply(lambda x: unidecode.unidecode(x))
    df['comuna']= df['comuna'].replace('[^a-zA-Z0-9 ]', '', regex=True)
    df['comuna'] = df['comuna'].str.title()
    df['comuna'] = df['comuna'].replace(r'\s+', ' ', regex=True)
    df['comuna'] = df['comuna'].replace(r"^ +| +$", r"", regex=True)
    df['direccion_completa'] = df['direccion2'] + ", " + df['comuna'] +", "+ reg_select + ", Chile"
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

    def get_Mapbox_type(x):
        if hasattr(x,'raw') and (x.raw['properties'] is not None): 
            return x.raw['properties']

    geolocator = MapBox(api_key=api_key, timeout=1)
    geolocate_column = df0['direccion_completa'].apply(geolocator.geocode)
    df0['direccion_api'] = geolocate_column.apply(get_address)
    df0['tipo_ubicacion'] = geolocate_column.apply(get_Mapbox_type)
    df0['tipo_ubicacion'] = df0['tipo_ubicacion'].astype(str)
    df0['lat'] = geolocate_column.apply(get_latitude)
    df0['long'] = geolocate_column.apply(get_longitude)

    df0.drop(['direccion2'],axis='columns', inplace=True)
    df0 = (df0[["direccion_completa", "direccion_api", "tipo_ubicacion", "lat", "long"]])

    df1 = pd.merge(df, df0, on="direccion_completa", how="left")
    df1.drop(['direccion2'],axis='columns', inplace=True)

    df1['long'] = df1['long'].astype(str)
    df1['lat'] = df1['lat'].astype(str)

    df1["lat1"] = df1["lat"].str[:3].astype(str)
    df1["long1"] = df1["long"].str[:3].astype(str)

    df1["lat2"] = df1["lat"].str[4:10].astype(str)
    df1["long2"] = df1["long"].str[4:10].astype(str)

    df1["latitud"] = df1["lat1"] + "," + df1["lat2"]
    df1["longitud"] = df1["long1"] + "," + df1["long2"]

    df1['long'] = pd.to_numeric(df1['long'],errors='coerce')
    df1['lat'] = pd.to_numeric(df1['lat'],errors='coerce')

    puntos = gpd.GeoDataFrame(
        df1, geometry=gpd.points_from_xy(df1.long , df1.lat))
    puntos.set_crs(epsg=4326, inplace=True)

    url = "https://www.dropbox.com/s/v5pbqsbtuqzu54c/comunas_rm_geo.geojson?dl=1"

    comunas = gpd.read_file(url)

    puntos_j = gpd.sjoin(puntos, comunas, how="left", predicate='intersects')

    join = pd.DataFrame(puntos_j)

    join.drop(['geometry', 'index_right', 'lat1', 'lat2', 'long1', 'long2'], axis='columns', inplace=True)

    join['comuna_geo'] = join['comuna_geo'].astype(str)
    join['comuna_geo'] = join['comuna_geo'].apply(lambda x: unidecode.unidecode(x))

    join['comunas_rev'] = np.where(join['comuna'] == join['comuna_geo'], "coincide", "no coincide")   

    join["api_consulta"] = 'Mapbox'

    join = join[["id", "direccion","direccion_completa", "direccion_api", "tipo_ubicacion", "comuna",
    "comuna_geo", "comunas_rev","lat", "long", "latitud", "longitud", "api_consulta"]]   

    return join



def display_map(df):
    fig = px.scatter_mapbox(df, lat='lat', lon='long', hover_name="id", 
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

    region_select = st.selectbox('Seleccione un Región:', options=opciones_region, index=6)
    
    api_key_input = st.text_input(label="Ingrese API key", type="password")
    if api_key_input:
        if st.button('Comenzar'):
            st.write("Comienza la geocodificación...")
            join = CONSULTA_API_MAPBOX(api_key_input, df, region_select)

            with st.spinner('El proceso está terminando...'):
                time.sleep(5)
            st.success('Listo!')
            st.plotly_chart(display_map(join), use_container_width=True)

            csv_salida = convert_df(join)

            st.download_button(
            "Descargue resultado",
            csv_salida,
            "resultado_API_MAPBOX.csv",
            "text/csv",
            key='download-csv-mapbox')

link_rev = '[Revision resultados](https://fportalesor-app-geocoding-main-z8y7n3.streamlit.app/Revision_resultados)'

with st.sidebar:
        st.markdown("#### Instrucciones de uso")
        st.markdown(f"""##### 
1) Descargar archivo de referencia para cargar datos con el formato solicitado.
2) Dar click en "Browse files" o en "Drag and drop file here" para cargar el archivo csv con los datos.
3) Ingresar Api key y luego presionar Enter.
4) Dar click en el botón Comenzar.
5) Se mapean los resultados obtenidos.
6) Dar click en "Descargue resultado". 
7) Puede visitar el módulo "{link_rev}" para utilizar la herramienta de validación disponible."""
, unsafe_allow_html=True)
        



