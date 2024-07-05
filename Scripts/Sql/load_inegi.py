


# !pip install mysql.connector
# !pip install requests
import pandas as pd
import numpy as np
import requests
from sqlalchemy import create_engine
import sys
import pymysql
import mysql
import mysql.connector
import math

############################################################################
#                        Configuración para Conexión 
############################################################################
user='root'
password='sesnA2024$'
host='localhost'
database='psociales'


# coneccion con MySQL
db= mysql.connector.connect(user=user, 
                            password=password,
                            host=host,
                            database=database)
#cnx.close()

cursor = db.cursor()

##############################################################################
#                       Creación de tabla en MySQl
##############################################################################
# Si existe previamente la tabla inegi la elimina
cursor.execute('DROP TABLE IF EXISTS inegi')
# Genera la tabla inegi
cursor.execute("""create TABLE inegi(
    cvegeo varchar(20),
    cve_ent varchar(60) NOT NULL,
    entidad varchar(120) NOT NULL,
    entidad_abrev varchar(60),
    cve_mun varchar(60) NOT NULL,
    municipio varchar(120),
    cve_loc	varchar(60) NOT NULL,
    localidad varchar(120),
    ambito varchar(60),
    latitud	float,
    longitud float,
    altitud	varchar(60),
    pob_ent int,
    pob_fem_ent int,
    pob_mas_ent int,	    
    viv_ent int, 
    pob_mun int,
    pob_fem_mun int,
    pob_mas_mun int,
    viv_mun int, 
    pob_loc float,
    viv_loc float, 
    PRIMARY KEY (cvegeo),
    KEY (cve_ent, cve_mun, cve_loc),
    KEY (cve_ent, cve_mun),
    KEY (cve_ent),
    KEY (cve_mun),
    KEY (cve_loc)
    
)
""")

db.commit()
print("Table creada exitosamente!!!")
##############################################################################
#                       Subida a Base de Datos
##############################################################################
# lectura de base en formato xlsx
base = pd.read_csv('./bases/MGE.csv', converters={'cve_ent':str, 'cve_mun':str, 'cve_loc':str,'cvegeo':str, 'altitud':str})
# procesamiento
base['cvegeo'] = base['cvegeo'].astype('str')
base['cve_ent'] = base['cve_ent'].astype('str')
base['entidad'] = base['entidad'].astype('str')
base['entidad_abrev'] = base['entidad_abrev'].astype('str')
base['cve_mun'] = base['cve_mun'].astype('str')
base['municipio'] = base['municipio'].astype('str')
base['cve_loc'] = base['cve_loc'].astype('str')
base['localidad'] = base['localidad'].astype('str')
base['ambito'] = base['ambito'].astype('str')
base['latitud'] = base['latitud'].astype('float')
base['longitud'] = base['longitud'].astype('float')
base['altitud'] = base['altitud'].astype('str')
base['pob_ent'] = base['pob_ent'].astype('int')
base['pob_fem_ent'] = base['pob_fem_ent'].astype('int')
base['pob_mas_ent'] = base['pob_mas_ent'].astype('int')
base['viv_ent'] = base['viv_ent'].astype('int')
base['pob_mun'] = base['pob_mun'].replace('NA',np.nan).replace('*',np.nan).replace('-',np.nan)
base['pob_fem_mun'] = base['pob_fem_mun'].replace('NA',np.nan).replace('*',np.nan).replace('-',np.nan)
base['pob_mas_mun'] = base['pob_mas_mun'].replace('NA',np.nan).replace('*',np.nan).replace('-',np.nan)
base['viv_mun'] = base['viv_mun'].replace('NA',np.nan).replace('*',np.nan).replace('-',np.nan)
base['pob_loc'] = base['pob_loc'].replace('NA',np.nan).replace('*',np.nan).replace('-',np.nan).astype('float')
base['viv_loc'] = base['viv_loc'].replace('NA',np.nan).replace('*',np.nan).replace('-',np.nan).astype('float')


# El siguiente paso consite en subir los datos a la tabla siacon_agro
#  para ello, previamente debe estar creada la tabla siacon_agro en 
#  mysql
query = """INSERT INTO inegi (cvegeo, cve_ent, entidad, entidad_abrev, cve_mun,
    municipio, cve_loc, localidad, ambito, latitud, longitud, altitud, pob_ent,
    pob_fem_ent, pob_mas_ent, viv_ent, pob_mun, pob_fem_mun, pob_mas_mun, viv_mun,
    pob_loc, viv_loc) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s)"""

for i, row in base.iterrows():
    #print(row)
    cve_geo = row['cvegeo']
    cve_ent = row['cve_ent']
    nom_ent = row['entidad']
    nom_abr = row['entidad_abrev']
    cve_mun = row['cve_mun']
    nom_mun = row['municipio']
    cve_loc = row['cve_loc']
    nom_loc = row['localidad']
    ambito = row['ambito']
    lat = row['latitud']
    lon = row['longitud']
    alt = row['altitud']
    pob_ent = row['pob_ent']
    pob_fem_ent = row['pob_fem_ent']
    pob_mas_ent = row['pob_mas_ent']
    viv_ent = row['viv_ent']
    pob_mun = np.where(math.isnan(row['pob_mun']),None, row['pob_mun']).tolist() #row['pob_mun']
    pob_fem_mun = np.where(math.isnan(row['pob_fem_mun']),None, row['pob_fem_mun']).tolist() #row['pob_fem_mun']
    pob_mas_mun = np.where(math.isnan(row['pob_mas_mun']),None, row['pob_mas_mun']).tolist() #row['pob_mas_mun']
    viv_mun = np.where(math.isnan(row['viv_mun']),None, row['viv_mun']).tolist() #row['viv_mun'] 
    pob_loc = np.where(math.isnan(row['pob_loc']),None, row['pob_loc']).tolist() # row['pob_loc']
    viv_loc = np.where(math.isnan(row['viv_loc']),None, row['viv_loc']).tolist() #row['viv_loc']
    #print(f'{idx[0]}')
    
    values = (cve_geo, cve_ent, nom_ent, nom_abr, cve_mun, nom_mun, 
              cve_loc, nom_loc, ambito, lat, lon, alt, pob_ent, pob_fem_ent, 
              pob_mas_ent, viv_ent, pob_mun, pob_fem_mun, pob_mas_mun, viv_mun, 
              pob_loc, viv_loc)
    #print(values)
    cursor.execute(query, values)
    #print(idx)
cursor.close()

db.commit()

###############################
print("Carga exitosa!!!")