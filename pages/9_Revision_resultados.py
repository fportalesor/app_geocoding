import streamlit as st
import pandas as pd
import plotly.express as px
import unidecode
import geopandas as gpd
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode

st.set_page_config("Revisión de resultados", layout="wide")

st.markdown("# Revisión de resultados")

st.markdown("")



@st.cache_data()
def display_map(df):
    fig = px.scatter_mapbox(df, lat='lat', lon='long', color_discrete_sequence= ["red"],
                            hover_data=["direccion_completa", "direccion_api", "tipo_ubicacion"], hover_name="id", 
                            color="tipo_ubicacion",zoom=17, mapbox_style= 'open-street-map', height=500)
    fig.update_traces(marker={'size': 15})

    
    return fig

@st.cache_data()
def std_app(df):
    condicion1 = df['comuna'] == df['comuna_geo']
    lista_validas = ["{'accuracy': 'point'}", "{'accuracy': 'interpolated'}", "ROOFTOP", "RANGE_INTERPOLATED",
                      "Point Address", "Address Range", "houseNumber", "Address", "building", "POINT", "ADDRESS",
                      "PointAddress", "StreetAddress", "StreetAddressExt"]
    condicion2 = df['tipo_ubicacion'].isin(lista_validas)   
    df["ubicación_válida"] = np.where((condicion1) & (condicion2), True, False)
    df = df[["ubicación_válida","id","direccion", "direccion_completa", "direccion_api", "tipo_ubicacion", "comuna",
                              "comuna_geo", "comunas_rev","lat", "long", "latitud", "longitud", "api_consulta"]]
    df['long'] = df['long'].astype(str)
    df['lat'] = df['lat'].astype(str)

    df['long'] = df['long'].str.replace('.', '')
    df['lat'] = df['lat'].str.replace('.', '')

    df["lat1"] = df["lat"].str[:3].astype(str)
    df["long1"] = df["long"].str[:3].astype(str)

    df["lat2"] = df["lat"].str[3:15].astype(str)
    df["long2"] = df["long"].str[3:15].astype(str)

    df["lat"] = df["lat1"] + "." + df["lat2"]
    df["long"] = df["long1"] + "." + df["long2"]

    df["lat"] = df["lat"].astype(float)
    df["long"] = df["long"].astype(float)
     
    df.drop(columns=["lat1", "long1", "lat2", "long2"], inplace=True)
   
    return df


@st.cache_data()
def std_midas(df):
    cols = ['id', 'via', 'region', 'comuna', 'direccion', 'direccion_completa', 'lat', 'long', 'direccion_api', 'tipo_ubicacion', 'otro']
    df.columns = cols
    df['direccion_completa'] = df['direccion_completa'].apply(lambda x: unidecode.unidecode(x))
    df['direccion_completa']= df['direccion_completa'].replace('[^a-zA-Z0-9 ]', '', regex=True)
    df['comuna'] = df['comuna'].apply(lambda x: unidecode.unidecode(x))
    df['comuna']= df['comuna'].replace('[^a-zA-Z0-9 ]', '', regex=True)
    df['comuna'] = df['comuna'].str.title()
    df['comuna'] = df['comuna'].replace(r'\s+', ' ', regex=True)
    df['comuna'] = df['comuna'].replace(r"^ +| +$", r"", regex=True)
    
    df['long'] = df['long'].astype(str)
    df['lat'] = df['lat'].astype(str)

    df["lat1"] = df["lat"].str[:3].astype(str)
    df["long1"] = df["long"].str[:3].astype(str)

    df["lat2"] = df["lat"].str[4:12].astype(str)
    df["long2"] = df["long"].str[4:12].astype(str)
      
    df["latitud"] = df["lat1"] + "," + df["lat2"]
    df["longitud"] = df["long1"] + "," + df["long2"]

    puntos = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.long , df.lat))
    puntos.set_crs(epsg=4326, inplace=True)

    url = "https://www.dropbox.com/s/f0ck8en4qdrff9c/comunas_chile_geo.geojson?dl=1"

    comunas = gpd.read_file(url)

    puntos_j = gpd.sjoin(puntos, comunas, how="left", predicate='intersects')

    join = pd.DataFrame(puntos_j)

    join.drop(['geometry', 'index_right', 'lat1', 'lat2', 'long1', 'long2'], axis='columns', inplace=True)
                
    join['comuna_geo'] = join['comuna_geo'].astype(str)
    join['comuna_geo'] = join['comuna_geo'].apply(lambda x: unidecode.unidecode(x))


    join['comunas_rev'] = np.where(join['comuna'] == join['comuna_geo'], "coincide", "no coincide")     

    join["api_consulta"] = ''

    condicion1 = join['comuna'] == join['comuna_geo']
    lista_validas = ["{'accuracy': 'point'}", "{'accuracy': 'interpolated'}", "ROOFTOP", "RANGE_INTERPOLATED",
                      "Point Address", "Address Range", "houseNumber", "Address", "building", "POINT", "ADDRESS",
                      "PointAddress", "StreetAddress", "StreetAddressExt"]
    condicion2 = join['tipo_ubicacion'].isin(lista_validas)
    join["ubicación_válida"] = np.where((condicion1) & (condicion2), True, False)
    join = join[["ubicación_válida","id","direccion", "direccion_completa", "direccion_api", "tipo_ubicacion", "comuna",
                              "comuna_geo", "comunas_rev","lat", "long", "latitud", "longitud", "api_consulta"]]
    
    return join

