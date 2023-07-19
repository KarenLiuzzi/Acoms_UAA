from datetime import datetime, date, time, timedelta
#from accounts.models.user import FuncionarioDocente
from calendarapp.models.event import Parametro, Cita
from calendarapp.models.calendario import HorarioSemestral, Dia, Convocatoria
from django.core import serializers
import pandas as pd

'''------------logica para obtener los horarios disponibles del funcionario/docente de acuerdo al horario del mismo y si este rango }
de horarios aun se encuentra disponible-------'''

tipo = 'tutoria'
func_doc = 3 #Luis Diaz

#funcion para generar los horarios
def dividir_horarios_por_minuto(minutos, hora_inicio, hora_fin, dia, id_convocatoria):
    # Convertir los horarios de strings a objetos datetime
    hora_inicio = datetime.strptime(hora_inicio, '%H:%M:%S').time()
    hora_fin = datetime.strptime(hora_fin, '%H:%M:%S').time()

    # Calcular la diferencia en minutos entre la hora de inicio y fin
    diferencia = timedelta(hours=hora_fin.hour, minutes=hora_fin.minute) - timedelta(hours=hora_inicio.hour, minutes=hora_inicio.minute)
    minutos_totales = int(diferencia.total_seconds() / 60)

    # Dividir la diferencia en minutos según el parámetro "minutos"
    divisiones = []
    for i in range(minutos, minutos_totales + minutos, minutos):
        hora_inicio_division = (datetime.combine(datetime.today(), hora_inicio) + timedelta(minutes=i-minutos)).time()
        hora_fin_division = (datetime.combine(datetime.today(), hora_inicio) + timedelta(minutes=i)).time()

        if(hora_fin_division <= hora_fin):
            divisiones.append({"hora_inicio": hora_inicio_division, "hora_fin":hora_fin_division, "dia": dia, "id_convocatoria": id_convocatoria})

    return divisiones


#el parametro cargaremos en minutos y ese vamos a tomar como valor para poder calcular el tiempo de proceso entre horarios del funcionario/docente
#primero traemos el parametro de minutos que se encuentra disponible de acuerdo a la actividad academica (tuto u orie academ )
if tipo== "tutoria":
    parametro = Parametro.objects.filter(es_tutoria= True, id_unidad_medida__descripcion_unidad_medida__contains='minutos').values('valor')
    parametro= parametro[0]['valor']
    
elif tipo== "ori_academica":
    parametro = Parametro.objects.filter(es_orientacion_academica= True, id_unidad_medida__descripcion_unidad_medida__contains='minutos').values('valor')
    parametro= parametro[0]['valor']
else:
    parametro= 0

#vamos a consultar los horarios cargados del funcionario_docente cuyo semestre aun no haya finalizado
horario_func_doc= HorarioSemestral.objects.filter(id_funcionario_docente= func_doc, id_convocatoria__fecha_fin__gt = datetime.now())
#json_data = serializers.serialize('json', horario_func_doc)
valores= horario_func_doc

#generamos varias listas para agregar las fechas y horas de acuerdo al dia de la semana 
fechas_lunes = []  # Lista para almacenar las fechas de lunes
fechas_martes = []  # Lista para almacenar las fechas de martes
fechas_miercoles = []  # Lista para almacenar las fechas de miercoles
fechas_jueves = []  # Lista para almacenar las fechas de jueves
fechas_viernes = []  # Lista para almacenar las fechas de viernes
fechas_sabado = []  # Lista para almacenar las fechas de sabado
calendario_semestral = [] #lista para guardar los horarios del func/doc con los valores interesados
horarios_finales= [] #lista para ir guardando todos los horarios finales
horas_dia= [] #lista auxiliar para ir iterando los registros de horarios generados para el func/doc por iteracion 


#iteramos cada registro del calendario funcionario/docente y por cada item vamos generando las fechas con los horarios
for item in valores: #este hay que cambiar por el json_data que es el que devuelve los registros del calendario funcionario/docente
    hora_inicio = item['fields']['hora_inicio']
    hora_fin = item['fields']['hora_fin']
    id_convocatoria = item['fields']['id_convocatoria']
    id_dia = item['fields']['id_dia']
    
    calendario_semestral.append({"id_dia": id_dia, "id_convocatoria": id_convocatoria , "hora_inicio": hora_inicio, "hora_fin": hora_fin})

