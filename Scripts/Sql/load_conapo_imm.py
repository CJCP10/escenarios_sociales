

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


# Configuración para conexión
user='root'
password='sesnA2024$'
host='localhost'
database='psociales'


# coneccion con mysql 
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
cursor.execute('DROP TABLE IF EXISTS conapo_IMM')
# Generación de tabla
cursor.execute("""create TABLE conapo_IMM(
    year INT,
    cve_ent  varchar(60) NOT NULL,
    cve_mun  varchar(60) NOT NULL,
    pob_tot INT,
    analf FLOAT,
    sbasc FLOAT,
    ovsde FLOAT,
    ovsee FLOAT,
    ovsae FLOAT,
    ovpt FLOAT,
    vhac FLOAT,
    pl5000 FLOAT,
    po2sm FLOAT,
    im FLOAT, 
    gm varchar(20),
    imn float,
    KEY (cve_ent),
    KEY (cve_mun)
)
""")

db.commit()
print("Table creada exitosamente!!!")

# lectura de base en formato xlsx
base = pd.read_csv('./bases/IMM.csv', converters={'cve_ent':str, 'cve_mun':str})
# procesamiento
base['year'] = base['year'].astype('int') 
base['cve_ent'] = base['cve_ent'].astype('str')
base['cve_mun'] = base['cve_mun'].astype('str')
base['pob_tot'] = base['pob_tot'].astype('int')
base['analf'] = base['analf'].astype('float')
base['sbasc'] = base['sbasc'].astype('float')
base['ovsde'] = base['ovsde'].astype('float')
base['ovsee'] = base['ovsee'] .astype('float')
base['ovsae'] = base['ovsae'].astype('float')
base['ovpt'] = base['ovpt'].astype('float')
base['vhac'] = base['vhac'].astype('float')
base['pl5000'] = base['pl.5000'].astype('float')
base['po2sm'] = base['po2sm'].astype('float')
base['im'] = base['im'].astype('float')
base['gm'] = base['gm'].astype('str')
base['imn'] = base['imn'].astype('float')
#base = base.fillna('NA')
print('Procesamiento exitoso!!')

# El siguiente paso consite en subir los datos a la tabla siacon_agro
#  para ello, previamente debe estar creada la tabla siacon_agro en 
#  mysql
query = """INSERT INTO conapo_IMM(year,cve_ent, cve_mun,
    pob_tot, analf, sbasc, ovsde, ovsee, ovsae, ovpt, vhac, 
    pl5000, po2sm, im, gm, imn) 
    VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

for i, row in base.iterrows():
    #print(row)
    year = row['year'],
    ent = row['cve_ent'],
    mun = row['cve_mun'],
    pob_total = row['pob_tot'],
    analf = row['analf'],
    sbasc = row['sbasc'],
    ovsde = row['ovsde'],
    ovsee = row['ovsee'],
    ovesae = row['ovsae'],
    ovpt = row['ovpt'],
    vhac = row['vhac'],
    pl5000 = row['pl5000'],
    po2sm = row['po2sm'],
    im = row['im'],
    gm = row['gm'],
    imn = row['imn']

    values = (year[0], ent[0], mun[0], pob_total[0],analf[0],sbasc[0],
              ovsde[0],ovsee[0],ovesae[0],ovpt[0],vhac[0], pl5000[0], po2sm[0],
              im[0], gm[0], imn)


    #print(values)
    cursor.execute(query.encode("utf-8"), values)
    
    #print(idx)
cursor.close()

db.commit()

print("Carga exitosa!!!")