import os
import streamlit as st
import pandas as pd
import time
import gdown
from deepparse.dataset_container import CSVDatasetContainer
from deepparse.parser import AddressParser



st.set_page_config(page_title="Formateador de direcciones")

st.markdown("# Formateador de direccioness")

df_ejemplo = pd.read_csv("archivo_ejemplo_formateador.csv", dtype=str, sep=";", encoding="latin-1")

def convert_df(df):
    return df.to_csv(index=False, sep=";").encode('cp1252')

csv = convert_df(df_ejemplo)

if "model" not in st.session_state.keys():
    file_id = st.secrets["MODEL"]
    url = f'https://drive.google.com/uc?id={file_id}'
    
    st.write("El modelo se está cargando...")
    gdown.download(url, quiet=False)

    address_parser = AddressParser(
    model_type="fasttext",
    device=0,
    path_to_retrained_model="CLParser.ckpt",
    )
    st.session_state["model"] = address_parser
    with st.spinner('El proceso está terminando...'):
        time.sleep(3)
    st.success('Modelo cargado')

model = st.session_state["model"]

@st.cache_resource()
def process(df_input):
    df = df_input
    df['Direccion'] = df['direccion'].fillna("") + " SANTIAGO"
    df['Direccion'] = df['Direccion'].replace('[^a-zA-Z0-9 ]', '', regex=True)
    df['Direccion'] = df['Direccion'].str.upper()
    df['Direccion'] = df['Direccion'].replace(r'\s+', ' ', regex=True)
    df['Direccion'] = df['Direccion'].str.strip()

    # SE FILTRAN REGISTROS NULOS
    df = df.loc[df["Direccion"].notna()]
    df = df.loc[df["Direccion"] != ""]

    lista = df['Direccion'].tolist()

    parsed_addresses = model(lista)

    fields = ['StreetNumber', 'StreetName', 'Municipality']
    parsed_address_df= pd.DataFrame([parsed_address.to_dict(fields=fields) for parsed_address in parsed_addresses],
                                         columns=fields)

    df = pd.concat([df, parsed_address_df], axis=1)
    df = df.drop(columns=["Direccion", "Municipality"])
    
    return df

 
container = st.container()

with container:

    st.download_button(
        "Descargue archivo de referencia",
        csv,
        "Archivo de referencia.csv",
        "text/csv",
        key='download-csv-ref')
    

container2 = st.container()

with container2:
    
    uploaded_file = st.file_uploader("Elija un archivo csv para realizar la geocodificación", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file, dtype=str, sep=";", encoding="latin-1")
        
        if st.button('Iniciar proceso'):
            st.write("Comienza el proceso...")
            result = process(df)
            with st.spinner('El proceso está terminando...'):
                 time.sleep(3)
            st.success('Listo!')

            csv_salida = convert_df(result)

            st.download_button(
            "Descargue resultado",
            csv_salida,
            "resultado_estandarizacion.csv",
            "text/csv",
            key='download-csv-std')
    

with st.sidebar:
        st.markdown("#### Instrucciones de uso")
        st.markdown(f"""##### 
1) Espere hasta que el modelo se haya cargado.
2) Descargar archivo de referencia para cargar datos con el formato solicitado.
3) Dar click en "Browse files" o en "Drag and drop file here" para cargar el archivo csv con los datos.
4) Dar click en el botón Iniciar proceso.
5) Dar click en "Descargue resultado". 
"""
, unsafe_allow_html=True)
