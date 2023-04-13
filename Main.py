import streamlit as st
import pandas as pd



st.set_page_config(
    page_title="APP Geocodificación",
)



st.write("# APP Geocodificación")

st.markdown("---")

st.markdown("")
st.markdown("")

link_rev = '[herramienta](http://localhost:8501/Revision_resultados)'
st.markdown('<a href="https://fportalesor-app-geocoding-main-z8y7n3.streamlit.app/" target=_top>Revision resultados</a>', unsafe_allow_html=True)
st.markdown(
    f"""
Esta aplicación permite utilizar distintos servicios de geocodificación en un mismo sitio web,
basándose principalmente en la utilización del cliente de python Geopy (https://geopy.readthedocs.io/en/stable/#).

Por otro lado, se facilita documentación y una {link_rev} para validar los resultados
que se obtienen a partir del uso de los servicios de geocodificación.

<br>

IMPORTANTE: Esta aplicación, al igual que Geopy, no es un servicio. <br>
Citando a Geopy: <br>
La codificación geográfica es proporcionada por una serie de servicios diferentes, que no están afiliados a geopy de ninguna manera.
Estos servicios proporcionan API, que cualquiera podría implementar, y geopy es solo una biblioteca que proporciona estas implementaciones
para muchos servicios diferentes en un solo paquete.

"""
, unsafe_allow_html=True)
