# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 20:29:57 2021

# Actualizado al 22 de setiembre de 2021
@author: cesar
"""
# Resumen Vacunacion
import pandas as pd
#import pygsheets
import os 

os.chdir("D:/Investigacion propia/Covid/Proyecto_Python/Outputs")
#Datos:
#df_vacunas= pd.read_csv('https://cloud.minsa.gob.pe/s/To2QtqoNjKqobfw/download',sep=',',encoding='latin9')

df_vacunas= pd.read_csv('vacunas_covid.csv',sep=',',encoding='latin9')

# En esta base no figura "LIMA REGION", por lo que será necesario crearla:
df_vacunas.loc[(df_vacunas['DEPARTAMENTO']=='LIMA') & (df_vacunas['PROVINCIA']!='LIMA'),'DEPARTAMENTO']='LIMA REGION'
#df_vacunas['DEPARTAMENTO'].value_counts()

# Grupos etarios:
df_vacunas.loc[(df_vacunas['EDAD']>=0) & (df_vacunas['EDAD']<=20),'GRUPO_EDAD']='De 0 a 20 años'
df_vacunas.loc[(df_vacunas['EDAD']>=21) & (df_vacunas['EDAD']<=30),'GRUPO_EDAD']='De 21 a 30 años'
df_vacunas.loc[(df_vacunas['EDAD']>=31) & (df_vacunas['EDAD']<=40),'GRUPO_EDAD']='De 31 a 40 años'
df_vacunas.loc[(df_vacunas['EDAD']>=41) & (df_vacunas['EDAD']<=50),'GRUPO_EDAD']='De 41 a 50 años'
df_vacunas.loc[(df_vacunas['EDAD']>=51) & (df_vacunas['EDAD']<=60),'GRUPO_EDAD']='De 51 a 60 años'
df_vacunas.loc[(df_vacunas['EDAD']>=61) & (df_vacunas['EDAD']<=70),'GRUPO_EDAD']='De 61 a 70 años'
df_vacunas.loc[(df_vacunas['EDAD']>=71) & (df_vacunas['EDAD']<=200),'GRUPO_EDAD']='De 71 a más años'
#df_vacunas['GRUPO_EDAD'].value_counts()

# Renombrando el numero de dosis:
r_dosis={"1": "Primera dosis",
         "2":"Segunda dosis"}
df_vacunas['DOSIS']=df_vacunas['DOSIS'].astype(str)
df_vacunas['DOSIS']=df_vacunas['DOSIS'].replace(r_dosis)
#df_vacunas['DOSIS'].value_counts()

# Agrupando
df_vacunas=df_vacunas.groupby(['DEPARTAMENTO', 'PROVINCIA', 'DISTRITO','GRUPO_EDAD','DOSIS','FECHA_VACUNACION'])['UUID'].count().reset_index()
df_vacunas['FECHA_VACUNACION']=pd.to_datetime(df_vacunas['FECHA_VACUNACION'].astype(str).str.slice(stop=4)+'/'+df_vacunas['FECHA_VACUNACION'].astype(str).str.slice(start=4).str.slice(stop=2)+'/'+df_vacunas['FECHA_VACUNACION'].astype(str).str.slice(start=6).str.slice(stop=2),format='%Y/%m/%d')

# Definiendo las variables:
df_vacunas.columns=['Region', 'Provincia', 'Distrito', 'Grupo etario', 'Dosis','Fecha de vacunacion', 'Vacunados']

# Creamos sub-bases segun grupo etario:
de0_20_una=df_vacunas.loc[(df_vacunas['Grupo etario']=='De 0 a 20 años')&(df_vacunas['Dosis']=='Primera dosis')]
de0_20_dos=df_vacunas.loc[(df_vacunas['Grupo etario']=='De 0 a 20 años')&(df_vacunas['Dosis']=='Segunda dosis')]
de21_30_una=df_vacunas.loc[(df_vacunas['Grupo etario']=='De 21 a 30 años')&(df_vacunas['Dosis']=='Primera dosis')]
de21_30_dos=df_vacunas.loc[(df_vacunas['Grupo etario']=='De 21 a 30 años')&(df_vacunas['Dosis']=='Segunda dosis')]
de31_40_una=df_vacunas.loc[(df_vacunas['Grupo etario']=='De 31 a 40 años')&(df_vacunas['Dosis']=='Primera dosis')]
de31_40_dos=df_vacunas.loc[(df_vacunas['Grupo etario']=='De 31 a 40 años')&(df_vacunas['Dosis']=='Segunda dosis')]
de41_50_una=df_vacunas.loc[(df_vacunas['Grupo etario']=='De 41 a 50 años')&(df_vacunas['Dosis']=='Primera dosis')]
de41_50_dos=df_vacunas.loc[(df_vacunas['Grupo etario']=='De 41 a 50 años')&(df_vacunas['Dosis']=='Segunda dosis')]
de51_60_una=df_vacunas.loc[(df_vacunas['Grupo etario']=='De 51 a 60 años')&(df_vacunas['Dosis']=='Primera dosis')]
de51_60_dos=df_vacunas.loc[(df_vacunas['Grupo etario']=='De 51 a 60 años')&(df_vacunas['Dosis']=='Segunda dosis')]
de61_70_una=df_vacunas.loc[(df_vacunas['Grupo etario']=='De 61 a 70 años')&(df_vacunas['Dosis']=='Primera dosis')]
de61_70_dos=df_vacunas.loc[(df_vacunas['Grupo etario']=='De 61 a 70 años')&(df_vacunas['Dosis']=='Segunda dosis')]
de71_mas_una=df_vacunas.loc[(df_vacunas['Grupo etario']=='De 71 a más años')&(df_vacunas['Dosis']=='Primera dosis')]
de71_mas_dos=df_vacunas.loc[(df_vacunas['Grupo etario']=='De 71 a más años')&(df_vacunas['Dosis']=='Segunda dosis')]

 
#Generando una base de fechas (solo desde el 9 de febrero de 2021 cuando inició el proceso)
serie_vacuna=pd.DataFrame()
x=pd.date_range(start="2021-02-09",end=max(df_vacunas['Fecha de vacunacion']).strftime('%Y-%m-%d'))
for i in range(1,len(x)):
    tmp=pd.DataFrame()
    tmp=df_vacunas[['Region', 'Provincia', 'Distrito']].drop_duplicates()
    tmp['Fecha de vacunacion']=x[i]
    serie_vacuna=serie_vacuna.append(tmp)

#Merge a las bases parciales, para llenar los espacios con fechas vacías
de0_20_una=pd.merge(serie_vacuna,de0_20_una,on=['Region', 'Provincia', 'Distrito','Fecha de vacunacion'],how='left')
de0_20_una['Grupo etario']=de0_20_una['Grupo etario'].fillna('De 0 a 20 años')
de0_20_una['Dosis']=de0_20_una['Dosis'].fillna('Primera dosis')
de0_20_una['Vacunados']=de0_20_una['Vacunados'].fillna(0)
de0_20_dos=pd.merge(serie_vacuna,de0_20_dos,on=['Region', 'Provincia', 'Distrito','Fecha de vacunacion'],how='left')
de0_20_dos['Grupo etario']=de0_20_dos['Grupo etario'].fillna('De 0 a 20 años')
de0_20_dos['Dosis']=de0_20_dos['Dosis'].fillna('Segunda dosis')
de0_20_dos['Vacunados']=de0_20_dos['Vacunados'].fillna(0)

de21_30_una=pd.merge(serie_vacuna,de21_30_una,on=['Region', 'Provincia', 'Distrito','Fecha de vacunacion'],how='left')
de21_30_una['Grupo etario']=de21_30_una['Grupo etario'].fillna('De 21 a 30 años')
de21_30_una['Dosis']=de21_30_una['Dosis'].fillna('Primera dosis')
de21_30_una['Vacunados']=de21_30_una['Vacunados'].fillna(0)
de21_30_dos=pd.merge(serie_vacuna,de21_30_dos,on=['Region', 'Provincia', 'Distrito','Fecha de vacunacion'],how='left')
de21_30_dos['Grupo etario']=de21_30_dos['Grupo etario'].fillna('De 21 a 30 años')
de21_30_dos['Dosis']=de21_30_dos['Dosis'].fillna('Segunda dosis')
de21_30_dos['Vacunados']=de21_30_dos['Vacunados'].fillna(0)

de31_40_una=pd.merge(serie_vacuna,de31_40_una,on=['Region', 'Provincia', 'Distrito','Fecha de vacunacion'],how='left')
de31_40_una['Grupo etario']=de31_40_una['Grupo etario'].fillna('De 31 a 40 años')
de31_40_una['Dosis']=de31_40_una['Dosis'].fillna('Primera dosis')
de31_40_una['Vacunados']=de31_40_una['Vacunados'].fillna(0)
de31_40_dos=pd.merge(serie_vacuna,de31_40_dos,on=['Region', 'Provincia', 'Distrito','Fecha de vacunacion'],how='left')
de31_40_dos['Grupo etario']=de31_40_dos['Grupo etario'].fillna('De 31 a 40 años')
de31_40_dos['Dosis']=de31_40_dos['Dosis'].fillna('Segunda dosis')
de31_40_dos['Vacunados']=de31_40_dos['Vacunados'].fillna(0)

de41_50_una=pd.merge(serie_vacuna,de41_50_una,on=['Region', 'Provincia', 'Distrito','Fecha de vacunacion'],how='left')
de41_50_una['Grupo etario']=de41_50_una['Grupo etario'].fillna('De 41 a 50 años')
de41_50_una['Dosis']=de41_50_una['Dosis'].fillna('Primera dosis')
de41_50_una['Vacunados']=de41_50_una['Vacunados'].fillna(0)
de41_50_dos=pd.merge(serie_vacuna,de41_50_dos,on=['Region', 'Provincia', 'Distrito','Fecha de vacunacion'],how='left')
de41_50_dos['Grupo etario']=de41_50_dos['Grupo etario'].fillna('De 41 a 50 años')
de41_50_dos['Dosis']=de41_50_dos['Dosis'].fillna('Segunda dosis')
de41_50_dos['Vacunados']=de41_50_dos['Vacunados'].fillna(0)

de51_60_una=pd.merge(serie_vacuna,de51_60_una,on=['Region', 'Provincia', 'Distrito','Fecha de vacunacion'],how='left')
de51_60_una['Grupo etario']=de51_60_una['Grupo etario'].fillna('De 51 a 60 años')
de51_60_una['Dosis']=de51_60_una['Dosis'].fillna('Primera dosis')
de51_60_una['Vacunados']=de51_60_una['Vacunados'].fillna(0)
de51_60_dos=pd.merge(serie_vacuna,de51_60_dos,on=['Region', 'Provincia', 'Distrito','Fecha de vacunacion'],how='left')
de51_60_dos['Grupo etario']=de51_60_dos['Grupo etario'].fillna('De 51 a 60 años')
de51_60_dos['Dosis']=de51_60_dos['Dosis'].fillna('Segunda dosis')
de51_60_dos['Vacunados']=de51_60_dos['Vacunados'].fillna(0)

de61_70_una=pd.merge(serie_vacuna,de61_70_una,on=['Region', 'Provincia', 'Distrito','Fecha de vacunacion'],how='left')
de61_70_una['Grupo etario']=de61_70_una['Grupo etario'].fillna('De 61 a 70 años')
de61_70_una['Dosis']=de61_70_una['Dosis'].fillna('Primera dosis')
de61_70_una['Vacunados']=de61_70_una['Vacunados'].fillna(0)
de61_70_dos=pd.merge(serie_vacuna,de61_70_dos,on=['Region', 'Provincia', 'Distrito','Fecha de vacunacion'],how='left')
de61_70_dos['Grupo etario']=de61_70_dos['Grupo etario'].fillna('De 61 a 70 años')
de61_70_dos['Dosis']=de61_70_dos['Dosis'].fillna('Segunda dosis')
de61_70_dos['Vacunados']=de61_70_dos['Vacunados'].fillna(0)

de71_mas_una=pd.merge(serie_vacuna,de71_mas_una,on=['Region', 'Provincia', 'Distrito','Fecha de vacunacion'],how='left')
de71_mas_una['Grupo etario']=de71_mas_una['Grupo etario'].fillna('De 71 a más años')
de71_mas_una['Dosis']=de71_mas_una['Dosis'].fillna('Primera dosis')
de71_mas_una['Vacunados']=de71_mas_una['Vacunados'].fillna(0)
de71_mas_dos=pd.merge(serie_vacuna,de71_mas_dos,on=['Region', 'Provincia', 'Distrito','Fecha de vacunacion'],how='left')
de71_mas_dos['Grupo etario']=de71_mas_dos['Grupo etario'].fillna('De 71 a más años')
de71_mas_dos['Dosis']=de71_mas_dos['Dosis'].fillna('Segunda dosis')
de71_mas_dos['Vacunados']=de71_mas_dos['Vacunados'].fillna(0)


# Append a las bases:
base=pd.concat([de0_20_una,de0_20_dos,de21_30_una,de21_30_dos,de31_40_una,de31_40_dos,de41_50_una,de41_50_dos,de51_60_una,de51_60_dos,de61_70_una,de61_70_dos,de71_mas_una,de71_mas_dos],axis=0)
    
# Creando vacunados acumulados:
base['Acumulados']=base.groupby(['Region', 'Provincia', 'Distrito', 'Grupo etario', 'Dosis'])['Vacunados'].cumsum()

# Ajuste final:    
base['Region']=base['Region'].str.capitalize()
base['Provincia']=base['Provincia'].str.capitalize()
base['Distrito']=base['Distrito'].str.capitalize()

# Homogenizando nombres con Tableau:
base.loc[(base['Region']=='Lima'),'Region']='Lima (city)'
base.loc[(base['Region']=='Lima region'),'Region']='Lima'


#base['Region'].value_counts()
#base['Grupo de riesgo'].value_counts()

## Exportar
os.chdir("D:/Investigacion propia/Covid/Proyecto_Python/Outputs")
base.to_csv(r"Vacunacion actual.csv",index=False, encoding='latin9')