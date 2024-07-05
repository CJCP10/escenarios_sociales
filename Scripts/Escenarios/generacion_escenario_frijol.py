import pandas as pd
import numpy as np

# importa función para generar escenario precio
from f_escenarios import get_escenario

# producto _ frijol
producto_nombre = 'frijol' 
# monto apoyo productor
monto_apoyo = 14500
# apoyo flete productor
apoyo_flete = 0
# presupuesto ejercido producto
monto_total_producto = 109359921.56




anio = 2022
idcultivo = 6840000


###############################################################################################
#                              lectura y unión de bases                                       #
###############################################################################################


# Base población objetivo
df_producto = pd.read_csv('../../Data/Productores/bprod_'+producto_nombre+'.csv', converters={'cve_ent':str,'cve_mun':str })
df_producto = df_producto.drop('Unnamed: 0', axis=1)
# base marginacion
df_margina = pd.read_csv('../../Data/IMM.csv', converters={'cve_ent':str,'cve_mun':str })
df_margina = df_margina[df_margina['year']==2020]
df_margina = df_margina[['cve_ent', 'cve_mun', 'gm', 'imn']]
df = df_producto.merge(df_margina, on=['cve_ent', 'cve_mun'], how='left')

# Base siacon
names_siacon = ['year', 'cve_ent', 'cve_mun', 'idcultivo','idmodalidad','idciclo', 'precio']
df_siacon = pd.read_csv('../../Data/DBEstProdAgricola.csv', usecols=names_siacon, converters={'cve_ent':str, 'cve_mun':str})


# copia debase df
df2 = df.copy()
# filtro year
df_siacon = df_siacon[df_siacon['year']==anio]
df_siacon = df_siacon.drop('year', axis=1)
# filtro idcultivo
df_siacon = df_siacon[df_siacon['idcultivo']==idcultivo]
df_siacon = df_siacon.drop('idcultivo', axis=1)

  ##### No se necesitan para frijol estos filtroa #####
# filtro modalidad
#df_siacon = df_siacon[df_siacon['idmodalidad']==idmodalidad]
#df_siacon = df_siacon.drop('idmodalidad', axis=1)
# filtro ciclo 
#df_siacon = df_siacon[df_siacon['idciclo']==idciclo]
#df_siacon = df_siacon.drop('idciclo', axis=1)

# promedio por entidad
df_siacon = df_siacon.groupby(['cve_ent', 'cve_mun']).agg({'precio':"mean"}).reset_index()


#############################################################################################
#                                  Estimación de escenario marginación                      #
#############################################################################################

# monto apoyo estimado
df['monto_apoyo_estimado'] = df['produccion_total']*(monto_apoyo + apoyo_flete)
# ordenamos de forma ascendente el imn
df = df.sort_values('imn', ascending=True)
# escenario
escenario_m = get_escenario(df['monto_apoyo_estimado'].to_list(), monto_total_producto)
df['Escenario_marginacion'] = escenario_m

##############################################################################################
#                                      Estimación de escenario precio                        #
##############################################################################################

# merge siacon
df2 = df.copy()
df2 = df2.merge(df_siacon, on=['cve_ent', 'cve_mun'], how='left')
# imputamos por 
df2['precio'] = df_siacon[['cve_ent','precio']].groupby("cve_ent").transform(lambda x: x.fillna(x.mean()))
# orden por precio
#df2 = df2.sort_values('precio', ascending=True)
df2 = df2.replace(0, float('inf')).sort_values('precio', ascending=True).replace(float('inf'), 0)  # Cómo tenemos municipios con precios 0

# calculo de escenario
escenario_precio = get_escenario(df['monto_apoyo_estimado'].to_list(), monto_total_producto)
df2['Escenario_precio'] = escenario_precio

# filtramos columnas 
ordercols = ['cve_ent','cve_mun', 'productores', 'produccion_total','gm', 'imn', 'precio','Escenario_marginacion', 'Escenario_precio']
df2 = df2[ordercols]

# salvamos resultado
df2.to_csv('../../Data/Escenarios/escenarios_'+producto_nombre+'.csv', index=False)


print('\n-- Generación de escenarios con éxito --')