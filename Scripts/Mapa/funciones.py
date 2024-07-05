import numpy as np
import pandas as pd


###############################################################################################################
################ Función para extraer del archivo escenarios las columnas necesarias ########################## 
###############################################################################################################
def extraccion_escenarios(producto_sel):

    ### Base de escenarios  ###
    producto = producto_sel
    escenarios = pd.read_csv('Data/Escenarios/escenarios_' + producto + '.csv', converters={'cve_ent':str, 'cve_mun':str})


    MGE = pd.read_csv('Data/MGE.csv', converters={'cve_ent':str, 'cve_mun':str,'cve_loc':str}) # Leemos el marco geoestadístico del INEGI
    MGE["cve_ent"] = MGE["cve_ent"].apply(lambda x: x.zfill(2)) # Arreglamos el formato, ya que deben haber dos dígitos
    MGE["cve_mun"] = MGE["cve_mun"].apply(lambda x: x.zfill(3)) # Arreglamos el formato, ya que deben haber tres dígitos, para el caso de municipio
    MGE["cve_loc"] = MGE["cve_loc"].apply(lambda x: x.zfill(4)) # Arreglamos el formato, ya que deben haber cuatro dígitos, para el caso de Localidad

    mge_filtros = MGE[['cve_ent','entidad','cve_mun','municipio','cve_loc','localidad','longitud','latitud']]  #Nos quedamos con las columnas que necesitamos
    mge_filtros = mge_filtros.groupby(['cve_ent','cve_mun']).agg({'cve_loc':np.min}).reset_index() # agrupamos por entidad y municipio, y quedarnos con la localidad minima
    mge_filtros = mge_filtros.merge(MGE[['cve_ent','entidad','cve_mun','municipio','cve_loc','localidad','longitud','latitud']], on=['cve_ent','cve_mun', 'cve_loc'], how='left') #hacemos el merge de nuevo con el MGE para poder quedarnos las latitudes y longitudes
    mge_filtros.columns

    # Esta línea es para unir escenarios y el marcogeoestadístico, para traer latitudes, longitudes y nombres de entidades y municipios. 
    escenarios = escenarios.merge(mge_filtros[['cve_ent', 'cve_mun', 'cve_loc', 'entidad', 'municipio', 'localidad',
                                            'longitud', 'latitud']], on=['cve_ent','cve_mun'], how='left')

    # Reeordenamos columnas
    escenarios = escenarios.reindex(columns=['cve_ent', 'entidad', 'cve_mun', 'municipio', 'cve_loc', 'localidad', 'productores',
                                        'produccion_total','gm','imn','precio','Escenario_marginacion','Escenario_precio',
                                        'longitud', 'latitud'])
    

    #print('La suma de productores es: ' + str(escenarios['productores'].sum()))
    return escenarios[['entidad','municipio','latitud','longitud']] #, escenarios['productores'].sum()




###############################################################################################################
############ Función para extraer las coordenadas de cierto DataFrame que se armo anteriormente ###############
###############################################################################################################
def lista_coordenadas(productores):
    i=0
    ubicaciones = []
    for i in range(len(productores)):
        ubi = list(productores.iloc[i:i+1].values) # recorremos cada fila del DataFrame.
        ubi = np.array(ubi)
        ubi = ubi.tolist() 
        ubi = ubi[0] # accedemos a la lista creada con la lista de coordenadas y nombres.
        ubicaciones.append(ubi) 
    return ubicaciones