#volvemos a iterar los elementos de la lista construida con los valores seleccionados
for item in calendario_semestral:
    id_dia= item["id_dia"]
    id_convocatoria= item["id_convocatoria"]
    hora_inicio = item['hora_inicio']
    hora_fin = item['hora_fin']

    #tengo que buscar todas las fechas que se generan de acuerdo al dia que cae para el horario, hasta el ultimo dia del semestre
    #antes buscamos el dia 
    
    #generamos los parametros que utilizaremos par extraer las fechas y horarios 
    #traer el dia 
    dia= Dia.objects.filter(id_dia= id_dia).values('descripcion_dia').first()
    dia= dia['descripcion_dia']
    #traer la ultima fecha del semestre
    fin_semestre= Convocatoria.objects.filter(id_convocatoria= id_convocatoria).values('fecha_fin').first()
    
    fecha_inicial = datetime.now()  # Fecha inicial, dia de hoy para generar las citas, inclusive
    fecha_fin = fin_semestre  # Fecha de finalización, inclusive


    #generar todas las fechas por dia de semana para todo el semestre
    while fecha_inicial <= fecha_fin:
        if (fecha_inicial.weekday() == 0 and dia == 'Lunes'):  # 0 corresponde al día lunes
            fechas_lunes.append({"fecha": fecha_inicial.date(), "dia": 'Lunes' })
        elif (fecha_inicial.weekday() == 1 and dia == 'Martes'):
            fechas_martes.append({"fecha": fecha_inicial.date(), "dia": 'Martes' })
        elif (fecha_inicial.weekday() == 2 and dia == 'Miércoles'):
            fechas_miercoles.append({"fecha": fecha_inicial.date(), "dia": 'Miércoles' })
        elif (fecha_inicial.weekday() == 3 and dia == 'Jueves'):
            fechas_jueves.append({"fecha": fecha_inicial.date(), "dia": 'Jueves' })
        elif (fecha_inicial.weekday() == 4 and dia == 'Viernes'):
            fechas_viernes.append({"fecha": fecha_inicial.date(), "dia": 'Viernes' })
        elif (fecha_inicial.weekday() == 5 and dia == 'Sábado'):
            fechas_sabado.append({"fecha": fecha_inicial.date(), "dia": 'Sábado' })
        
        fecha_inicial += timedelta(days=1)


    #una generado todas las fechas de acuerdo al dia correspondiente vamos a crear otro listado con las horas, dias y convocatoria que corresponde
    auxiliar= dividir_horarios_por_minuto(parametro, hora_inicio, hora_fin, dia, id_convocatoria)
    #esto me genera un objeto de tipo lista que posee elementos de tipo lista que a su vez guarda diccionarios
    
    horas_dia.append(auxiliar)
    #recorremos todos los horarios y por cada horario vamos iterando nuevamente las fechas y agregando en la lista final de horarios
    #if (bandera == 0) :

        #print(horas_dia)
    for dato in horas_dia:
        for item in dato:
            hora_inicio = item['hora_inicio']
            hora_fin = item['hora_fin']
            convocatoria= item['id_convocatoria']
            #recorremos la lista de acuerdo al dia y vamos generando los horarios
            if dia == 'Lunes': #preguntamos si el dia el lunes entonces iteramos en los horarios de los lunes 
                #iteramos la lista y a medida que vamos iterando le vamos agregando las horas
                for dt in fechas_lunes:
                    fecha= dt['fecha']
                    dia= dt['dia']
                    horarios_finales.append({"fecha": fecha, "hora_inicio": hora_inicio, "hora_fin": hora_fin, "dia": dia, "convocatoria": convocatoria})
            elif dia == 'Martes': #preguntamos si el dia el martes entonces iteramos en los horarios de los martes 
                #iteramos la lista y a medida que vamos iterando le vamos agregando las horas
                for dt in fechas_martes:
                    fecha= dt['fecha']
                    dia= dt['dia']
                    horarios_finales.append({"fecha": fecha, "hora_inicio": hora_inicio, "hora_fin": hora_fin, "dia": dia, "convocatoria": convocatoria})
            elif dia == 'Miércoles': #preguntamos si el dia el miercoles entonces iteramos en los horarios de los miercoles 
                #iteramos la lista y a medida que vamos iterando le vamos agregando las horas
                for dt in fechas_miercoles:
                    fecha= dt['fecha']
                    dia= dt['dia']
                    horarios_finales.append({"fecha": fecha, "hora_inicio": hora_inicio, "hora_fin": hora_fin, "dia": dia, "convocatoria": convocatoria})
            elif dia == 'Jueves': #preguntamos si el dia el jueves entonces iteramos en los horarios de los jueves 
                #iteramos la lista y a medida que vamos iterando le vamos agregando las horas
                for dt in fechas_jueves:
                    fecha= dt['fecha']
                    dia= dt['dia']
                    horarios_finales.append({"fecha": fecha, "hora_inicio": hora_inicio, "hora_fin": hora_fin, "dia": dia, "convocatoria": convocatoria})

            elif dia == 'Viernes': #preguntamos si el dia el viernes entonces iteramos en los horarios de los viernes 
                #iteramos la lista y a medida que vamos iterando le vamos agregando las horas
                for dt in fechas_viernes:
                    fecha= dt['fecha']
                    dia= dt['dia']
                    horarios_finales.append({"fecha": fecha, "hora_inicio": hora_inicio, "hora_fin": hora_fin, "dia": dia, "convocatoria": convocatoria})

            elif dia == 'Sábado': #preguntamos si el dia el sabado entonces iteramos en los horarios de los sabados 
                #iteramos la lista y a medida que vamos iterando le vamos agregando las horas
                for dt in fechas_sabado:
                    fecha= dt['fecha']
                    dia= dt['dia']
                    horarios_finales.append({"fecha": fecha, "hora_inicio": hora_inicio, "hora_fin": hora_fin, "dia": dia, "convocatoria": convocatoria})

    horas_dia= []

