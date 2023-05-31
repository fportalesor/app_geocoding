import streamlit as st


st.set_page_config("API_keys")


st.markdown("""
## 1) Mapbox

- Para crear su token de acceso debe ingresar a www.mapbox.com . En el costado superior derecho encontrará la opción para registrarse y crear una cuenta (Sign up).
- La cuenta se activará una vez ingrese al link de verificación que se envió al e-mail que registró.
- Con la cuenta activada podrá iniciar sesión. En la página principal (https://account.mapbox.com/) encontrará el token de acceso público (referencia en la figura 2). Este se debe copiar y pegar en la aplicación.


""", unsafe_allow_html=True)
            
st.image("https://raw.githubusercontent.com/fportalesor/app_geocoding/blob/e1428d852095558ba65b05de7301e466fc026a34/images/4.png", caption= '80-day sale data', width=550)

st.markdown(            
"""
## 2)	Google

- Para crear su token de acceso debe ingresar a https://cloud.google.com/ y dar click en "Empezar gratis".
- Ingresar con una cuenta de gmail.
- Ingresar los datos solicitados y aceptar las condiciones de servicio. Dar click a continuar. En el paso 2 se solicita información de contacto. Verificar el contacto con código enviado al celular. En el paso 3 se solicita validar información de pago. Debe ingresar datos de una tarjeta de crédito o débito.
- Luego de haber ingresado sus datos su cuenta gmail estará vinculada. Para visualizar o crear su api key debe dirigirse a https://console.cloud.google.com/projectselector2/apis/credentials?. Allí deberá seleccionar la opción "My First Project". En la nueva página encontrará la opción "CREAR CREDENCIALES". Luego seleccionar "Clave de API". Finalmente debe dar click en el nombre de la clave API y allí encontrará el dato a copiar.


<p align="center">
<img src="7.png"  width="550" height="210">
</p>

## 3)	TomTom

- Para crear su token de acceso debe ingresar a https://developer.tomtom.com/. En el costado superior derecho encontrará la opción para registrarse y crear una cuenta (Register).
- La cuenta se activará una vez ingrese al link de verificación que se envió al e-mail que registró. Luego ir a la sección Dashboard y encontrará la API Key que se entrega por defecto.


<p align="center">
<img src="5.png"  width="550" height="300">
</p>


## 4)	Here

- Para crear su token de acceso debe ingresar a https://developer.here.com/ y dar click en "Get started for free".
- Ingresar los datos que se solicitan en el formulario y luego dar click "Verify email". Llegará un mensaje al correo electrónico ingresado. En el mensaje dar click en "Verify email". Será redireccionado a página web que solicita ingresar país y contraseña. Luego de leer los términos de HERE, dar click en el botón "Next".
- Luego vienen las opciones de facturación, las cuales se pueden saltar o sino, agregar los datos necesarios. Tras seleccionar una de las opciones finalizará la configuración de la cuenta.
- Para obtener el token de acceso o api key, ingresar a https://platform.here.com/admin/apps. Dar click en "Register new app". Ingresar un nombre. En la opción default access to a project, seleccionar No Project (en principio. De igual modo lo puede asociar a un proyecto). Luego dar click en Register.
- En el costado derecho de la nueva página web, dar click en API Keys y luego en Create API Key.
- Luego copiar la Api key tal como se muestra en la siguiente imagen.

<p align="center">
<img src="9.png"  width="550" height="180">
</p>

## 5)	Bing


- Para crear su token de acceso debe ingresar a https://www.bingmapsportal.com/ y dar click en "Sign in".
- Ingresar con una cuenta de Microsoft (hotmail, outlook).
- En la siguiente página debe dar click en "Yes, let's create a new account" e ingresar los datos solicitados en el formulario  y dar. Finalmente dar click en create.
- Una vez ingresados los datos de la cuenta debe dirigirse a  "My account" y luego a "My Keys". Se solicitará el nombre de la aplicación (puede ser cualquiera), URL de la aplicación (no es necesario ingresar este dato) y en Application type mantener la opción "Dev/Test". Finalmente dar click en "Create".
- Con la API KEY creada sólo queda dar click en "Copy key" para luego ingresar este dato dentro de la app.

<p align="center">
<img src="8.png"  width="550" height="300">
</p>

## 6)	Mapquest

- Para crear su token de acceso debe ingresar a https://developer.mapquest.com/ y dar click en "Get Started".
- Ingresar los datos solicitados en el formulario y dar click en "Sing me up".
- Ingresar código de verificación enviado al correo. Con este paso ya habrá ingresado a su cuenta.
- Para crear su API KEY debe dirigirse a https://developer.mapquest.com/user/me/apps y luego dar click en el botón "Create a New Key". En el siguiente cuadro se le solicitará un nombre de la aplicación (puede ser cualquiera) y una "Callback URL" (no es necesario rellenar ese campo). Una vez realizado lo anterior podrá encontrar dentro del nombre de la aplicación el "Cosumer Key", que corresponde al token de acceso.


<p align="center">
<img src="6.png"  width="550" height="200">
</p>

## 7)	Arcgis

""", unsafe_allow_html=True)
