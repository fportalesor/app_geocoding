import streamlit as st


st.set_page_config("API_keys")

st.markdown("""
Las indicaciones entregadas en este apartado le permitirá crear una cuenta de desarrollador y una Api key (o token de acceso), con la que podrá utilizar los servicios de geocodificación de distintos proveedores, bajo las condiciones de gratuidad que estos entregan.
Los volúmenes de consultas gratuitas que se pueden realizar varía entre los distintos proveedores. En las condiciones de uso se puede encontrar dicha información.

""", unsafe_allow_html=True)

st.markdown("""
## 1) Mapbox

##### Obtención API Key
- Para crear su token de acceso debe ingresar a www.mapbox.com . En el costado superior derecho encontrará la opción para registrarse y crear una cuenta (Sign up).
- La cuenta se activará una vez ingrese al link de verificación que se envió al e-mail que registró.
- Con la cuenta activada podrá iniciar sesión. En la página principal (https://account.mapbox.com/) encontrará el token de acceso público (referencia en la figura 2). Este se debe copiar y pegar en la aplicación.

""", unsafe_allow_html=True)
            
st.image("images/4.png", width=550, use_column_width= 'always')

st.markdown("""
##### Condiciones de uso
- No solicita datos de tarjeta de crédito
- 100.000 consultas gratuitas por mes
- Sin restricción de uso por día

Referencia: https://www.mapbox.com/pricing

""", unsafe_allow_html=True)


st.markdown(            
"""
## 2)	Google

##### Obtención API Key
- Para crear su token de acceso debe ingresar a https://cloud.google.com/ y dar click en "Empezar gratis".
- Ingresar con una cuenta de gmail.
- Ingresar los datos solicitados y aceptar las condiciones de servicio. Dar click a continuar. En el paso 2 se solicita información de contacto. Verificar el contacto con código enviado al celular. En el paso 3 se solicita validar información de pago. Debe ingresar datos de una tarjeta de crédito o débito.
- Luego de haber ingresado sus datos su cuenta gmail estará vinculada. Para visualizar o crear su api key debe dirigirse a https://console.cloud.google.com/projectselector2/apis/credentials?. Allí deberá seleccionar la opción "My First Project". En la nueva página encontrará la opción "CREAR CREDENCIALES". Luego seleccionar "Clave de API". Finalmente debe dar click en el nombre de la clave API y allí encontrará el dato a copiar.
""", unsafe_allow_html=True)

st.image("images/7.png", width=550, use_column_width= 'always')

st.markdown("""
##### Condiciones de uso
- Debe ingresar datos de tarjeta de crédito
- USD 300 para el primer mes de uso (aprox. 60.000 consultas gratuitas por mes)
- USD 200 para uso mensual sin cobro (aprox. 40.000 consultas gratuitas por mes)
- Sin restricción de uso por día

Referencia: https://mapsplatform.google.com/pricing/

""", unsafe_allow_html=True)

st.markdown(            
"""
## 3)	TomTom

##### Obtención API Key
- Para crear su token de acceso debe ingresar a https://developer.tomtom.com/. En el costado superior derecho encontrará la opción para registrarse y crear una cuenta (Register).
- La cuenta se activará una vez ingrese al link de verificación que se envió al e-mail que registró. Luego ir a la sección Dashboard y encontrará la API Key que se entrega por defecto.

""", unsafe_allow_html=True)

st.image("images/5.png", width=550, use_column_width= 'always')

st.markdown("""
##### Condiciones de uso
- No solicita datos de tarjeta de crédito
- 2.500 consultas diarias gratis (75.000 por mes aprox.)

Referencia: https://developer.tomtom.com/store/maps-api

""", unsafe_allow_html=True)

st.markdown(            
"""
## 4)	Here

##### Obtención API Key
- Para crear su token de acceso debe ingresar a https://developer.here.com/ y dar click en "Get started for free".
- Ingresar los datos que se solicitan en el formulario y luego dar click "Verify email". Llegará un mensaje al correo electrónico ingresado. En el mensaje dar click en "Verify email". Será redireccionado a página web que solicita ingresar país y contraseña. Luego de leer los términos de HERE, dar click en el botón "Next".
- Luego vienen las opciones de facturación, las cuales se pueden saltar o sino, agregar los datos necesarios. Tras seleccionar una de las opciones finalizará la configuración de la cuenta.
- Para obtener el token de acceso o api key, ingresar a https://platform.here.com/admin/apps. Dar click en "Register new app". Ingresar un nombre. En la opción default access to a project, seleccionar No Project (en principio. De igual modo lo puede asociar a un proyecto). Luego dar click en Register.
- En el costado derecho de la nueva página web, dar click en API Keys y luego en Create API Key.
- Luego copiar la Api key tal como se muestra en la siguiente imagen.

""", unsafe_allow_html=True)

