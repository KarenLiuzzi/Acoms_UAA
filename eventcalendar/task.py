# eventcalendar/tasks.py
from celery import shared_task
import json
import requests
from calendarapp.models.event import Event
from accounts.models.user import TipoDocumento, Persona, Alumno, Facultad, Departamento, Carrera, CarreraAlumno, Materia, MateriaCarrera
from django.db import transaction
from datetime import datetime
today = datetime.now()
hoy = today.strftime("%d_%m_%Y_%H_%M_%S")

@shared_task
def importar_datos():
    
    ###########################################
    ############Tabla Tipo Documento###########
    ###########################################
    
    #Preparamos los datos para la solicitud
    url =  'https://'
    headers = {
        'Authorization': '123456',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    proxy_servers = { 'http': 'http://10.10.10.1:8080', 'https': 'http://10.10.10.1:8080'}
    
    # Realizar la solicitud HTTP a un servicio web externo
    response = requests.get(url, headers=headers, proxies= proxy_servers)
    
    if (199 < response.status_code < 300):

        # Procesar los datos y volcarlos en la base de datos
        datos = response.json() 
        #supongamos que los datos nos trae de esta manera
        datos= {
            {
            'id': '1',
            'descripcion_tipo_documento':'CI'
            },
            {
            'id': '2',
            'descripcion_tipo_documento':'RUC'
            },
            {
            'id': '3',
            'descripcion_tipo_documento':'Pasaporte'
            },
        }
        for dato in datos:
            try:
                with transaction.atomic():
                    descripcion_tipo_documento = dato['descripcion_tipo_documento']
                    # Intenta actualizar el registro si ya existe, o crea uno nuevo si no existe
                    tipo_documento, created = TipoDocumento.objects.update_or_create(
                        descripcion_tipo_documento=descripcion_tipo_documento,
                        defaults={'descripcion_tipo_documento': descripcion_tipo_documento}  
                    )
            except Exception as e:
                print(f'Error al insertar datos de TipoDocumento: {str(e)}')

    # SI LA RESPUESTA DA ERROR, VOLCAMOS LOS DATOS EN UN BLOC DE NOTAS
    #respuestas incorrectas lado del cliente
    elif (199 < response.status_code < 300):
        #Vamos a guardar los datos en un txt
        cod_error= str(response.status_code)
        JSON = response.json()
        crear_archivo_error(JSON, cod_error, 'TipoDocumento')

    # respuestas incorrectas lado del servidor
    elif (199 < response.status_code < 300):
        # Vamos a guardar los datos en un txt
        cod_error = str(response.status_code)
        JSON = response.json()
        crear_archivo_error(JSON, cod_error, 'TipoDocumento')
        
    
    ###########################################
    ###############Tabla Persona###############
    ###########################################
    
    #Preparamos los datos para la solicitud
    url =  'https://'
    headers = {
        'Authorization': '123456',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    proxy_servers = { 'http': 'http://10.10.10.1:8080', 'https': 'http://10.10.10.1:8080'}
    
    # Realizar la solicitud HTTP a un servicio web externo
    response = requests.get(url, headers=headers, proxies= proxy_servers)
    
    if (199 < response.status_code < 300):

        # Procesar los datos y volcarlos en la base de datos
        datos = response.json() 
        #supongamos que los datos nos trae de esta manera
        datos= {
            {
            'id': '1',
            'tipo_documento':'CI',
            'nro_documento': '123333',
            'nombre': 'Luis',
            'apellido': 'Diaz',
            'telefono':'021666888',
            'celular': '0984555555',
            'email': 'luis.diaz@gmail.com',
            },
            {
            'id': '2',
            'tipo_documento':'CI',
            'nro_documento': '321111',
            'nombre': 'Lorena',
            'apellido': 'Gonzalez',
            'telefono':'021888999',
            'celular': '0984555555',
            'email': 'lore.gonzalez@gmail.com',
            },
            {
            'id': '3',
            'tipo_documento':'CI',
            'nro_documento': '654666',
            'nombre': 'Federico',
            'apellido': 'Gimenez',
            'telefono':'021333444',
            'celular': '0984555555',
            'email': 'fede.gimenez@gmail.com',
            },
        }
        for dato in datos:
            try:
                with transaction.atomic():
                    tipo_documento = dato['tipo_documento']
                    #traemos la instancia del tipo documento
                    ins_documento= TipoDocumento.objects.filter(descripcion_tipo_documento= tipo_documento).first()
                    nro_documento= dato['nro_documento']
                    nombre= dato['nombre']
                    apellido= dato['apellido']
                    telefono= dato['telefono']
                    email=  dato['email']
                    celular= dato['celular']
                    
                    # Intenta actualizar el registro si ya existe, o crea uno nuevo si no existe
                    persona, created = Persona.objects.update_or_create(
                        documento=nro_documento,
                        defaults={'id_tipo_documento': ins_documento, 'documento': nro_documento, 'nombre': nombre, 'apellido': apellido, 'correo': email, 'telefono': telefono, 'celular': celular}  
                    )
            
            except Exception as e:
                print(f'Error al insertar datos de persona: {str(e)}')

    # SI LA RESPUESTA DA ERROR, VOLCAMOS LOS DATOS EN UN BLOC DE NOTAS
    #respuestas incorrectas lado del cliente
    elif (199 < response.status_code < 300):
        #Vamos a guardar los datos en un txt
        cod_error= str(response.status_code)
        JSON = response.json()
        crear_archivo_error(JSON, cod_error, 'Persona')

    # respuestas incorrectas lado del servidor
    elif (199 < response.status_code < 300):
        # Vamos a guardar los datos en un txt
        cod_error = str(response.status_code)
        JSON = response.json()
        crear_archivo_error(JSON, cod_error, 'Persona')
        
    
    ###########################################
    ###################Alumno##################
    ###########################################
    
    #Preparamos los datos para la solicitud
    url =  'https://'
    headers = {
        'Authorization': '123456',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    proxy_servers = { 'http': 'http://10.10.10.1:8080', 'https': 'http://10.10.10.1:8080'}
    
    # Realizar la solicitud HTTP a un servicio web externo
    response = requests.get(url, headers=headers, proxies= proxy_servers)
    
    if (199 < response.status_code < 300):

        # Procesar los datos y volcarlos en la base de datos
        datos = response.json() 
        #supongamos que los datos nos trae de esta manera
        datos= {
            {
            'id': '1',
            'documento': '123333'
            },
            {
            'id': '2',
            'documento': '321111'
            },
            {
            'id': '3',
            'documento': '654666'
            },
        }
        for dato in datos:
            try:
                with transaction.atomic():
                    documento = dato['documento']
                    ins_alumno= Persona.objects.filter(documento= documento).first()
                    # Intenta actualizar el registro si ya existe, o crea uno nuevo si no existe
                    alumno, created = Alumno.objects.update_or_create(
                        id_alumno=ins_alumno,
                        defaults={'id_alumno': ins_alumno}  
                    )
            
            except Exception as e:
                print(f'Error al insertar datos de alumno: {str(e)}')
                
    # SI LA RESPUESTA DA ERROR, VOLCAMOS LOS DATOS EN UN BLOC DE NOTAS
    #respuestas incorrectas lado del cliente
    elif (199 < response.status_code < 300):
        #Vamos a guardar los datos en un txt
        cod_error= str(response.status_code)
        JSON = response.json()
        crear_archivo_error(JSON, cod_error, 'Alumno')

    # respuestas incorrectas lado del servidor
    elif (199 < response.status_code < 300):
        # Vamos a guardar los datos en un txt
        cod_error = str(response.status_code)
        JSON = response.json()
        crear_archivo_error(JSON, cod_error, 'Alumno')
                
    
    ###########################################
    ##############Tabla Facultad ##############
    ###########################################
    
    #Preparamos los datos para la solicitud
    url =  'https://'
    headers = {
        'Authorization': '123456',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    proxy_servers = { 'http': 'http://10.10.10.1:8080', 'https': 'http://10.10.10.1:8080'}
    
    # Realizar la solicitud HTTP a un servicio web externo
    response = requests.get(url, headers=headers, proxies= proxy_servers)
    
    if (199 < response.status_code < 300):

        # Procesar los datos y volcarlos en la base de datos
        datos = response.json() 
        #supongamos que los datos nos trae de esta manera
        datos= {
            {
            'id': '1',
            'descripcion_facultad':'Facultad de Ciencias y Tecnología'
            },
            {
            'id': '2',
            'descripcion_facultad':'Facultad de Ciencias Económicas y Empresariales'
            },
            {
            'id': '3',
            'descripcion_facultad':'Facultad de Ciencias Jurídicas, Políticas y Sociales'
            },
        }
        for dato in datos:
            try:
                with transaction.atomic():
                    descripcion_facultad = dato['descripcion_facultad']
                    # Intenta actualizar el registro si ya existe, o crea uno nuevo si no existe
                    facultad, created = Facultad.objects.update_or_create(
                        descripcion_facultad=descripcion_facultad,
                        defaults={'descripcion_facultad': descripcion_facultad}  
                    )
            
            except Exception as e:
                print(f'Error al insertar datos de facultad: {str(e)}')
                

    # SI LA RESPUESTA DA ERROR, VOLCAMOS LOS DATOS EN UN BLOC DE NOTAS
    #respuestas incorrectas lado del cliente
    elif (199 < response.status_code < 300):
        #Vamos a guardar los datos en un txt
        cod_error= str(response.status_code)
        JSON = response.json()
        crear_archivo_error(JSON, cod_error, 'Facultad')

    # respuestas incorrectas lado del servidor
    elif (199 < response.status_code < 300):
        # Vamos a guardar los datos en un txt
        cod_error = str(response.status_code)
        JSON = response.json()
        crear_archivo_error(JSON, cod_error, 'Facultad')


    ###########################################
    ##############Tabla Departamento###########
    ###########################################
    
    #Preparamos los datos para la solicitud
    url =  'https://'
    headers = {
        'Authorization': '123456',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    proxy_servers = { 'http': 'http://10.10.10.1:8080', 'https': 'http://10.10.10.1:8080'}
    
    # Realizar la solicitud HTTP a un servicio web externo
    response = requests.get(url, headers=headers, proxies= proxy_servers)
    
    if (199 < response.status_code < 300):

        # Procesar los datos y volcarlos en la base de datos
        datos = response.json() 
        #supongamos que los datos nos trae de esta manera
        datos= {
            {
            'id': '1',
            'descripcion_departamento':'Departamento de Informática',
            'facultad': 'Facultad de Ciencias y Tecnología',
            'telefono': '021456789',
            },
            {
            'id': '2',
            'descripcion_departamento':'Departamento de E-learning',
            'facultad': 'Facultad de Ciencias y Tecnología',
            'telefono': '021035604',
            },
            {
            'id': '3',
            'descripcion_departamento':'Departamento de Ciencias Exactas',
            'facultad': 'Facultad de Ciencias y Tecnología',
            'telefono': '021946845',
            },
        }
        for dato in datos:
            try:
                with transaction.atomic():
                    descripcion_departamento = dato['descripcion_departamento']
                    facultad = dato['facultad']
                    #Traemos la instancia de facultad que coincida con la descripcion
                    ins_facultad= Facultad.objects.filter(descripcion_facultad= facultad).first()
                    telefono = dato['telefono']
                    # Intenta actualizar el registro si ya existe, o crea uno nuevo si no existe
                    departamento, created = Departamento.objects.update_or_create(
                        descripcion_departamento=descripcion_departamento, id_facultad= ins_facultad,
                        defaults={'descripcion_departamento': descripcion_departamento, 'id_facultad': ins_facultad , 'telefono': telefono}  
                    )
            except Exception as e:
                print(f'Error al insertar datos de Departamento: {str(e)}')
                

    # SI LA RESPUESTA DA ERROR, VOLCAMOS LOS DATOS EN UN BLOC DE NOTAS
    #respuestas incorrectas lado del cliente
    elif (199 < response.status_code < 300):
        #Vamos a guardar los datos en un txt
        cod_error= str(response.status_code)
        JSON = response.json()
        crear_archivo_error(JSON, cod_error, 'Departamento')

    # respuestas incorrectas lado del servidor
    elif (199 < response.status_code < 300):
        # Vamos a guardar los datos en un txt
        cod_error = str(response.status_code)
        JSON = response.json()
        crear_archivo_error(JSON, cod_error, 'Departamento')
        
        
    ###########################################
    ################Tabla Carrera##############
    ###########################################
    
    #Preparamos los datos para la solicitud
    url =  'https://'
    headers = {
        'Authorization': '123456',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    proxy_servers = { 'http': 'http://10.10.10.1:8080', 'https': 'http://10.10.10.1:8080'}
    
    # Realizar la solicitud HTTP a un servicio web externo
    response = requests.get(url, headers=headers, proxies= proxy_servers)
    
    if (199 < response.status_code < 300):

        # Procesar los datos y volcarlos en la base de datos
        datos = response.json() 
        #supongamos que los datos nos trae de esta manera
        datos= {
            {
            'id': '1',
            'descripcion_carrera': 'Ingeniería en Informática Énfasis en: Ciencias de la Computación',
            'facultad': 'Facultad de Ciencias y Tecnología'
            },
            {
            'id': '2',
            'descripcion_carrera':'Ingeniería en Informática Énfasis en: Sistemas Informáticos',
            'facultad': 'Facultad de Ciencias y Tecnología'
            },
            {
            'id': '3',
            'descripcion_carrera':'Licenciatura en Ciencias Informáticas Énfasis en: Bases de Datos',
            'facultad': 'Facultad de Ciencias y Tecnología'
            },
        }
        for dato in datos:
            try:
                with transaction.atomic():
                    descripcion_carrera = dato['descripcion_carrera']
                    facultad= dato['facultad']
                    #Traemos la instancia de facultad que coincida con la descripcion
                    ins_facultad= Facultad.objects.filter(descripcion_facultad= facultad).first()
                    
                    # Intenta actualizar el registro si ya existe, o crea uno nuevo si no existe
                    facultad, created = Carrera.objects.update_or_create(
                        descripcion_carrera=descripcion_carrera, id_facultad= ins_facultad,
                        defaults={'descripcion_carrera': descripcion_carrera, 'id_facultad': ins_facultad}  
                    )
            
            except Exception as e:
                print(f'Error al insertar datos de Carrera: {str(e)}')
                

    # SI LA RESPUESTA DA ERROR, VOLCAMOS LOS DATOS EN UN BLOC DE NOTAS
    #respuestas incorrectas lado del cliente
    elif (199 < response.status_code < 300):
        #Vamos a guardar los datos en un txt
        cod_error= str(response.status_code)
        JSON = response.json()
        crear_archivo_error(JSON, cod_error, 'Carrera')

    # respuestas incorrectas lado del servidor
    elif (199 < response.status_code < 300):
        # Vamos a guardar los datos en un txt
        cod_error = str(response.status_code)
        JSON = response.json()
        crear_archivo_error(JSON, cod_error, 'Carrera')
        
        
    ###########################################
    ############Tabla CarreraAlumno############
    ###########################################
    
    #Preparamos los datos para la solicitud
    url =  'https://'
    headers = {
        'Authorization': '123456',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    proxy_servers = { 'http': 'http://10.10.10.1:8080', 'https': 'http://10.10.10.1:8080'}
    
    # Realizar la solicitud HTTP a un servicio web externo
    response = requests.get(url, headers=headers, proxies= proxy_servers)
    
    if (199 < response.status_code < 300):

        # Procesar los datos y volcarlos en la base de datos
        datos = response.json() 
        #supongamos que los datos nos trae de esta manera
        datos= {
            {
            'id': '1',
            'descripcion_carrera': 'Ingeniería en Informática Énfasis en: Ciencias de la Computación',
            'documento_alumno': '123333'
            },
            {
            'id': '2',
            'descripcion_carrera':'Ingeniería en Informática Énfasis en: Sistemas Informáticos',
            'documento_alumno': '321111'
            },
            {
            'id': '3',
            'descripcion_carrera':'Licenciatura en Ciencias Informáticas Énfasis en: Bases de Datos',
            'documento_alumno': '654666'
            },
        }
        for dato in datos:
            try:
                with transaction.atomic():
                    descripcion_carrera = dato['descripcion_carrera']
                    documento_alumno= dato['documento_alumno']
                    #Traemos la instancia de Alumno que coincida con el nro de documento
                    ins_alumno= Alumno.objects.filter(id_alumno__documento= documento_alumno).first()
                    #Traemos la instancia de carrera que coincida con la descripción
                    ins_carrera= Carrera.objects.filter(descripcion_carrera= descripcion_carrera).first()
                    
                    # Intenta actualizar el registro si ya existe, o crea uno nuevo si no existe
                    carrera_alumno, created = CarreraAlumno.objects.update_or_create(
                        id_alumno=ins_alumno, id_carrera= ins_carrera,
                        defaults={'id_alumno': ins_alumno, 'id_carrera': ins_carrera}  
                    )
            
            except Exception as e:
                print(f'Error al insertar datos de CarreraAlumno: {str(e)}')
                

    # SI LA RESPUESTA DA ERROR, VOLCAMOS LOS DATOS EN UN BLOC DE NOTAS
    #respuestas incorrectas lado del cliente
    elif (199 < response.status_code < 300):
        #Vamos a guardar los datos en un txt
        cod_error= str(response.status_code)
        JSON = response.json()
        crear_archivo_error(JSON, cod_error, 'CarreraAlumno')

    # respuestas incorrectas lado del servidor
    elif (199 < response.status_code < 300):
        # Vamos a guardar los datos en un txt
        cod_error = str(response.status_code)
        JSON = response.json()
        crear_archivo_error(JSON, cod_error, 'CarreraAlumno')



    ###########################################
    ###############Tabla Materia###############
    ###########################################
    
    #Preparamos los datos para la solicitud
    url =  'https://'
    headers = {
        'Authorization': '123456',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    proxy_servers = { 'http': 'http://10.10.10.1:8080', 'https': 'http://10.10.10.1:8080'}
    
    # Realizar la solicitud HTTP a un servicio web externo
    response = requests.get(url, headers=headers, proxies= proxy_servers)
    
    if (199 < response.status_code < 300):

        # Procesar los datos y volcarlos en la base de datos
        datos = response.json() 
        #supongamos que los datos nos trae de esta manera
        datos= {
            {
            'id': '1',
            'descripcion_materia': 'INTRODUCCIÓN A LAS TECNOLOGÍAS DE INFORMACIÓN Y LA COMUNICACIÓN',
            'departamento': 'Departamento de E-learning'
            },
            {
            'id': '2',
            'descripcion_materia':'TRABAJO DE GRADO PARA INGENIERÍA EN INFORMÁTICA ÉNFASIS CIENCIAS DE COMPUTACIÓN',
            'departamento': 'Departamento de Informática'
            },
            {
            'id': '3',
            'descripcion_materia':'PROGRAMACIÓN SQL',
            'departamento': 'Departamento de Informática'
            },
        }
        for dato in datos:
            try:
                with transaction.atomic():
                    descripcion_materia = dato['descripcion_materia']
                    departamento= dato['departamento']
                    #Traemos la instancia de departamento que coincida con la descripción
                    ins_departamento= Departamento.objects.filter(descripcion_departamento= departamento).first()
                    
                    # Intenta actualizar el registro si ya existe, o crea uno nuevo si no existe
                    materia, created = Materia.objects.update_or_create(
                        descripcion_materia=descripcion_materia, id_departamento= ins_departamento,
                        defaults={'descripcion_materia': descripcion_materia, 'id_departamento': ins_departamento}  
                    )
            
            except Exception as e:
                print(f'Error al insertar datos de Materia: {str(e)}')
                

    # SI LA RESPUESTA DA ERROR, VOLCAMOS LOS DATOS EN UN BLOC DE NOTAS
    #respuestas incorrectas lado del cliente
    elif (199 < response.status_code < 300):
        #Vamos a guardar los datos en un txt
        cod_error= str(response.status_code)
        JSON = response.json()
        crear_archivo_error(JSON, cod_error, 'Materia')

    # respuestas incorrectas lado del servidor
    elif (199 < response.status_code < 300):
        # Vamos a guardar los datos en un txt
        cod_error = str(response.status_code)
        JSON = response.json()
        crear_archivo_error(JSON, cod_error, 'Materia')
        
        
    ###########################################
    ##########Tabla MateriaCarrera#############
    ###########################################
    
    #Preparamos los datos para la solicitud
    url =  'https://'
    headers = {
        'Authorization': '123456',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    proxy_servers = { 'http': 'http://10.10.10.1:8080', 'https': 'http://10.10.10.1:8080'}
    
    # Realizar la solicitud HTTP a un servicio web externo
    response = requests.get(url, headers=headers, proxies= proxy_servers)
    
    if (199 < response.status_code < 300):

        # Procesar los datos y volcarlos en la base de datos
        datos = response.json() 
        #supongamos que los datos nos trae de esta manera
        datos= {
            {
            'id': '1',
            'descripcion_materia': 'INTRODUCCIÓN A LAS TECNOLOGÍAS DE INFORMACIÓN Y LA COMUNICACIÓN',
            'carrera': 'Ingeniería en Informática Énfasis en: Sistemas Informáticos'
            },
            {
            'id': '2',
            'descripcion_materia':'TRABAJO DE GRADO PARA INGENIERÍA EN INFORMÁTICA ÉNFASIS CIENCIAS DE COMPUTACIÓN',
            'carrera': 'Ingeniería en Informática Énfasis en: Ciencias de la Computación'
            },
            {
            'id': '3',
            'descripcion_materia':'PROGRAMACIÓN SQL',
            'carrera': 'Ingeniería en Informática Énfasis en: Sistemas Informáticos'
            },
        }
        for dato in datos:
            try:
                with transaction.atomic():
                    descripcion_materia = dato['descripcion_materia']
                    carrera= dato['carrera']
                    #Traemos la instancia de Carrera que coincida con la descripción
                    ins_carrera= Carrera.objects.filter(descripcion_carrera= descripcion_materia).first()
                    #Traemos la instancia de Carrera que coincida con la descripción
                    ins_materia= Materia.objects.filter(descripcion_materia= carrera).first()
                    
                    # Intenta actualizar el registro si ya existe, o crea uno nuevo si no existe
                    materiacarrera, created = MateriaCarrera.objects.update_or_create(
                        id_carrera= ins_carrera, id_materia= ins_materia, 
                        defaults={'id_carrera': ins_carrera, 'id_materia': ins_materia}  
                    )
            
            except Exception as e:
                print(f'Error al insertar datos de MateriaCarrera: {str(e)}')
                

    # SI LA RESPUESTA DA ERROR, VOLCAMOS LOS DATOS EN UN BLOC DE NOTAS
    #respuestas incorrectas lado del cliente
    elif (199 < response.status_code < 300):
        #Vamos a guardar los datos en un txt
        cod_error= str(response.status_code)
        JSON = response.json()
        crear_archivo_error(JSON, cod_error, 'MateriaCarrera')

    # respuestas incorrectas lado del servidor
    elif (199 < response.status_code < 300):
        # Vamos a guardar los datos en un txt
        cod_error = str(response.status_code)
        JSON = response.json()
        crear_archivo_error(JSON, cod_error, 'MateriaCarrera')
    

    def crear_archivo_error(json, cod, tabla):
        #cambiar la direccion de almacenamiento del archivo una vez este en producción
        data= json
        cod= cod
        with open('C:\\Users\\equipo\\Documents\\Errores\\Error_Tipo_' + tabla + '_' + cod + '_' + hoy + '.txt', 'w') as json_file:
            json.dump(data, json_file)
    