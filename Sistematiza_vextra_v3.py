# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 15:39:07 2021

@author: Cesar Mora
"""
# Resumen Covi-Datos
# Actualizado al 22 de setiembre 2021
#paquetes
import pandas as pd
import pygsheets
import os 

os.chdir("D:/Investigacion propia/Covid/Proyecto_Python/Outputs")
#Datos conservando solo las variables relevantes:
#data_casos = pd.read_csv('https://cloud.minsa.gob.pe/s/AC2adyLkHCKjmfm/download',sep=';',encoding='latin9',usecols=['UUID', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO','EDAD', 'SEXO', 'FECHA_RESULTADO'])
#data_fallecidos = pd.read_csv('https://cloud.minsa.gob.pe/s/xJ2LQ3QyRW38Pe5/download',sep=';',encoding='latin9',usecols=['UUID', 'FECHA_FALLECIMIENTO', 'EDAD_DECLARADA', 'SEXO','DEPARTAMENTO', 'PROVINCIA', 'DISTRITO'])
#data_sinadef=pd.read_csv('https://cloud.minsa.gob.pe/s/nqF2irNbFomCLaa/download',header=2 ,sep=';',encoding='latin9',usecols=['Nº','SEXO','EDAD','TIEMPO EDAD','NIVEL DE INSTRUCCIÓN','DEPARTAMENTO DOMICILIO','PROVINCIA DOMICILIO','DISTRITO DOMICILIO','FECHA'])

data_casos = pd.read_csv('positivos_covid.csv',sep=';',encoding='latin9',usecols=['id_persona', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO','EDAD', 'SEXO', 'FECHA_RESULTADO'])
data_fallecidos = pd.read_csv('fallecidos_covid.csv',sep=';',encoding='latin9',usecols=['id_persona', 'FECHA_FALLECIMIENTO', 'EDAD_DECLARADA', 'SEXO','DEPARTAMENTO', 'PROVINCIA', 'DISTRITO'])
#data_sinadef=pd.read_csv('fallecidos_sinadef.csv',header=2 ,sep=';',encoding='latin9',usecols=['Nº','SEXO','EDAD','TIEMPO EDAD','NIVEL DE INSTRUCCIÓN','DEPARTAMENTO DOMICILIO','PROVINCIA DOMICILIO','DISTRITO DOMICILIO','FECHA'])
data_sinadef=pd.read_csv('fallecidos_sinadef.csv',sep='|',encoding='UTF-8',usecols=['Nº','SEXO','EDAD','TIEMPO EDAD','NIVEL DE INSTRUCCIÓN','DEPARTAMENTO DOMICILIO','PROVINCIA DOMICILIO','DISTRITO DOMICILIO','FECHA'])

#data_casos['DEPARTAMENTO'].value_counts()
#data_fallecidos['DEPARTAMENTO'].value_counts()
#data_sinadef['DEPARTAMENTO DOMICILIO'].value_counts()

# Cambiando LIMA REGION Y LIMA METROPOLITANA donde corresponda:
data_casos.loc[(data_casos['DEPARTAMENTO']=='LIMA') & (data_casos['PROVINCIA']=='LIMA'),'DEPARTAMENTO']='LIMA METROPOLITANA'
data_casos.loc[(data_casos['DEPARTAMENTO']=='LIMA') & (data_casos['PROVINCIA']!='LIMA'),'DEPARTAMENTO']='LIMA REGION'
data_fallecidos.loc[(data_fallecidos['DEPARTAMENTO']=='LIMA') & (data_fallecidos['PROVINCIA']=='LIMA'),'DEPARTAMENTO']='LIMA METROPOLITANA'
data_fallecidos.loc[(data_fallecidos['DEPARTAMENTO']=='LIMA') & (data_fallecidos['PROVINCIA']!='LIMA'),'DEPARTAMENTO']='LIMA REGION'
data_sinadef.loc[(data_sinadef['DEPARTAMENTO DOMICILIO']=='LIMA') & (data_sinadef['PROVINCIA DOMICILIO']=='LIMA'),'DEPARTAMENTO DOMICILIO']='LIMA METROPOLITANA'
data_sinadef.loc[(data_sinadef['DEPARTAMENTO DOMICILIO']=='LIMA') & (data_sinadef['PROVINCIA DOMICILIO']!='LIMA'),'DEPARTAMENTO DOMICILIO']='LIMA REGION'



# En la base de SINADEF, no todas las edades están en años, por lo que cambiaremos esos casos:
data_sinadef.loc[(data_sinadef['TIEMPO EDAD']!='AÑOS'),'EDAD']='0'
data_sinadef.loc[(data_sinadef['EDAD']=='SIN REGISTRO'),'EDAD']=''
## Convertimos a numerica la EDAD:
data_sinadef['EDAD']=pd.to_numeric(data_sinadef['EDAD'])

# Creando variables de agrupamiento: GRUPO_EDAD, EDUCACION
## Base casos:
### Creando la variable GRUPO_EDAD
data_casos.loc[(data_casos['EDAD']>=0) & (data_casos['EDAD']<=20),'GRUPO_EDAD']='De 0 a 20 años'
data_casos.loc[(data_casos['EDAD']>=21) & (data_casos['EDAD']<=30),'GRUPO_EDAD']='De 21 a 30 años'
data_casos.loc[(data_casos['EDAD']>=31) & (data_casos['EDAD']<=40),'GRUPO_EDAD']='De 31 a 40 años'
data_casos.loc[(data_casos['EDAD']>=41) & (data_casos['EDAD']<=50),'GRUPO_EDAD']='De 41 a 50 años'
data_casos.loc[(data_casos['EDAD']>=51) & (data_casos['EDAD']<=60),'GRUPO_EDAD']='De 51 a 60 años'
data_casos.loc[(data_casos['EDAD']>=61) & (data_casos['EDAD']<=70),'GRUPO_EDAD']='De 61 a 70 años'
data_casos.loc[(data_casos['EDAD']>=71) & (data_casos['EDAD']<=200),'GRUPO_EDAD']='De 71 a más años'
### Modificando la variable SEXO:
data_casos.loc[(data_casos['SEXO']=='FEMENINO'),'SEXO']='Mujer'
data_casos.loc[(data_casos['SEXO']=='MASCULINO'),'SEXO']='Hombre'
    
## Base fallecidos:
### Creando la variable GRUPO_EDAD
data_fallecidos.loc[(data_fallecidos['EDAD_DECLARADA']>=0) & (data_fallecidos['EDAD_DECLARADA']<=20),'GRUPO_EDAD']='De 0 a 20 años'
data_fallecidos.loc[(data_fallecidos['EDAD_DECLARADA']>=21) & (data_fallecidos['EDAD_DECLARADA']<=30),'GRUPO_EDAD']='De 21 a 30 años'
data_fallecidos.loc[(data_fallecidos['EDAD_DECLARADA']>=31) & (data_fallecidos['EDAD_DECLARADA']<=40),'GRUPO_EDAD']='De 31 a 40 años'
data_fallecidos.loc[(data_fallecidos['EDAD_DECLARADA']>=41) & (data_fallecidos['EDAD_DECLARADA']<=50),'GRUPO_EDAD']='De 41 a 50 años'
data_fallecidos.loc[(data_fallecidos['EDAD_DECLARADA']>=51) & (data_fallecidos['EDAD_DECLARADA']<=60),'GRUPO_EDAD']='De 51 a 60 años'
data_fallecidos.loc[(data_fallecidos['EDAD_DECLARADA']>=61) & (data_fallecidos['EDAD_DECLARADA']<=70),'GRUPO_EDAD']='De 61 a 70 años'
data_fallecidos.loc[(data_fallecidos['EDAD_DECLARADA']>=71) & (data_fallecidos['EDAD_DECLARADA']<=200),'GRUPO_EDAD']='De 71 a más años'
### Modificando la variable SEXO:
data_fallecidos.loc[(data_fallecidos['SEXO']=='FEMENINO'),'SEXO']='Mujer'
data_fallecidos.loc[(data_fallecidos['SEXO']=='MASCULINO'),'SEXO']='Hombre'

## Base SINADEF
### Creando la variable GRUPO_EDAD
data_sinadef.loc[(data_sinadef['EDAD']>=0) & (data_sinadef['EDAD']<=20),'GRUPO_EDAD']='De 0 a 20 años'
data_sinadef.loc[(data_sinadef['EDAD']>=21) & (data_sinadef['EDAD']<=30),'GRUPO_EDAD']='De 21 a 30 años'
data_sinadef.loc[(data_sinadef['EDAD']>=31) & (data_sinadef['EDAD']<=40),'GRUPO_EDAD']='De 31 a 40 años'
data_sinadef.loc[(data_sinadef['EDAD']>=41) & (data_sinadef['EDAD']<=50),'GRUPO_EDAD']='De 41 a 50 años'
data_sinadef.loc[(data_sinadef['EDAD']>=51) & (data_sinadef['EDAD']<=60),'GRUPO_EDAD']='De 51 a 60 años'
data_sinadef.loc[(data_sinadef['EDAD']>=61) & (data_sinadef['EDAD']<=70),'GRUPO_EDAD']='De 61 a 70 años'
data_sinadef.loc[(data_sinadef['EDAD']>=71) & (data_sinadef['EDAD']<=200),'GRUPO_EDAD']='De 71 a más años'
### Modificando la variable SEXO:
data_sinadef.loc[(data_sinadef['SEXO']=='FEMENINO'),'SEXO']='Mujer'
data_sinadef.loc[(data_sinadef['SEXO']=='MASCULINO'),'SEXO']='Hombre'
## Creando la variable instruccion (solo para mayores de 18 años)
data_sinadef=data_sinadef.rename(columns={'NIVEL DE INSTRUCCIÓN':'INSTRUCCION'})
data_sinadef.loc[((data_sinadef['INSTRUCCION']=='IGNORADO') | (data_sinadef['INSTRUCCION']=='SIN REGISTRO')) & (data_sinadef['EDAD']>=18),'EDUCACION']='Ignorado'
data_sinadef.loc[(data_sinadef['INSTRUCCION']=='NINGUN NIVEL / ILETRADO') | (data_sinadef['INSTRUCCION']=='INICIAL / PRE-ESCOLAR') | (data_sinadef['INSTRUCCION']=='PRIMARIA INCOMPLETA') | (data_sinadef['INSTRUCCION']=='PRIMARIA COMPLETA') & (data_sinadef['EDAD']>=18),'EDUCACION']='Primaria completa o menos'
data_sinadef.loc[(data_sinadef['INSTRUCCION']=='SECUNDARIA INCOMPLETA') | (data_sinadef['INSTRUCCION']=='SECUNDARIA COMPLETA') & (data_sinadef['EDAD']>=18) ,'EDUCACION']='Secundaria incomp/completa'
data_sinadef.loc[(data_sinadef['INSTRUCCION']=='SUPERIOR NO UNIV. INC.') | (data_sinadef['INSTRUCCION']=='SUPERIOR NO UNIV. COMP.') | (data_sinadef['INSTRUCCION']=='SUPERIOR UNIV. INC.') | (data_sinadef['INSTRUCCION']=='SUPERIOR UNIV. COMP.') & (data_sinadef['EDAD']>=18),'EDUCACION']='Más que secundaria'


## Nuevas variables de conteo:
data_casos['conteo']=1
data_fallecidos['conteo']=1
data_sinadef['conteo']=1

####################################################################################
#Agrupamiento de las variables a nivel distrital (sin agrupamiento por edad o sexo)#
####################################################################################
## Casos 
#d_casos=data_casos.groupby(['DEPARTAMENTO', 'PROVINCIA', 'DISTRITO','FECHA_RESULTADO'])['UUID'].count().reset_index()
d_casos=data_casos.groupby(['DEPARTAMENTO', 'PROVINCIA', 'DISTRITO','FECHA_RESULTADO'])['conteo'].sum().reset_index()
d_casos['FECHA_RESULTADO']=pd.to_datetime(d_casos['FECHA_RESULTADO'].astype(str).str.slice(stop=4)+'/'+d_casos['FECHA_RESULTADO'].astype(str).str.slice(start=4).str.slice(stop=2)+'/'+d_casos['FECHA_RESULTADO'].astype(str).str.slice(start=6).str.slice(stop=2),format='%Y/%m/%d')
#d_casos['cumsum_casos']=d_casos.groupby(['DEPARTAMENTO', 'PROVINCIA', 'DISTRITO'])['UUID'].cumsum()

## Fallecidos confirmados:
#d_fallecidos=data_fallecidos.groupby(['DEPARTAMENTO', 'PROVINCIA', 'DISTRITO','FECHA_FALLECIMIENTO'])['UUID'].count().reset_index()
d_fallecidos=data_fallecidos.groupby(['DEPARTAMENTO', 'PROVINCIA', 'DISTRITO','FECHA_FALLECIMIENTO'])['conteo'].sum().reset_index()
d_fallecidos['FECHA_FALLECIMIENTO']=pd.to_datetime(d_fallecidos['FECHA_FALLECIMIENTO'],format='%Y%m%d')
#d_fallecidos['cumsum_muertes']=d_fallecidos.groupby(['DEPARTAMENTO', 'PROVINCIA', 'DISTRITO',])['UUID'].cumsum()

## Fallecidos SINADEF:
#d_sinadef=data_sinadef.groupby(['DEPARTAMENTO DOMICILIO', 'PROVINCIA DOMICILIO', 'DISTRITO DOMICILIO','FECHA'])['Nº'].count().reset_index()
d_sinadef=data_sinadef.groupby(['DEPARTAMENTO DOMICILIO', 'PROVINCIA DOMICILIO', 'DISTRITO DOMICILIO','FECHA'])['conteo'].sum().reset_index()
#d_sinadef['FECHA']=pd.to_datetime(d_sinadef['FECHA'],format='%d/%m/%Y')
d_sinadef['FECHA']=pd.to_datetime(d_sinadef['FECHA'],format='%Y/%m/%d')
#d_sinadef['cumsum_sinadef']=d_sinadef.groupby(['DEPARTAMENTO DOMICILIO', 'PROVINCIA DOMICILIO', 'DISTRITO DOMICILIO',])['Nº'].cumsum()

# Definiendo los nombres de las variables en las bases:
d_casos.columns=['DPTO', 'PROVINCIA', 'DISTRITO', 'FECHA', 'Casos confirmados']
d_fallecidos.columns=['DPTO', 'PROVINCIA', 'DISTRITO', 'FECHA', 'Fallecidos COVID-19']
d_sinadef.columns=['DPTO', 'PROVINCIA', 'DISTRITO', 'FECHA', 'Fallecidos SINADEF']

#Generando una base de fechas (solo desde el 1 de marzo 2020)
data_covid_dist=pd.DataFrame()
x=pd.date_range(start="2020-03-01",end=max(d_casos['FECHA']).strftime('%Y-%m-%d'))
for i in range(1,len(x)):
    tmp=pd.DataFrame()
    tmp=d_casos[['DPTO', 'PROVINCIA', 'DISTRITO']].drop_duplicates()
    tmp['FECHA']=x[i]
    data_covid_dist=data_covid_dist.append(tmp)
         
#Consolidacion de datos de nivel distrital:
data_covid_dist=pd.merge(data_covid_dist,d_casos,on=['DPTO', 'PROVINCIA', 'DISTRITO','FECHA'],how='left')
data_covid_dist=pd.merge(data_covid_dist,d_fallecidos,on=['DPTO', 'PROVINCIA', 'DISTRITO','FECHA'],how='left')
data_covid_dist=pd.merge(data_covid_dist,d_sinadef,on=['DPTO', 'PROVINCIA', 'DISTRITO','FECHA'],how='left')
data_covid_dist=data_covid_dist.fillna(0)

# Ajuste final:    
data_covid_dist['DPTO']=data_covid_dist['DPTO'].str.capitalize()
data_covid_dist['PROVINCIA']=data_covid_dist['PROVINCIA'].str.capitalize()
data_covid_dist['DISTRITO']=data_covid_dist['DISTRITO'].str.capitalize()

# Homogenizando nombres con Tableau:
data_covid_dist['REGION']=data_covid_dist['DPTO']
data_covid_dist.loc[(data_covid_dist['REGION']=='Lima metropolitana'),'REGION']='Lima (city)'
data_covid_dist.loc[data_covid_dist['REGION']=='Lima region','REGION']='Lima'
data_covid_dist.loc[data_covid_dist['REGION']=='Lima','REGION']='Lima'
#data_covid['REGION'].value_counts()

## Exportar Version distrital
os.chdir("D:/Investigacion propia/Covid/Proyecto_Python/Outputs")
data_covid_dist.to_csv(r"Data_covid_distrital_simple.csv",encoding='latin9',index=False)


#########################################################################################################
#Agrupamiento de las variables a nivel regional (con agrupamiento por edad, sexo y nivel de instrucción)#
#########################################################################################################
## Casos 
#r_casos=data_casos.groupby(['DEPARTAMENTO','FECHA_RESULTADO','GRUPO_EDAD','SEXO'])['UUID'].count().reset_index()
r_casos=data_casos.groupby(['DEPARTAMENTO','FECHA_RESULTADO','GRUPO_EDAD','SEXO'])['conteo'].sum().reset_index()
r_casos['FECHA_RESULTADO']=pd.to_datetime(r_casos['FECHA_RESULTADO'].astype(str).str.slice(stop=4)+'/'+r_casos['FECHA_RESULTADO'].astype(str).str.slice(start=4).str.slice(stop=2)+'/'+r_casos['FECHA_RESULTADO'].astype(str).str.slice(start=6).str.slice(stop=2),format='%Y/%m/%d')
## Fallecidos confirmado
#r_fallecidos=data_fallecidos.groupby(['DEPARTAMENTO','FECHA_FALLECIMIENTO','GRUPO_EDAD','SEXO'])['UUID'].count().reset_index()
r_fallecidos=data_fallecidos.groupby(['DEPARTAMENTO','FECHA_FALLECIMIENTO','GRUPO_EDAD','SEXO'])['conteo'].sum().reset_index()
r_fallecidos['FECHA_FALLECIMIENTO']=pd.to_datetime(r_fallecidos['FECHA_FALLECIMIENTO'],format='%Y%m%d')
## Fallecidos SINADEF (GRUPO_EDAD y SEXO):
#r_sinadef=data_sinadef.groupby(['DEPARTAMENTO DOMICILIO','FECHA','GRUPO_EDAD','SEXO'])['Nº'].count().reset_index()
r_sinadef=data_sinadef.groupby(['DEPARTAMENTO DOMICILIO','FECHA','GRUPO_EDAD','SEXO'])['conteo'].sum().reset_index()
#r_sinadef['FECHA']=pd.to_datetime(r_sinadef['FECHA'],format='%d/%m/%Y')
r_sinadef['FECHA']=pd.to_datetime(r_sinadef['FECHA'],format='%Y/%m/%d')

## Fallecidos SINADEF (EDUCACION):
#r_sinadef_e=data_sinadef.groupby(['DEPARTAMENTO DOMICILIO','FECHA','EDUCACION'])['Nº'].count().reset_index()
r_sinadef_e=data_sinadef.groupby(['DEPARTAMENTO DOMICILIO','FECHA','EDUCACION'])['conteo'].sum().reset_index()
#r_sinadef_e['FECHA']=pd.to_datetime(r_sinadef_e['FECHA'],format='%d/%m/%Y')
r_sinadef_e['FECHA']=pd.to_datetime(r_sinadef_e['FECHA'],format='%Y/%m/%d')

# Definiendo los nombres de las variables en las bases:
r_casos.columns=['DPTO','FECHA','Grupo etario','Sexo','Casos confirmados']
r_fallecidos.columns=['DPTO','FECHA','Grupo etario','Sexo', 'Fallecidos COVID-19']
r_sinadef.columns=['DPTO', 'FECHA', 'Grupo etario','Sexo', 'Fallecidos SINADEF']
r_sinadef_e.columns=['DPTO', 'FECHA','Instrucción', 'Fallecidos SINADEF']

#Generando una base de fechas a nivel provincial (solo desde el 1 de marzo 2020)
data_covid_reg=pd.DataFrame()
x=pd.date_range(start="2020-03-01",end=max(r_casos['FECHA']).strftime('%Y-%m-%d'))
for i in range(1,len(x)):
    tmp=pd.DataFrame()
    tmp=r_casos[['DPTO','Grupo etario','Sexo']].drop_duplicates()
    tmp['FECHA']=x[i]
    data_covid_reg=data_covid_reg.append(tmp)
    
#Consolidacion de datos de nivel regional con grupo etario y sexo:
data_covid_reg=pd.merge(data_covid_reg,r_casos,on=['DPTO','FECHA','Grupo etario','Sexo'],how='left')
data_covid_reg=pd.merge(data_covid_reg,r_fallecidos,on=['DPTO','FECHA','Grupo etario','Sexo'],how='left')
data_covid_reg=pd.merge(data_covid_reg,r_sinadef,on=['DPTO', 'FECHA','Grupo etario','Sexo'],how='left')
data_covid_reg=data_covid_reg.fillna(0)

#Colocando fechas a los datos de SINADEF por nivel educativo:
data_covid_reg_e=pd.DataFrame()
x=pd.date_range(start="2020-03-01",end=max(r_sinadef_e['FECHA']).strftime('%Y-%m-%d'))
for i in range(1,len(x)):
    tmp=pd.DataFrame()
    tmp=r_sinadef_e[['DPTO','Instrucción']].drop_duplicates()
    tmp['FECHA']=x[i]
    data_covid_reg_e=data_covid_reg_e.append(tmp)
    
data_covid_reg_e=pd.merge(data_covid_reg_e,r_sinadef_e,on=['DPTO','FECHA','Instrucción'],how='left')
data_covid_reg_e=data_covid_reg_e.fillna(0)

# Ajuste final:
data_covid_reg['DPTO']=data_covid_reg['DPTO'].str.capitalize()
data_covid_reg_e['DPTO']=data_covid_reg_e['DPTO'].str.capitalize()

# Homogenizando nombres con Tableau:
data_covid_reg['REGION']=data_covid_reg['DPTO']
data_covid_reg.loc[(data_covid_reg['REGION']=='Lima metropolitana'),'REGION']='Lima (city)'
data_covid_reg.loc[data_covid_reg['REGION']=='Lima region','REGION']='Lima'
data_covid_reg.loc[(data_covid_reg['REGION']=='Lima'),'REGION']='Lima'

data_covid_reg_e['REGION']=data_covid_reg_e['DPTO']
data_covid_reg_e.loc[(data_covid_reg_e['REGION']=='Lima metropolitana'),'REGION']='Lima (city)'
data_covid_reg_e.loc[data_covid_reg_e['REGION']=='Lima region','REGION']='Lima'
data_covid_reg_e.loc[data_covid_reg_e['REGION']=='Lima','REGION']='Lima'

## Exportar Versiones regionales:
os.chdir("D:/Investigacion propia/Covid/Proyecto_Python/Outputs")
data_covid_reg.to_csv(r"Data_covid_regional_simple.csv",encoding='latin9',index=False)
data_covid_reg_e.to_csv(r"Data_covid_regional_sinad_educ.csv",encoding='latin9',index=False)
