# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 20:29:57 2021

@author: cesar
"""
# Resumen Vacunacion
import pandas as pd
#import pygsheets
import os 

#Datos:
df_vacunas= pd.read_csv('https://cloud.minsa.gob.pe/s/ZgXoXqK2KLjRLxD/download',sep=',',encoding='latin9')

# En esta base no figura "LIMA REGION", por lo que será necesario crearla:
df_vacunas.loc[(df_vacunas['DEPARTAMENTO']=='LIMA') & (df_vacunas['PROVINCIA']!='LIMA'),'DEPARTAMENTO']='LIMA REGION'
#df_vacunas['DEPARTAMENTO'].value_counts()

#Renombraremos los grupos de riesgo para tener menos categorias:
ree={"PERSONAL DE SALUD": "Personal/est. de salud",
     "ESTUDIANTES DE CIENCIAS DE LA SALUD":"Personal/est. de salud",
     "POLICIA NACIONAL DEL PERU":"Policía, FFAA, bomberos",
     "PERSONAL MILITAR Ã FF AA":"Policía, FFAA, bomberos",
     "BOMBERO":"Policía, FFAA, bomberos",
     "BRIGADISTAS":"Policía, FFAA, bomberos",
     "TRABAJADOR Ã PERSONAL DE LIMPIEZA":"Limpieza/seguridad",
     "PERSONAL DE SEGURIDAD":"limpieza/seguridad",
     "ADULTO MAYOR":"Adulto mayor"}
df_vacunas['GRUPO_RIESGO']=df_vacunas['GRUPO_RIESGO'].replace(ree)
#df_vacunas['GRUPO_RIESGO'].value_counts()

# Renombrando el numero de dosis:
r_dosis={"1": "Primera dosis",
         "2":"Segunda dosis"}
df_vacunas['DOSIS']=df_vacunas['DOSIS'].astype(str)
df_vacunas['DOSIS']=df_vacunas['DOSIS'].replace(r_dosis)
#df_vacunas['DOSIS'].value_counts()

# Agrupando
df_vacunas=df_vacunas.groupby(['DEPARTAMENTO', 'PROVINCIA', 'DISTRITO','GRUPO_RIESGO','DOSIS','FECHA_VACUNACION'])['UUID'].count().reset_index()
df_vacunas['FECHA_VACUNACION']=pd.to_datetime(df_vacunas['FECHA_VACUNACION'].astype(str).str.slice(stop=4)+'/'+df_vacunas['FECHA_VACUNACION'].astype(str).str.slice(start=4).str.slice(stop=2)+'/'+df_vacunas['FECHA_VACUNACION'].astype(str).str.slice(start=6).str.slice(stop=2),format='%Y/%m/%d')

# Definiendo las variables:
df_vacunas.columns=['Region', 'Provincia', 'Distrito', 'Grupo de riesgo', 'Dosis','Fecha de vacunacion', 'Vacunados']

# Creamos sub-bases:
salud_una=df_vacunas.loc[(df_vacunas['Grupo de riesgo']=='Personal/est. de salud')&(df_vacunas['Dosis']=='Primera dosis')]
salud_dos=df_vacunas.loc[(df_vacunas['Grupo de riesgo']=='Personal/est. de salud')&(df_vacunas['Dosis']=='Segunda dosis')]
poli_una=df_vacunas.loc[(df_vacunas['Grupo de riesgo']=='Policía, FFAA, bomberos')&(df_vacunas['Dosis']=='Primera dosis')]
poli_dos=df_vacunas.loc[(df_vacunas['Grupo de riesgo']=='Policía, FFAA, bomberos')&(df_vacunas['Dosis']=='Segunda dosis')] 
limp_una=df_vacunas.loc[(df_vacunas['Grupo de riesgo']=='Limpieza/seguridad')&(df_vacunas['Dosis']=='Primera dosis')]
limp_dos=df_vacunas.loc[(df_vacunas['Grupo de riesgo']=='Limpieza/seguridad')&(df_vacunas['Dosis']=='Segunda dosis')]   
am_una=df_vacunas.loc[(df_vacunas['Grupo de riesgo']=='Adulto mayor')&(df_vacunas['Dosis']=='Primera dosis')]
am_dos=df_vacunas.loc[(df_vacunas['Grupo de riesgo']=='Adulto mayor')&(df_vacunas['Dosis']=='Segunda dosis')]  


#Generando una base de fechas (solo desde el 9 de febrero de 2021 cuando inició el proceso)
serie_vacuna=pd.DataFrame()
x=pd.date_range(start="2021-02-09",end=max(df_vacunas['Fecha de vacunacion']).strftime('%Y-%m-%d'))
for i in range(1,len(x)):
    tmp=pd.DataFrame()
    tmp=df_vacunas[['Region', 'Provincia', 'Distrito']].drop_duplicates()
    tmp['Fecha de vacunacion']=x[i]
    serie_vacuna=serie_vacuna.append(tmp)

#Merge a las bases parciales, para llenar los espacios con fechas vacías
salud_una=pd.merge(serie_vacuna,salud_una,on=['Region', 'Provincia', 'Distrito','Fecha de vacunacion'],how='left')
salud_una['Grupo de riesgo']=salud_una['Grupo de riesgo'].fillna('Personal/est. de salud')
salud_una['Dosis']=salud_una['Dosis'].fillna('Primera dosis')
salud_una['Vacunados']=salud_una['Vacunados'].fillna(0)
salud_dos=pd.merge(serie_vacuna,salud_dos,on=['Region', 'Provincia', 'Distrito','Fecha de vacunacion'],how='left')
salud_dos['Grupo de riesgo']=salud_dos['Grupo de riesgo'].fillna('Personal/est. de salud')
salud_dos['Dosis']=salud_dos['Dosis'].fillna('Segunda dosis')
salud_dos['Vacunados']=salud_dos['Vacunados'].fillna(0)

poli_una=pd.merge(serie_vacuna,poli_una,on=['Region', 'Provincia', 'Distrito','Fecha de vacunacion'],how='left')
poli_una['Grupo de riesgo']=poli_una['Grupo de riesgo'].fillna('Policía, FFAA, bomberos')
poli_una['Dosis']=poli_una['Dosis'].fillna('Primera dosis')
poli_una['Vacunados']=poli_una['Vacunados'].fillna(0)
poli_dos=pd.merge(serie_vacuna,poli_dos,on=['Region', 'Provincia', 'Distrito','Fecha de vacunacion'],how='left')
poli_dos['Grupo de riesgo']=poli_dos['Grupo de riesgo'].fillna('Policía, FFAA, bomberos')
poli_dos['Dosis']=poli_dos['Dosis'].fillna('Segunda dosis')
poli_dos['Vacunados']=poli_dos['Vacunados'].fillna(0)

limp_una=pd.merge(serie_vacuna,limp_una,on=['Region', 'Provincia', 'Distrito','Fecha de vacunacion'],how='left')
limp_una['Grupo de riesgo']=limp_una['Grupo de riesgo'].fillna('Limpieza/seguridad')
limp_una['Dosis']=limp_una['Dosis'].fillna('Primera dosis')
limp_una['Vacunados']=limp_una['Vacunados'].fillna(0)
limp_dos=pd.merge(serie_vacuna,limp_dos,on=['Region', 'Provincia', 'Distrito','Fecha de vacunacion'],how='left')
limp_dos['Grupo de riesgo']=limp_dos['Grupo de riesgo'].fillna('Limpieza/seguridad')
limp_dos['Dosis']=limp_dos['Dosis'].fillna('Segunda dosis')
limp_dos['Vacunados']=limp_dos['Vacunados'].fillna(0)   

am_una=pd.merge(serie_vacuna,am_una,on=['Region', 'Provincia', 'Distrito','Fecha de vacunacion'],how='left')
am_una['Grupo de riesgo']=am_una['Grupo de riesgo'].fillna('Adulto mayor')
am_una['Dosis']=am_una['Dosis'].fillna('Primera dosis')
am_una['Vacunados']=am_una['Vacunados'].fillna(0)
am_dos=pd.merge(serie_vacuna,am_dos,on=['Region', 'Provincia', 'Distrito','Fecha de vacunacion'],how='left')
am_dos['Grupo de riesgo']=am_dos['Grupo de riesgo'].fillna('Adulto mayor')
am_dos['Dosis']=am_dos['Dosis'].fillna('Segunda dosis')
am_dos['Vacunados']=am_dos['Vacunados'].fillna(0)

# Append a las bases:
base=pd.concat([salud_una,salud_dos,poli_una,poli_dos,limp_una,limp_dos,am_una,am_dos],axis=0)
    
# Creando vacunados acumulados:
base['Acumulados']=base.groupby(['Region', 'Provincia', 'Distrito', 'Grupo de riesgo', 'Dosis'])['Vacunados'].cumsum()

# Ajuste final:    
base['Region']=base['Region'].str.capitalize()
base['Provincia']=base['Provincia'].str.capitalize()
base['Distrito']=base['Distrito'].str.capitalize()

# Homogenizando nombres con Tableau:
base.loc[(base['Region']=='Lima'),'Region']='Lima (city)'
base.loc[(base['Region']=='Lima region'),'Region']='Lima'


#base['Region'].value_counts()

## Exportar
os.chdir("D:/Investigacion propia/Covid/Proyecto_Python/Outputs")
base.to_csv(r"Vacunacion actual.csv",index=False, encoding='latin9')