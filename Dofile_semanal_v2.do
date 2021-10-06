clear
global datos cd "D:\Investigacion propia\Covid"
global bases cd "D:\Investigacion propia\Covid\Proyecto_Python\Outputs"
global graph cd "D:\Investigacion propia\Covid\Graphs\Semanales"

**************************************
* PREPARACION DE DATOS Y FECHAS*******
**************************************
* Reporte semanal:
** Cambiar los nombres de los folder de acuerdo a la fecha

$graph 
*mkdir "Semana termina en 031021"
global new_folder cd "D:\Investigacion propia\Covid\Graphs\Semanales\Semana termina en 031021"

* Definicion de fechas:
global fecha_inicio "21mar2021"
global fecha_fin "22556"
global linea "22524" /*1 de setiembre*/

global semana_inicio "24"
global semana_fin "27"
global etiqueta "label define semana 0 "22-28 marzo" 1 "29m-4 abril" 2 "5-11 abril" 3 "12-18 abril" 4 "19-25 abril" 5 "26 abr-2 mayo" 6 "3-9 mayo" 7 "10-16 mayo" 8 "17-23 mayo" 9 "24-30 mayo" 10 "31 may-6 jun" 11 "7-13 junio" 12 "14-20 junio" 13 "21-27 junio" 14 "28 jun-4 jul" 15 "5-11 julio" 16 "12-18 julio" 17 "19-25 julio" 18 "26 jul-1 ago" 19 "2-8 agosto" 20 "9-15 agosto" 21 "16-22 agosto" 22 "23-29 agosto" 23 "30 ago-5 sep" 24 "6-12 setiembre" 25 "13-19 setiembre" 26 "20-26 setiembre" 27 "27 set-3 oct""

* Etiquetas de graficos:
global inicio "20-26 setiembre" 
global fin "27 set-3 oct"

*******************************
* 1. Informacion Twitter MINSA*
*******************************
$datos
import excel "Tendencia Corona_Peru2.xlsx", firstrow clear
replace Día=Día-1
gen x=Día
br Día x /*inspeccionar el día que corresponda*/
* Revisar las fechas para definir la linea referencial de dos semanas

tsset Día
format Día %tdMon/YY
gen int semana_nro= (wofd(Día-3)) - wofd(td($fecha_inicio))
sum semana_nro
scalar semana_max=r(max)

***********************************

* Ratio de positividad:
gen positivo_dia=(Nuevoscasosconfirmadospordía/Nuevosreportes)*100

* Medias móviles de últimos 7 días para variables seleccionadas:
gen reportesdia_movil7=(Nuevosreportes+L1.Nuevosreportes+L2.Nuevosreportes+L3.Nuevosreportes+L4.Nuevosreportes+L5.Nuevosreportes+L6.Nuevosreportes)/7
gen positdia_movil7=(positivo_dia+L1.positivo_dia+L2.positivo_dia+L3.positivo_dia+L4.positivo_dia+L5.positivo_dia+L6.positivo_dia)/7
gen ncasosdia_movil7=(Nuevoscasosconfirmadospordía+L1.Nuevoscasosconfirmadospordía+L2.Nuevoscasosconfirmadospordía+L3.Nuevoscasosconfirmadospordía+L4.Nuevoscasosconfirmadospordía+L5.Nuevoscasosconfirmadospordía+L6.Nuevoscasosconfirmadospordía)/7
gen falldia_movil7=(Fallecidospordía+L1.Fallecidospordía+L2.Fallecidospordía+L3.Fallecidospordía+L4.Fallecidospordía+L5.Fallecidospordía+L6.Fallecidospordía)/7

label var Casosactivos " "
label var Día "Fecha"
label var positivo_dia "Según día"
label var Hospita " "
label var reportesdia_movil7 "Reportes por día"
label var positdia_movil7 " "
label var ncasosdia_movil7 "Positivos por día"
label var falldia_movil7 " "