df2 = pd.DataFrame(horarios_finales)

# Convertir en tipos de datos correctos para poder operar
df2['fecha'] = pd.to_datetime(df2['fecha']).dt.date
df2['dia'] = df2['dia'].astype(str)
df2['hora_inicio'] = pd.to_datetime(df2["hora_inicio"].astype(str)).dt.time
df2['hora_fin'] = pd.to_datetime(df2["hora_fin"].astype(str)).dt.time

#ordenamos por fecha 
df2.sort_values(by='fecha', inplace=True)


#procedemos a borrar duplicados
df2.drop_duplicates(keep='first', inplace=True)


# Eliminar registros donde fecha sea hoy y la hora_inicio supere la hora actual
df2.drop(df2[(df2['fecha'] == datetime.now().date()) & (df2['hora_inicio'] < datetime.now().time())].index, inplace=True)
       
#ahora que ya tenemos generado todos los horarios por dias vamos a preguntar cuales de ellos ya estan con estado "Pendiente" para poder excluir
#traer todos los registros de citas donde la convocatoria aun no haya terminado y la fecha sea de hoy con la hora superior a la actual 


from django.db.models import Q

if tipo== "tutoria":
    actividades_academicas= Cita.objects.filter(Q(datetime_inicio_estimado__gt=datetime.now()) | Q(datetime_inicio_real__gt=datetime.now()), es_tutoria=True, id_funcionario_docente_encargado= func_doc).values('datetime_inicio_estimado', 'datetime_inicio_real')
    
elif tipo== "ori_academica":
    actividades_academicas= Cita.objects.filter(Q(datetime_inicio_estimado__gt=datetime.now()) | Q(datetime_inicio_real__gt=datetime.now()), es_orientacion_academica=True, id_funcionario_docente_encargado= func_doc).values('datetime_inicio_estimado', 'datetime_inicio_real')
else:
    actividades_academicas= []
    
#convertimos a un dt 
dt_aa= pd.DataFrame(actividades_academicas)

#creamos una lista auxiliar para ir pasando ahi los items 
lista_provisoria= []

if actividades_academicas: #preguntamos si posee datos 
    for item in actividades_academicas:
            fecha= item['id_cita__datetime_inicio_estimado']            
            lista_provisoria.append({'fecha': fecha,'hora_inicio': fecha})
           
    dt_aa= pd.DataFrame(lista_provisoria)

    dt_aa['fecha'] = pd.to_datetime(dt_aa['fecha']).dt.date
    dt_aa['hora_inicio'] = pd.to_datetime(dt_aa['hora_inicio']).dt.time
    
else:
    #creamos igual forma un dt para evitar errores en el merged 
    dt_aa= pd.DataFrame([{'fecha': date(2000, 12, 31) , 'hora_inicio': time(0, 0, 0)}])
    
    
#excluir los horarios que ya se encuentren reservados 
# Mantener los registros del primer dataframe que no están en el segundo dataframe
''' agregamos una columna llamada '_merge' con la etiqueta del origen de cada registro ('both', 'left_only' o 'right_only') utilizando el parámetro indicator=True.

Finalmente, filtramos los registros que solo están presentes en el primer dataframe (etiqueta 'left_only') y eliminamos la columna '_merge' para 
obtener el resultado deseado en el dataframe df_filtered.'''
# Merge de los dataframes con indicator=True
merged_df = df2.merge(dt_aa, on=['fecha', 'hora_inicio'], how='left', indicator=True)

# Filtrar los registros que solo están en el primer dataframe
df_filtered = merged_df[merged_df['_merge'] == 'left_only'].drop(columns=['_merge'])


df_filtered.to_excel("C:/Users/beatr/Documents/df_sin_duplicados.xlsx", index=False)