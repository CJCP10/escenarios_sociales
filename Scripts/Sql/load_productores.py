

# !pip install mysql.connector
# !pip install requests
import pandas as pd
import numpy as np
#import requests
from sqlalchemy import create_engine
#import sys
import pymysql
import mysql
import mysql.connector
#import math

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

#######################################################################


# Si existe previamente la tabla Beneficiarios la elimina
cursor.execute('DROP TABLE IF EXISTS productores;')
# Generación de la tabla Beneficiarios
cursor.execute("""create table productores(
	cultivo varchar(40), 
    cve_ent	varchar(60) NOT NULL,
    cve_mun	varchar(60) NOT NULL,
    productores	int,
    produccion_total float,	
    escenario_precio float,
	escenario_marginacion float
);
""")
db.commit()

print("Table creada exitosamente!!!")
##############################################################################
#                       Subida a Base de Datos
##############################################################################

#         Unión de bases de productores
cultivos = ['Arroz', 'Frijol','Maiz','Trigo', 'Leche']
dfs = []
for cultivo in cultivos:
    dfi = pd.read_csv('./bases/bprod_'+cultivo+'.csv', converters={'cve_ent':str, 'cve_mun':str})
    dfi = dfi[['cve_ent','cve_mun','productores', 'produccion_total']]
    dfi['cultivo'] = np.where(cultivo=='Maiz','Maíz',cultivo)
    dfs.append(dfi)

# dataframe de productores    
base = pd.concat(dfs, axis=0)   

base = base.fillna(value=np.nan)
nulls = np.nan
# Procesamiento 
base['cultivo'] = base['cultivo'].astype('str').fillna(value=nulls)
base['cve_ent'] = base['cve_ent'].astype('str').fillna(value=nulls)
base['cve_mun'] = base['cve_mun'].astype('str').fillna(value=nulls)
base['productores'] = base['productores'].astype('int').fillna(value=nulls)
base['produccion_total'] = base['produccion_total'].astype('float').fillna(value=nulls)
base['escenario_precio'] = [2.10 for x in base['cultivo']] # Este es un ejemplo hay que cargar los archivos con los escenarios correctos
base['escenario_marginacion'] = [5.10 for x in base['cultivo']] # Este es un ejemplo hay que cargar los archivos con los escenarios correctos


#id, year,cve_ent, cve_mun, cve_loc, cultivo,idcultivo, nomciclo, pgarantia, preferencia, vincentivado, monto_total, tipo
query = """INSERT INTO productores (cultivo, cve_ent,cve_mun,productores,produccion_total,escenario_precio,escenario_marginacion) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)"""

for i, row in base.iterrows():
    #print(row)
    cultivo = row['cultivo']
    cve_ent = row['cve_ent'] 
    cve_mun =row['cve_mun'] 
    productores = row['productores'] 
    produccion_total = row['produccion_total'] 
    escenario_precio = row['escenario_precio'] 
    escenario_marginacion = row['escenario_marginacion'] 
    

    values = (cultivo, cve_ent, cve_mun,
              productores, produccion_total, escenario_precio,
              escenario_marginacion)
    #print(values)
    cursor.execute(query.encode("utf-8"), values)
    #print(idx)
cursor.close()

db.commit()

###############################
print("Carga exitosa!!!")