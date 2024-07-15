#################################### Para poder correr nuestro mapa en un servidor ######################################
############################################# Utilizando Dash y Folium #############################################

import pandas as pd
import numpy as np
import folium # La libreria folium es la que usaremos para construir algunos de nuestros mapas
import dash  # Libreria dash para poder cargar nuestras visualizaciones y conexiones con el servidor
from dash import dcc  
from dash import html  
from dash.dependencies import Input, Output # Libreria de dash para las dependencias que ocuparemos

# Funciones propias
from Scripts.Mapa.funciones import extraccion_escenarios 
from Scripts.Mapa.funciones import lista_coordenadas


# Función para poder extraer algun escenario, en este caso trabajeremos con arroz

productores = extraccion_escenarios('arroz')

# Crear el mapa de Folium, en un punto central y el zoom con el que queremos comenzar viendo el mapa
mapa = folium.Map(location=[19.432608, -99.133209], zoom_start=5, tiles=None) # tiles es para no mostrar el mapa predeterminado

# Cargar y añadir el archivo GeoJSON al mapa
geojson_path = 'Data/geo_estados.json'
folium.GeoJson(
    geojson_path,
    name='geojson'
).add_to(mapa)

# Añadir control de capas
folium.LayerControl().add_to(mapa)

# Añadir marcadores para cada ubicación en la lista de coordenadas, la lista de coordenadas la podemos obtener
# Con la función lista_coordenadas ( solo funciona con a estructura de los DataFrames que tenemos).
for  nombre, municipio, lat, lon in lista_coordenadas(productores):
    folium.Marker(
        location=[lat, lon],
        popup= [nombre,municipio],
        icon= folium.Icon(icon='cloud')  # Definimos un icono predeterminado  #info-sign icon predeterminado
        #icon= folium.CustomIcon('assets/prueba_2.png') #Podemos elegir algún icono que tengamos previamente descargado
    ).add_to(mapa)

# Guardar el mapa en un archivo HTML
mapa.save('mapa.html')

# # Crear la aplicación Dash
app = dash.Dash(__name__)

# # Definir el layout de la aplicación
app.layout = html.Div([
    html.H1("Mapa Interactivo con Folium y Dash"),
    html.Iframe(id='mapa', srcDoc=open('mapa.html', 'r',encoding='utf-8').read(), width='100%', height='500')
])

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=False) # Podemos cambiar a True el debug para poder visualizar errores en pantalla