def convert_df(df):
   #return df.to_csv(index=False, sep=";").encode('latin-1')
   return df.to_csv(index=False, sep=";").encode('cp1252')


checkbox_renderer = JsCode("""
class CheckboxRenderer{

    init(params) {
        this.params = params;

        this.eGui = document.createElement('input');
        this.eGui.type = 'checkbox';
        this.eGui.checked = params.value;

        this.checkedHandler = this.checkedHandler.bind(this);
        this.eGui.addEventListener('click', this.checkedHandler);
    }

    checkedHandler(e) {
        let checked = e.target.checked;
        let colId = this.params.column.colId;
        this.params.node.setDataValue(colId, checked);
    }

    getGui(params) {
        return this.eGui;
    }

    destroy(params) {
    this.eGui.removeEventListener('click', this.checkedHandler);
    }
}//end class
""")

opciones_csv = st.radio(
    "¿Cúal tipo de archivo usarás?",
    ('Por defecto APP', 'Geomasiva Midas'))

if opciones_csv == 'Por defecto APP':
    file = st.file_uploader("Elija un archivo csv con los resultados para realizar la revisión", type="csv", key="file1")
    if file is not None:
        ##df = pd.read_csv(file, sep=";", encoding="cp1252")
        df = pd.read_csv(file, sep=";", errors="ignore")
        df = df.loc[(df['lat'].notna()) & (df['lat'] != '')]
        df= std_app(df)

else:
    file = st.file_uploader("Elija un archivo con los resultados para realizar la revisión",key="file2")
    if file is not None:
        df = pd.read_csv(file, sep=";", encoding="utf-8", header=None)
        df = df.loc[(df['lat'].notna()) & (df['lat'] != '')]
        df = std_midas(df)
        
    
if file is not None:
    
        st.markdown("#### Selecciona una fila para validar la ubicación resultante")
        col1, col2 = st.columns(2)
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(enablePivot=True, enableValue=True, enableRowGroup=True)
        gb.configure_column("ubicación_válida", editable=True, cellRenderer=checkbox_renderer)
        gb.configure_column("id", hide=True)
        gb.configure_column("direccion", hide=True)
        gb.configure_selection(selection_mode="single")
        gb.configure_side_bar()
        gridoptions = gb.build()

        response = AgGrid(
        df,
        height=500,
        width='100%',
        gridOptions=gridoptions,
        enable_enterprise_modules=True,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        fit_columns_on_grid_load=False,
        header_checkbox_selection_filtered_only=True,
        allow_unsafe_jscode=True,
        use_checkbox=True)


        v = response['selected_rows']
            
        if v:
            dfs = pd.DataFrame(v)
            direccion = dfs.iloc[0]["direccion_completa"]
            st.markdown(f'##### Resultado de la dirección: {direccion}')
            st.plotly_chart(display_map(dfs), use_container_width=True)

        df_total = pd.DataFrame(response['data'])
        df_val = df_total.loc[df_total["ubicación_válida"]]
        df_noval = df_total.loc[~df_total["ubicación_válida"]]
        with col1:
            st.markdown(f"##### Ubicaciones validadas: {len(df_val.index)}")
        with col2:
            st.markdown(f"##### Ubicaciones no validadas: {len(df_noval.index)}")
        csv_val = convert_df(df_val)
        csv_noval = convert_df(df_noval)
        st.download_button(
            label="Descargue resultados validados",
            data=csv_val,
            file_name='resultados_válidos.csv',
            mime='text/csv')
        st.download_button(
            label="Descargue resultados no validados",
            data=csv_noval,
            file_name='resultados_no_válidos.csv',
            mime='text/csv')


with st.sidebar:
        st.markdown("#### Instrucciones de uso")
        st.markdown(f"""##### 
1) Seleccionar el tipo de archivo a cargar.
2) Dar click en "Browse files" o en "Drag and drop file here" para cargar el archivo con los resultados.
3) Se visualizará una tabla con los datos cargados. Por defecto, las ubicaciones que se definen como válidas (ticket azul) son:

    a) Direcciones donde la comuna de entrada y la comuna georreferenciada coinciden.
    
    b) El tipo de ubicación coincide con los homólogos de mayor precisión de Google, los cuales son Rooftop y Range Interpolated.

4) Para revisar en detalle la ubicación de un resultado, da click en una fila. Se visualizará un mapa con la ubicación de la dirección geolocalizada.
5) En las filas de la columna "ubicación_valida" podrás prender el ticket azul para dejar una dirección válida. Lo contrario para dejar como no válida.

6) Tras finalizar la revisión puedes descargar los datos validados y no validados por separado, dando click en los botones que se encuentran al final de la página.
"""
, unsafe_allow_html=True)
        