st.image("images/9.png", width=550, use_column_width= 'always')

st.markdown("""
##### Condiciones de uso
- No solicita datos de tarjeta de crédito
- 1.000 consultas diarias gratis (30.000 por mes aprox.)

Referencia: https://www.here.com/get-started/pricing

""", unsafe_allow_html=True)

st.markdown(            
"""
## 5)	Bing

##### Obtención API Key
- Para crear su token de acceso debe ingresar a https://www.bingmapsportal.com/ y dar click en "Sign in".
- Ingresar con una cuenta de Microsoft (hotmail, outlook).
- En la siguiente página debe dar click en "Yes, let's create a new account" e ingresar los datos solicitados en el formulario  y dar. Finalmente dar click en create.
- Una vez ingresados los datos de la cuenta debe dirigirse a  "My account" y luego a "My Keys". Se solicitará el nombre de la aplicación (puede ser cualquiera), URL de la aplicación (no es necesario ingresar este dato) y en Application type mantener la opción "Dev/Test". Finalmente dar click en "Create".
- Con la API KEY creada sólo queda dar click en "Copy key" para luego ingresar este dato dentro de la app.

""", unsafe_allow_html=True)

st.image("images/8.png", width=550, use_column_width= 'always')

st.markdown("""
##### Condiciones de uso
- No solicita datos de tarjeta de crédito
- Hasta 50.000 consultas dentro de un periodo de 24 horas
- Hasta 125.000 consultas acumuladas al año

Referencia: https://www.microsoft.com/en-us/maps/licensing

""", unsafe_allow_html=True)

st.markdown(            
"""
## 6)	Mapquest

##### Obtención API Key
- Para crear su token de acceso debe ingresar a https://developer.mapquest.com/ y dar click en "Get Started".
- Ingresar los datos solicitados en el formulario y dar click en "Sing me up".
- Ingresar código de verificación enviado al correo. Con este paso ya habrá ingresado a su cuenta.
- Para crear su API KEY debe dirigirse a https://developer.mapquest.com/user/me/apps y luego dar click en el botón "Create a New Key". En el siguiente cuadro se le solicitará un nombre de la aplicación (puede ser cualquiera) y una "Callback URL" (no es necesario rellenar ese campo). Una vez realizado lo anterior podrá encontrar dentro del nombre de la aplicación el "Cosumer Key", que corresponde al token de acceso.


""", unsafe_allow_html=True)

st.image("images/6.png", width=550, use_column_width= 'always')

st.markdown("""
##### Condiciones de uso
- No solicita datos de tarjeta de crédito
- 15.000 consultas gratuitas por mes

Referencia: https://developer.mapquest.com/plans

""", unsafe_allow_html=True)

st.markdown(            
"""
## 7)	Arcgis

##### Obtención API Key
- Para crear su token de acceso debe ingresar a https://developers.arcgis.com/ y dar click en "Start building for free".
- Ingresar los datos que piden en el formulario y dar click en Create developer account.
- En caso de haber usado la opción de Google u otra, seleccionar un modo para verificar la cuenta.
- Luego aceptar o cambiar el nombre de usuario asignado y aceptar las condiciones de uso de Esri. Dar click en Crear cuenta.
- Luego ingresar a https://developers.arcgis.com/dashboard/
- Allí se encontrará la api key creada por default. Se puede copiar tal como aparece en la siguiente imagen. En su defecto se puede crear una nueva.

""", unsafe_allow_html=True)

st.markdown("""
##### Condiciones de uso
- No solicita datos de tarjeta de crédito
- 100.000 consultas gratuitas por mes
- Sin restricción de uso por día

""", unsafe_allow_html=True)

st.image("images/10.png", width=550, use_column_width= 'always')