*********************************
* Graficos de series de tiempo **
*********************************

$new_folder
* Casos activos:
line Casosactivos Día, ylabel(#6,labsize(2.5)) xlabel(#8, labsize(2.5)) title("Casos activos COVID-19",size(medium)) xline($linea,lpa(dash)) 
graph export "Activos.png", width (1000)replace 

* Nuevos reportes y confirmados por día: todo el periodo (media móvil)
 line reportesdia_movil7 ncasosdia_movil7 Día, ylabel(#10,labsize(2)) xlabel(#8, labsize(2.5)) title("Pruebas aplicadas y positivos COVID-19 por día (media móvil)",size(medium)) xline($linea,lpa(dash))
graph export "Pruebas_Positivos_diarios.png", width (1000)replace 

* Positividad diaria (media movil de ultimos 7 dias)
 line positdia_movil7 Día,ylabel(#10,labsize(2)) xlabel(#8, labsize(2.5)) title("Positividad COVID-19",size(medium)) xline($linea,lpa(dash))
graph export "Positividad_diaria.png", width (1000)replace 

*******************************************
* Fallecidos y hospitalizados confirmados *
*******************************************

* Hospitalizados totales
line Hospita Día, ylabel(0 2000 4000 6000 8000 10000 12000 14000 16000,labsize(2)) xlabel(#10, labsize(2.5)) title("Nro. total de hospitalizados COVID-19",size(medium)) xline($linea,lpa(dash))
graph export "Hospitalizados.png", width (1000)replace 

* Fallecidos COVID-19 por día:
line falldia_movil7 Día if falldia_movil7<=500, ylabel(#8,labsize(2)) xlabel(#8, labsize(2.5)) title("Fallecidos COVID-19 por día (media móvil)",size(medium)) xline($linea,lpa(dash))
graph export "Fallecidos_diario.png", width (1000)replace 

*******************************************
* Barras de casos y de fallecidos COVID-19*
*******************************************

collapse (sum) Nuevoscasosconfirmadospordía Fallecidospordía,by(semana_nro)
keep if semana_nro>=($semana_fin-3) & semana_nro<=$semana_fin
$etiqueta
label values semana_nro semana

$new_folder
label var Nuevoscasosconfirmadospordía " "
label var Fallecidospordía " "

* Graficos de barras:
** Casos:
 graph bar (asis) Nuevoscasosconfirmadospordía,over(semana_nro) stack blabel(total) ylabel(#4,labsize(2.8)) title("Confirmados COVID-19",size(medium)) legend(off)
graph export "Confirmados_nacional_adv.png", width (1000)replace

** Fallecidos COVID-19:
 graph bar (asis) Fallecidospordía,over(semana_nro) stack blabel(total) ylabel(#4,labsize(2.8)) title("Fallecidos COVID-19",size(medium)) legend(off)
graph export "Fallecidos_C19_nacional_adv.png", width (1000)replace

*******




***************************
* 2. Informacion agregada *
***************************
$bases
import delimited Data_covid_regional_simple, clear
gen year=substr(fecha,1,4)
gen month=substr(fecha,6,2)
gen day=substr(fecha,9,2)
destring (year month day),replace
drop fecha dpto

gen fecha=mdy(month,day,year)
format fecha %d
drop month day year 

* Cambiar aqui (de ser necesario)
drop if fecha>$fecha_fin
gen int semana_nro= (wofd(fecha-3)) - wofd(td($fecha_inicio))

* Etiquetas
$etiqueta
label values semana_nro semana
replace region=proper(region)
replace region="Lima Región" if region=="Lima"
replace region="Lima Metr." if region=="Lima (City)"

** RESUMEN REGIONAL **
preserve
collapse (sum) casosconfirmados fallecidoscovid19 fallecidossinadef,by(region semana_nro)

keep if semana_nro>=($semana_fin-1) & semana_nro<=$semana_fin
foreach x of varlist casosconfirmados- fallecidossinadef{
gen `x'_f=`x' if semana_nro==$semana_fin
replace `x'=. if `x'_f!=.
}
collapse (max) casosconfirmados- fallecidossinadef_f,by(region)

$new_folder
** Graficos:
* Casos confirmados
 graph hbar (asis) casosconfirmados casosconfirmados_f, ///
over(region,sort(casosconfirmados) label(labsize(vsmall))) /*stack*/ bargap(-35) legend(label(1 "$inicio") label(2 "$fin") size(small)) ///
title("Casos COVID-19 confirmados",size(medium)) blabel(fall, position(outside) format(%4.1f)) ytitle("") ylabel(#20,labsize(2))
graph export "Confirmados_regiones.png", width (1000)replace

* Fallecidos COVID-19
 graph hbar (asis) fallecidoscovid19 fallecidoscovid19_f, ///
over(region,sort(fallecidoscovid19) label(labsize(vsmall))) /*stack*/ bargap(-35) legend(label(1 "$inicio") label(2 "$fin") size(small)) ///
title("Fallecidos COVID-19",size(medium)) blabel(fall, position(outside) format(%4.1f)) ytitle("") ylabel(#20,labsize(2))
graph export "Fallecidos_C19_regiones.png", width (1000)replace

* Fallecidos SINADEF
 graph hbar (asis) fallecidossinadef fallecidossinadef_f, ///
over(region,sort(fallecidoscovid19) label(labsize(vsmall))) /*stack*/ bargap(-35) legend(label(1 "$inicio") label(2 "$fin") size(small)) ///
title("Fallecidos por toda causa (SINADEF)",size(medium)) blabel(fall, position(outside) format(%4.1f)) ytitle("") ylabel(#20,labsize(2))
graph export "Fallecidos_SIN_regiones.png", width (1000)replace
restore

** RESUMEN GENERAL **
preserve
collapse (sum) casosconfirmados fallecidoscovid19 fallecidossinadef,by(semana_nro)
keep if semana_nro>=($semana_fin-3) & semana_nro<=$semana_fin

label values semana_nro semana 

label var casosconfirmados " "
label var fallecidoscovid19 " "
label var fallecidossinadef " "

* Graficos de barras:
** Casos:
 graph bar (asis) casosconfirmados,over(semana_nro) stack blabel(total) ylabel(#4,labsize(2.8)) title("Confirmados COVID-19",size(medium)) legend(off)
graph export "Confirmados_nacional.png", width (1000)replace

** Fallecidos COVID-19:
 graph bar (asis) fallecidoscovid19,over(semana_nro) stack blabel(total) ylabel(#4,labsize(2.8)) title("Fallecidos COVID-19",size(medium)) legend(off)
graph export "Fallecidos_C19_nacional.png", width (1000)replace

** Fallecidos en total:
 graph bar (asis) fallecidossinadef,over(semana_nro) stack blabel(total) ylabel(#4,labsize(2.8)) title("Fallecidos por toda causa (SINADEF)",size(medium)) legend(off)
graph export "Fallecidos_SIN_nacional.png", width (1000)replace
restore


** FALLECIDOS GENERAL POR SEXO Y GRUPO ETARIO:
preserve
collapse (sum) casosconfirmados fallecidoscovid19 fallecidossinadef,by(semana_nro sexo grupoetario)
label values semana_nro semana 

keep if semana_nro>=($semana_fin-1) & semana_nro<=$semana_fin
foreach x of varlist casosconfirmados- fallecidossinadef{
gen `x'_f=`x' if semana_nro==$semana_fin
replace `x'=. if `x'_f!=.
}
collapse (max) casosconfirmados- fallecidossinadef_f,by(grupoetario sexo)

$new_folder
** Graficos:
* Casos confirmados
 graph hbar (asis) casosconfirmados casosconfirmados_f , by(sexo) ///
over(grupoetario,sort(casosconfirmados) label(labsize(vsmall))) /*stack*/ bargap(-35) legend(label(1 "$inicio") label(2 "$fin") size(small)) ///
title("Casos confirmados por grupo etario",size(medium)) blabel(fall, position(outside) format(%4.1f)) ytitle("") ylabel(#10,labsize(2))
graph export "Confirmados_etario.png", width (1000)replace

* Fallecidos COVID-19 confirmados
 graph hbar (asis) fallecidoscovid19 fallecidoscovid19_f , by(sexo) ///
over(grupoetario,sort(fallecidoscovid19) label(labsize(vsmall))) /*stack*/ bargap(-35) legend(label(1 "$inicio") label(2 "$fin") size(small)) ///
title("Fallecidos COVID-19",size(medium)) blabel(fall, position(outside) format(%4.1f)) ytitle("") ylabel(#10,labsize(2))
graph export "Fallecidos_C19_etario.png", width (1000)replace

* Fallecidos en total
 graph hbar (asis) fallecidossinadef fallecidossinadef_f , by(sexo) ///
over(grupoetario,sort(fallecidossinadef) label(labsize(vsmall))) /*stack*/ bargap(-35) legend(label(1 "$inicio") label(2 "$fin") size(small)) ///
title("Fallecidos en total",size(medium)) blabel(fall, position(outside) format(%4.1f)) ytitle("") ylabel(#8,labsize(2))
graph export "Fallecidos_SIN_etario.png", width (1000)replace
restore


*****************
* 3. Vacunacion *
*****************
$bases
import delimited using "Vacunacion actual", clear
gen year=substr(fecha,1,4)
gen month=substr(fecha,6,2)
gen day=substr(fecha,9,2)
destring (year month day),replace
drop fecha 

gen fecha=mdy(month,day,year)
format fecha %d
drop month day year 

* Cambiar aqui (de ser necesario)
drop if fecha>$fecha_fin
gen int semana_nro= (wofd(fecha-3)) - wofd(td($fecha_inicio))

* Etiquetas
$etiqueta
label values semana_nro semana
replace region=proper(region)
replace region="Lima Región" if region=="Lima"
replace region="Lima Metr." if region=="Lima (City)"

** RESUMEN REGIONAL **
preserve
collapse (sum) vacunados,by(region semana_nro)

keep if semana_nro>=($semana_fin-1) & semana_nro<=$semana_fin
gen vacunados_f=vacunados if semana_nro==$semana_fin
replace vacunados=. if vacunados_f!=.

collapse (sum) vacunados vacunados_f,by(region)

$new_folder
** Graficos:
* Vacunas aplicadas
 graph hbar (asis) vacunados vacunados_f, ///
over(region,sort(vacunados) label(labsize(vsmall))) /*stack*/ bargap(-35) legend(label(1 "$inicio") label(2 "$fin") size(small)) ///
title("Vacunas aplicadas",size(medium)) blabel(fall, position(outside) format(%4.1f)) ytitle("") ylabel(#20,labsize(2))
graph export "Aplicaciones_regiones.png", width (1000)replace
restore

** RESUMEN GENERAL **
preserve
collapse (sum) vacunados,by(semana_nro)
keep if semana_nro>=($semana_fin-3) & semana_nro<=$semana_fin

*$etiqueta
label values semana_nro semana
label var vacunados " "

* Graficos de barras:
** Casos:
graph bar (asis) vacunados,over(semana_nro) stack blabel(total) ylabel(#4,labsize(2.8)) title("Vacunas aplicadas",size(medium)) legend(off) 
graph export "Aplicaciones_nacional.png", width (1000)replace
restore

collapse (sum)vacunados,by(semana_nro)
keep if semana_nro>=($semana_fin-3) & semana_nro<=$semana_fin
