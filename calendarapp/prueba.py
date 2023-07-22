from django.db.models import Q
from datetime import date, datetime, time, timedelta
#from accounts.models.user import FuncionarioDocente
from calendarapp.models.event import  Cita
from models.calendario import HorarioSemestral, Dia, Convocatoria
from django.core import serializers
import pandas as pd

tipo = 'tutoria'
func_doc = 3 #Luis Diaz
horarios_disponibles= []

if tipo== "tutoria":
    actividades_academicas= Cita.objects.filter(Q(id_cita__datetime_inicio_estimado__gt=datetime.now()) | Q(id_cita__datetime_inicio_real__gt=datetime.now()), es_tutoria=True, id_cita__id_funcionario_docente_encargado= func_doc, id_cita__id_estado_actividad_academica__descripcion_estado_actividad_academica__contains='pendiente').values('id_cita__datetime_inicio_estimado')
    
elif tipo== "ori_academica":
    actividades_academicas= Cita.objects.filter(Q(id_cita__datetime_inicio_estimado__gt=datetime.now()) | Q(id_cita__datetime_inicio_real__gt=datetime.now()), es_orientacion_academica=True, id_cita__id_funcionario_docente_encargado= func_doc, id_cita__id_estado_actividad_academica__descripcion_estado_actividad_academica__contains='pendiente').values('id_cita__datetime_inicio_estimado')
else:
    actividades_academicas= []
    
print(actividades_academicas)

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
    #dt_aa= pd.DataFrame([{'fecha': date(2000, 12, 31) , 'hora_inicio': time(0, 0, 0)}])
    dt_aa= pd.DataFrame([])


# df2= pd.DataFrame([{'fecha': date(2023, 7, 19),	'hora_inicio': time(13,20,00), 	'hora_fin': time(14, 00, 00),'dia': 'Miércoles',  'convocatoria' : 1},
#                    {'fecha': date(2023, 7, 19),	'hora_inicio': time(16,00,00), 	'hora_fin': time(15, 40, 00),'dia': 'Miércoles',  'convocatoria' : 1},
#                    {'fecha': date(2023, 7, 19),	'hora_inicio': time(14,00,00), 	'hora_fin': time(14, 40, 00),'dia': 'Miércoles',  'convocatoria' : 1},
#                    {'fecha': date(2023, 7, 19),	'hora_inicio': time(12,40,00), 	'hora_fin': time(13, 20, 00),'dia': 'Miércoles',  'convocatoria' : 1},
#                    {'fecha': date(2023, 7, 19),	'hora_inicio': time(13,40,00), 	'hora_fin': time(15, 20, 00),'dia': 'Miércoles',  'convocatoria' : 1},
#                    {'fecha': date(2023, 7, 19),	'hora_inicio': time(14,20,00), 	'hora_fin': time(16, 00, 00),'dia': 'Miércoles',  'convocatoria' : 1},
#                    {'fecha': date(2023, 7, 19),	'hora_inicio': time(15,20,00), 	'hora_fin': time(18, 00, 00),'dia': 'Miércoles',  'convocatoria' : 1},
#                    {'fecha': date(2023, 7, 19),	'hora_inicio': time(17,00,00), 	'hora_fin': time(12, 40, 00),'dia': 'Miércoles',  'convocatoria' : 1},
#                    {'fecha': date(2023, 7, 19),	'hora_inicio': time(16,40,00), 	'hora_fin': time(17, 20, 00),'dia': 'Miércoles',  'convocatoria' : 1}
#                    ])

#excluir los horarios que ya se encuentren reservados 
''' agregamos una columna llamada '_merge' con la etiqueta del origen de cada registro ('both', 'left_only' o 'right_only') utilizando el parámetro indicator=True.
 Merge de los dataframes con indicator=True'''
 
df2= pd.DataFrame([])
 
#  si el fun/doc no tiene ningun calendario disponible devolver lista vacia,
#en caso que no tenga datos los horarios vamos a crear uno vacio

#df2 = pd.DataFrame([{'fecha': date(200, 12, 31) , 'hora_inicio': time(1, 0, 0), 'hora_fin': time(0, 0, 0), "dia": '', "convocatoria": 0}])

    
#  si no exite otras citas y tiene calendario devolver los horarios sin exclusion
#  si tiene calendario y hay casos para exluir se procede a hacer la exclsion


#preguntamos si es que ambos dt estan con datos entones hacemos la exclusion

merged_df = df2.merge(dt_aa, on=['fecha', 'hora_inicio'], how='left', indicator=True)
df_filtered = merged_df[merged_df['_merge'] == 'left_only'].drop(columns=['_merge'])
horarios_disponibles= df_filtered

'''Finalmente, filtramos los registros que solo están presentes en el primer dataframe (etiqueta 'left_only') y eliminamos la columna '_merge' para 
obtener el resultado deseado en el dataframe df_filtered.'''
# Filtrar los registros que solo están en el primer dataframe


# dt_aa= pd.DataFrame ([{'fecha': date(2023,7,19), 'hora_inicio': time(16, 00 , 00)},  
#                       {'fecha': date(2023,7,19), 'hora_inicio': time(16, 00 , 00)}])



#dt_aa= pd.DataFrame([{'fecha': date(2000, 12, 31) , 'hora_inicio': time(0, 0, 0)}])
    

