import streamlit as st
import pandas as pd
from geopy.geocoders import ArcGIS
import unidecode
import numpy as np
import geopandas as gpd
import plotly.express as px
import time


st.set_page_config("Geocodificación API Arcgis")

st.markdown("""<p style="text-align:center;"><img src="https://community.esri.com/t5/image/serverpage/image-id/3157i061FF76E2EA3111A?v=v2"
alt="whatever" width="160" height= "160"></p>""", unsafe_allow_html=True)

st.markdown("---")

df_ejemplo = pd.read_csv("archivo_ejemplo.csv", dtype=str, sep=";", encoding="latin-1")

def convert_df(df):
   return df.to_csv(index=False, sep=";").encode('latin-1')

csv = convert_df(df_ejemplo)

@st.cache_data()
def CONSULTA_API_ARCGIS(username_input,password_input, df_input):
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

    def get_Arcgis_type(x):
        if hasattr(x,'raw') and (x.raw["attributes"]["Addr_type"] is not None): 
            return x.raw["attributes"]["Addr_type"]

    geolocator = ArcGIS(username= username_input, password=password_input,
    referer="https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates?", timeout=1)
    fieldList= 'address', 'location', 'Addr_type'
    geolocate_column = df0['direccion_completa'].apply(geolocator.geocode, out_fields= fieldList)
    df0['direccion_api'] = geolocate_column.apply(get_address)
    df0['tipo_ubicacion'] = geolocate_column.apply(get_Arcgis_type)
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

    url = "https://www.dropbox.com/s/f0ck8en4qdrff9c/comunas_chile_geo.geojson?dl=1"

    comunas = gpd.read_file(url)

    puntos_j = gpd.sjoin(puntos, comunas, how="left", predicate='intersects')

    join = pd.DataFrame(puntos_j)

    join.drop(['geometry', 'index_right', 'lat1', 'lat2', 'long1', 'long2'], axis='columns', inplace=True)

    join['comuna_geo'] = join['comuna_geo'].astype(str)
    join['comuna_geo'] = join['comuna_geo'].apply(lambda x: unidecode.unidecode(x))

    join['comunas_rev'] = np.where(join['comuna'] == join['comuna_geo'], "coincide", "no coincide")

    join["api_consulta"] = 'Arcgis'

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
        key='download-csv-Arcgis')

    uploaded_file = st.file_uploader("Elija un archivo csv para realizar la geocodificación", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file, dtype=str, sep=";", encoding="latin-1")
    
    un_input = st.text_input(label="Ingrese Nombre de usuario")
    pw_input = st.text_input(label="Ingrese contraseña", type="password")
    if pw_input:
        if st.button('Comenzar'):
            st.write("Comienza la geocodificación...")
            join = CONSULTA_API_ARCGIS(un_input, pw_input, df)

            with st.spinner('El proceso está terminando...'):
                time.sleep(5)
            st.success('Listo!')
            st.plotly_chart(display_map(join), use_container_width=True)

            csv_salida = convert_df(join)

            st.download_button(
            "Descargue resultado",
            csv_salida,
            "resultado_API_Arcgis.csv",
            "text/csv",
            key='download-csv-arcgis')


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
