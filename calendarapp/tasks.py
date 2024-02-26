
from accounts.models.user import TipoDocumento,  Persona, Alumno, Facultad, Departamento, Carrera, CarreraAlumno, Materia, MateriaCarrera
from celery import shared_task

@shared_task
def importar_datos():
    print('Iniciando la tarea...')
    #Preparamos los datos para la solicitud
    # url =  'https://'
    # headers = {
    #     'Authorization': '123456',
    #     'Content-Type': 'application/json',
    #     'Accept': 'application/json'
    # }
    # proxy_servers = { 'http': 'http://10.10.10.1:8080', 'https': 'http://10.10.10.1:8080'}

    #Realizar la solicitud HTTP a un servicio web externo
    #response = requests.get(url, headers=headers, proxies= proxy_servers)

    #if (199 < response.status_code < 300):

        #Procesar los datos y volcarlos en la base de datos
        #datos = response.json() 
    print('Iniciando Tipo documento...')
    datos= [
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
    ]
    
    try:
        for dato in datos:
            descripcion_tipo_documento = dato['descripcion_tipo_documento'].strip()
            # Intenta actualizar el registro si ya existe, o crea uno nuevo si no existe
            tipo_documento, created = TipoDocumento.objects.update_or_create(
                descripcion_tipo_documento=descripcion_tipo_documento,
                defaults={'descripcion_tipo_documento': descripcion_tipo_documento}  
            )
    except Exception as e:
        print(f'Error al insertar datos de TipoDocumento: {str(e)}')
        contenido= f'Estimad@: Le informamos que ocurrio un problema con el vuelco de datos de la tabla TipoDocumento.  Favor verificar el mismo: {str(e)}.  Atte equipo AcOms.'
        title = 'Error en vuelco de datos AcOMs'
        enviarcorreo(title, contenido)
    else:
        #si todo sale bien llamamos a ejecutar el volcado de Persona
        volcar_Persona()
    finally:
        print('Finalizo tipo Documento...')
        
    #respuestas incorrectas lado del cliente
    # elif (199 < response.status_code < 300):  
    #     error_text = response.text
    #     contenido= f'Estimad@: Le informamos que ocurrio un problema con el vuelco de datos de la tabla TipoDocumento. ' + error_text +  '.  Atte equipo AcOms.'
    #     title = 'Error en vuelco de datos AcOMs'
    #     enviarcorreo(title, contenido)

    # respuestas incorrectas lado del servidor
    # elif (199 < response.status_code < 300):
    #     error_text = response.text
    #     contenido= f'Estimad@: Le informamos que ocurrio un problema con el vuelco de datos de la tabla TipoDocumento. ' + error_text + '.  Atte equipo AcOms.'
    #     title = 'Error en vuelco de datos AcOMs'
    #     enviarcorreo(title, contenido)
        
def volcar_Persona():
    
    # ###########################################
    # ###############Tabla Persona###############
    # ###########################################
    
    print('Iniciando Persona...')
    #Preparamos los datos para la solicitud
    # url = 'https://'
    # headers = {
    # 'Authorization': '123456',
    # 'Content-Type': 'application/json',
    # 'Accept': 'application/json'
    # }
    # proxy_servers = { 'http': 'http://10.10.10.1:8080', 'https': 'http://10.10.10.1:8080'}

    #Realizar la solicitud HTTP a un servicio web externo
    #response = requests.get(url, headers=headers, proxies= proxy_servers)

    #if (199 < response.status_code < 300):

    #Procesar los datos y volcarlos en la base de datos
    #datos = response.json() 
    #supongamos que los datos nos trae de esta manera
    datos= [
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
    ]
    try:
        for dato in datos: 
            tipo_documento = dato['tipo_documento'].strip()
            #traemos la instancia del tipo documento
            ins_documento= TipoDocumento.objects.filter(descripcion_tipo_documento= tipo_documento).first()
            nro_documento= dato['nro_documento'].strip()
            nombre= dato['nombre'].strip()
            apellido= dato['apellido'].strip()
            telefono= dato['telefono'].strip()
            email= dato['email'].strip()
            celular= dato['celular'].strip()

            # Intenta actualizar el registro si ya existe, o crea uno nuevo si no existe
            persona, created = Persona.objects.update_or_create(
            documento=nro_documento,
            defaults={'id_tipo_documento': ins_documento, 'documento': nro_documento, 'nombre': nombre, 'apellido': apellido, 'correo': email, 'telefono': telefono, 'celular': celular} 
            )
    except Exception as e:
        print(f'Error al insertar datos de persona: {str(e)}')
        contenido= f'Estimad@: Le informamos que ocurrio un problema con el vuelco de datos de la tabla Persona.  Favor verificar el mismo: {str(e)}.  Atte equipo AcOms.'
        title = 'Error en vuelco de datos AcOMs'
        enviarcorreo(title, contenido)
    else:
        #si todo sale bien llamamos a ejecutar el volcado de Alumno
        volcar_Alumno()
    finally:
        print('Finalizo Persona...')
        
    #respuestas incorrectas lado del cliente
    # elif (199 < response.status_code < 300):  
    #     error_text = response.text
    #     contenido= f'Estimad@: Le informamos que ocurrio un problema con el vuelco de datos de la tabla Persona. ' + error_text +  '.  Atte equipo AcOms.'
    #     title = 'Error en vuelco de datos AcOMs'
    #     enviarcorreo(title, contenido)

    # respuestas incorrectas lado del servidor
    # elif (199 < response.status_code < 300):
    #     error_text = response.text
    #     contenido= f'Estimad@: Le informamos que ocurrio un problema con el vuelco de datos de la tabla Persona. ' + error_text + '.  Atte equipo AcOms.'
    #     title = 'Error en vuelco de datos AcOMs'
    #     enviarcorreo(title, contenido)
    
        
def volcar_Alumno():
   
    # ###########################################
    # ###################Alumno##################
    # ###########################################
    
    print('Iniciando Alumno...')
    # #Preparamos los datos para la solicitud
    # url =  'https://'
    # headers = {
    #     'Authorization': '123456',
    #     'Content-Type': 'application/json',
    #     'Accept': 'application/json'
    # }
    # proxy_servers = { 'http': 'http://10.10.10.1:8080', 'https': 'http://10.10.10.1:8080'}
    
    # # Realizar la solicitud HTTP a un servicio web externo
    # response = requests.get(url, headers=headers, proxies= proxy_servers)
    
    # if (199 < response.status_code < 300):

    # Procesar los datos y volcarlos en la base de datos
    #datos = response.json() 
    #supongamos que los datos nos trae de esta manera
    datos= [
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
    ]
    try:
        for dato in datos:
            documento = dato['documento'].strip()
            # treaemos la instancia de persona
            ins_alumno= Persona.objects.filter(documento= documento).first()
            # Intenta actualizar el registro si ya existe, o crea uno nuevo si no existe
            alumno, created = Alumno.objects.update_or_create(
                id_alumno=ins_alumno,
                defaults={'id_alumno': ins_alumno}  
            )
        
    except Exception as e:
        print(f'Error al insertar datos de alumno: {str(e)}')
        contenido= f'Estimad@: Le informamos que ocurrio un problema con el vuelco de datos de la tabla Alumno.  Favor verificar el mismo: {str(e)}.  Atte equipo AcOms.'
        title = 'Error en vuelco de datos AcOMs'
        enviarcorreo(title, contenido)
    else:
        #si todo sale bien llamamos a ejecutar el volcado de Facultad
        volcar_Facultad()
    finally:
        print('Finalizo Alumno...')
        
    #respuestas incorrectas lado del cliente
    # elif (199 < response.status_code < 300):  
    #     error_text = response.text
    #     contenido= f'Estimad@: Le informamos que ocurrio un problema con el vuelco de datos de la tabla Alumno. ' + error_text +  '. Atte equipo AcOms.'
    #     title = 'Error en vuelco de datos AcOMs'
    #     enviarcorreo(title, contenido)

    # respuestas incorrectas lado del servidor
    # elif (199 < response.status_code < 300):
    #     error_text = response.text
    #     contenido= f'Estimad@: Le informamos que ocurrio un problema con el vuelco de datos de la tabla Alumno. ' + error_text + '.  Atte equipo AcOms.'
    #     title = 'Error en vuelco de datos AcOMs'
    #     enviarcorreo(title, contenido)

def volcar_Facultad():
    # ###########################################
    # ##############Tabla Facultad ##############
    # ###########################################
    
    print('Iniciando Facultad...')
    # #Preparamos los datos para la solicitud
    # url =  'https://'
    # headers = {
    #     'Authorization': '123456',
    #     'Content-Type': 'application/json',
    #     'Accept': 'application/json'
    # }
    # proxy_servers = { 'http': 'http://10.10.10.1:8080', 'https': 'http://10.10.10.1:8080'}
    
    # # Realizar la solicitud HTTP a un servicio web externo
    # response = requests.get(url, headers=headers, proxies= proxy_servers)
    
    # if (199 < response.status_code < 300):

        # Procesar los datos y volcarlos en la base de datos
        #datos = response.json() 
        #supongamos que los datos nos trae de esta manera
    datos= [
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
    ]
    try:
        for dato in datos:
        
            descripcion_facultad = dato['descripcion_facultad'].strip()
            # Intenta actualizar el registro si ya existe, o crea uno nuevo si no existe
            facultad, created = Facultad.objects.update_or_create(
                descripcion_facultad=descripcion_facultad,
                defaults={'descripcion_facultad': descripcion_facultad}  
            )
        
    except Exception as e:
        print(f'Error al insertar datos de facultad: {str(e)}')
        contenido= f'Estimad@: Le informamos que ocurrio un problema con el vuelco de datos de la tabla Facultad.  Favor verificar el mismo: {str(e)}.  Atte equipo AcOms.'
        title = 'Error en vuelco de datos AcOMs'
        enviarcorreo(title, contenido)

    else:
        #si todo sale bien llamamos a ejecutar el volcado de volcar_Departamento
        volcar_Departamento()
    finally:
        print('Finalizo Facultad...')
        
    #respuestas incorrectas lado del cliente
    # elif (199 < response.status_code < 300):  
    #     error_text = response.text
    #     contenido= f'Estimad@: Le informamos que ocurrio un problema con el vuelco de datos de la tabla Facultad. ' + error_text +  '.  Atte equipo AcOms.'
    #     title = 'Error en vuelco de datos AcOMs'
    #     enviarcorreo(title, contenido)

    # respuestas incorrectas lado del servidor
    # elif (199 < response.status_code < 300):
    #     error_text = response.text
    #     contenido= f'Estimad@: Le informamos que ocurrio un problema con el vuelco de datos de la tabla Facultad. ' + error_text + '.  Atte equipo AcOms.'
    #     title = 'Error en vuelco de datos AcOMs'
    #     enviarcorreo(title, contenido)

def volcar_Departamento():
    
    ###########################################
    ##############Tabla Departamento###########
    ###########################################
    print('Iniciando Departamento...')
    #Preparamos los datos para la solicitud
    # url =  'https://'
    # headers = {
    #     'Authorization': '123456',
    #     'Content-Type': 'application/json',
    #     'Accept': 'application/json'
    # }
    # proxy_servers = { 'http': 'http://10.10.10.1:8080', 'https': 'http://10.10.10.1:8080'}
    
    # Realizar la solicitud HTTP a un servicio web externo
    # response = requests.get(url, headers=headers, proxies= proxy_servers)
    
    # if (199 < response.status_code < 300):

        #Procesar los datos y volcarlos en la base de datos
        #datos = response.json() 
    #supongamos que los datos nos trae de esta manera
    datos= [
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
    ]
    
    try:
        for dato in datos:
        
            descripcion_departamento = dato['descripcion_departamento'].strip()
            facultad = dato['facultad'].strip()
            #Traemos la instancia de facultad que coincida con la descripcion
            ins_facultad= Facultad.objects.filter(descripcion_facultad= facultad).first()
            telefono = dato['telefono'].strip()
            # Intenta actualizar el registro si ya existe, o crea uno nuevo si no existe
            departamento, created = Departamento.objects.update_or_create(
                descripcion_departamento=descripcion_departamento, id_facultad= ins_facultad,
                defaults={'descripcion_departamento': descripcion_departamento, 'id_facultad': ins_facultad , 'telefono': telefono}  
            )
    except Exception as e:
        print(f'Error al insertar datos de Departamento: {str(e)}')
        contenido= f'Estimad@: Le informamos que ocurrio un problema con el vuelco de datos de la tabla Departamento.  Favor verificar el mismo: {str(e)}.  Atte equipo AcOms.'
        title = 'Error en vuelco de datos AcOMs'
        enviarcorreo(title, contenido)
        
    else:
        #si todo sale bien llamamos a ejecutar el volcado de volcar_Carrera
        volcar_Carrera()
    finally:
        print('Finalizo Departamento...')
        
    #respuestas incorrectas lado del cliente
    # elif (199 < response.status_code < 300):  
    #     error_text = response.text
    #     contenido= f'Estimad@: Le informamos que ocurrio un problema con el vuelco de datos de la tabla Departamento. ' + error_text +  '. Atte equipo AcOms.'
    #     title = 'Error en vuelco de datos AcOMs'
    #     enviarcorreo(title, contenido)

    # respuestas incorrectas lado del servidor
    # elif (199 < response.status_code < 300):
    #     error_text = response.text
    #     contenido= f'Estimad@: Le informamos que ocurrio un problema con el vuelco de datos de la tabla Departamento. ' + error_text + '.  Atte equipo AcOms.'
    #     title = 'Error en vuelco de datos AcOMs'
    #     enviarcorreo(title, contenido)
        
        
def volcar_Carrera():   
    
    # ###########################################
    # ################Tabla Carrera##############
    # ###########################################
    
    print('Iniciando Carrera...')
    #Preparamos los datos para la solicitud
    # url =  'https://'
    # headers = {
    #     'Authorization': '123456',
    #     'Content-Type': 'application/json',
    #     'Accept': 'application/json'
    # }
    # proxy_servers = { 'http': 'http://10.10.10.1:8080', 'https': 'http://10.10.10.1:8080'}

    # Realizar la solicitud HTTP a un servicio web externo
    # response = requests.get(url, headers=headers, proxies= proxy_servers)

    # if (199 < response.status_code < 300):

        # Procesar los datos y volcarlos en la base de datos
        #datos = response.json() 
    #supongamos que los datos nos trae de esta manera
    datos= [
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
    ]
    try:
        for dato in datos:
            
            descripcion_carrera = dato['descripcion_carrera'].strip()
            facultad= dato['facultad'].strip()
            #Traemos la instancia de facultad que coincida con la descripcion
            ins_facultad= Facultad.objects.filter(descripcion_facultad= facultad).first()
        
            # Intenta actualizar el registro si ya existe, o crea uno nuevo si no existe
            facultad, created = Carrera.objects.update_or_create(
                descripcion_carrera=descripcion_carrera, id_facultad= ins_facultad,
                defaults={'descripcion_carrera': descripcion_carrera, 'id_facultad': ins_facultad}  
            )
        
    except Exception as e:
        print(f'Error al insertar datos de Carrera: {str(e)}')
        contenido= f'Estimad@: Le informamos que ocurrio un problema con el vuelco de datos de la tabla Carrera.  Favor verificar el mismo: {str(e)}.  Atte equipo AcOms.'
        title = 'Error en vuelco de datos AcOMs'
        enviarcorreo(title, contenido)
    else:
        #si todo sale bien llamamos a ejecutar el volcado de CarreraAlumno
        volcar_CarreraAlumno()
    finally:
        print('Finalizo Carrera...')
        
    #respuestas incorrectas lado del cliente
    # elif (199 < response.status_code < 300):  
    #     error_text = response.text
    #     contenido= f'Estimad@: Le informamos que ocurrio un problema con el vuelco de datos de la tabla Carrera. ' + error_text +  '.  Atte equipo AcOms.'
    #     title = 'Error en vuelco de datos AcOMs'
    #     enviarcorreo(title, contenido)

    # respuestas incorrectas lado del servidor
    # elif (199 < response.status_code < 300):
    #     error_text = response.text
    #     contenido= f'Estimad@: Le informamos que ocurrio un problema con el vuelco de datos de la tabla Carrera. ' + error_text + '.  Atte equipo AcOms.'
    #     title = 'Error en vuelco de datos AcOMs'
    #     enviarcorreo(title, contenido)
            

def volcar_CarreraAlumno():   
    
    # ###########################################
    # ############Tabla CarreraAlumno############
    # ###########################################
    
    print('Iniciando Carrera Alumno...')
    #Preparamos los datos para la solicitud
    # url =  'https://'
    # headers = {
    #     'Authorization': '123456',
    #     'Content-Type': 'application/json',
    #     'Accept': 'application/json'
    # }
    # proxy_servers = { 'http': 'http://10.10.10.1:8080', 'https': 'http://10.10.10.1:8080'}

    # # Realizar la solicitud HTTP a un servicio web externo
    # response = requests.get(url, headers=headers, proxies= proxy_servers)

    # if (199 < response.status_code < 300):

        # Procesar los datos y volcarlos en la base de datos
        #datos = response.json() 
    #supongamos que los datos nos trae de esta manera
    datos= [
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
    ]
    
    try:
        for dato in datos:
        
            descripcion_carrera = dato['descripcion_carrera'].strip()
            documento_alumno= dato['documento_alumno'].strip()
            #Traemos la instancia de Persona que coincida con el nro de documento
            ins_alumno= Persona.objects.filter(documento= documento_alumno).first()
            #Traemos la instancia de carrera que coincida con la descripción
            ins_carrera= Carrera.objects.filter(descripcion_carrera= descripcion_carrera).first()
        
            # Intenta actualizar el registro si ya existe, o crea uno nuevo si no existe
            carrera_alumno, created = CarreraAlumno.objects.update_or_create(
                id_alumno=ins_alumno, id_carrera= ins_carrera,
                defaults={'id_alumno': ins_alumno, 'id_carrera': ins_carrera}  
            )

    except Exception as e:
        print(f'Error al insertar datos de CarreraAlumno: {str(e)}')
        contenido= f'Estimad@: Le informamos que ocurrio un problema con el vuelco de datos de la tabla Carrera Alumno.  Favor verificar el mismo: {str(e)}.  Atte equipo AcOms.'
        title = 'Error en vuelco de datos AcOMs'
        enviarcorreo(title, contenido)
        
    else:
        #si todo sale bien llamamos a ejecutar el volcado de volcar_Materia
        volcar_Materia()
    finally:
        print('Finalizo Carrera Alumno...')
        
    #respuestas incorrectas lado del cliente
    # elif (199 < response.status_code < 300):  
    #     error_text = response.text
    #     contenido= f'Estimad@: Le informamos que ocurrio un problema con el vuelco de datos de la tabla Carrera Alumno. ' + error_text +  '.  Atte equipo AcOms.'
    #     title = 'Error en vuelco de datos AcOMs'
    #     enviarcorreo(title, contenido)

    # respuestas incorrectas lado del servidor
    # elif (199 < response.status_code < 300):
    #     error_text = response.text
    #     contenido= f'Estimad@: Le informamos que ocurrio un problema con el vuelco de datos de la tabla Carrera Alumno. ' + error_text + '.  Atte equipo AcOms.'
    #     title = 'Error en vuelco de datos AcOMs'
    #     enviarcorreo(title, contenido)
    

def volcar_Materia():
    
    # ###########################################
    # ###############Tabla Materia###############
    # ###########################################

    print('Iniciando Materia...')
    # #Preparamos los datos para la solicitud
    # url =  'https://'
    # headers = {
    #     'Authorization': '123456',
    #     'Content-Type': 'application/json',
    #     'Accept': 'application/json'
    # }
    # proxy_servers = { 'http': 'http://10.10.10.1:8080', 'https': 'http://10.10.10.1:8080'}

    # Realizar la solicitud HTTP a un servicio web externo
    # response = requests.get(url, headers=headers, proxies= proxy_servers)

    # if (199 < response.status_code < 300):

        #Procesar los datos y volcarlos en la base de datos
        #datos = response.json() 
    #supongamos que los datos nos trae de esta manera
    datos= [
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
    ]
    try:
        for dato in datos:
        
            descripcion_materia = dato['descripcion_materia'].strip()
            departamento= dato['departamento'].strip()
            #Traemos la instancia de departamento que coincida con la descripción
            ins_departamento= Departamento.objects.filter(descripcion_departamento= departamento).first()
        
            # Intenta actualizar el registro si ya existe, o crea uno nuevo si no existe
            materia, created = Materia.objects.update_or_create(
                descripcion_materia=descripcion_materia, id_departamento= ins_departamento,
                defaults={'descripcion_materia': descripcion_materia, 'id_departamento': ins_departamento}  
            )
    
    except Exception as e:
        print(f'Error al insertar datos de Materia: {str(e)}')
        contenido= f'Estimad@: Le informamos que ocurrio un problema con el vuelco de datos de la tabla Materia.  Favor verificar el mismo: {str(e)}.  Atte equipo AcOms.'
        title = 'Error en vuelco de datos AcOMs'
        enviarcorreo(title, contenido)
    
    else:
        #si todo sale bien llamamos a ejecutar el volcado de volcar_MateriaCarrera
        volcar_MateriaCarrera()
    finally:
        print('Finalizo Materia...')
        
    #respuestas incorrectas lado del cliente
    # elif (199 < response.status_code < 300):  
    #     error_text = response.text
    #     contenido= f'Estimad@: Le informamos que ocurrio un problema con el vuelco de datos de la tabla Materia. ' + error_text +  '.  Atte equipo AcOms.'
    #     title = 'Error en vuelco de datos AcOMs'
    #     enviarcorreo(title, contenido)

    # respuestas incorrectas lado del servidor
    # elif (199 < response.status_code < 300):
    #     error_text = response.text
    #     contenido= f'Estimad@: Le informamos que ocurrio un problema con el vuelco de datos de la tabla Materia. ' + error_text + '.   Atte equipo AcOms.'
    #     title = 'Error en vuelco de datos AcOMs'
    #     enviarcorreo(title, contenido)

        
def volcar_MateriaCarrera():
        
    ###########################################
    ##########Tabla MateriaCarrera#############
    ###########################################

    print('Iniciando Materia Carrera ...')
    #Preparamos los datos para la solicitud
    # url =  'https://'
    # headers = {
    #     'Authorization': '123456',
    #     'Content-Type': 'application/json',
    #     'Accept': 'application/json'
    # }
    # proxy_servers = { 'http': 'http://10.10.10.1:8080', 'https': 'http://10.10.10.1:8080'}

    # Realizar la solicitud HTTP a un servicio web externo
    # response = requests.get(url, headers=headers, proxies= proxy_servers)

    # if (199 < response.status_code < 300):

        #Procesar los datos y volcarlos en la base de datos
        #datos = response.json() 
    #supongamos que los datos nos trae de esta manera
    datos= [
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
    ]
    try:
        for dato in datos:
            descripcion_materia = dato['descripcion_materia'].strip()
            carrera= dato['carrera'].strip()
            #Traemos la instancia de Materia que coincida con la descripción
            ins_materia= Materia.objects.filter(descripcion_materia= descripcion_materia).first()
            #Traemos la instancia de Carrera que coincida con la descripción
            ins_carrera= Carrera.objects.filter(descripcion_carrera= carrera).first()
        
            # Intenta actualizar el registro si ya existe, o crea uno nuevo si no existe
            materiacarrera, created = MateriaCarrera.objects.update_or_create(
                id_carrera= ins_carrera, id_materia= ins_materia, 
                defaults={'id_carrera': ins_carrera, 'id_materia': ins_materia}  
            )
        
    except Exception as e:
        print(f'Error al insertar datos de MateriaCarrera: {str(e)}')
        contenido= f'Estimad@: Le informamos que ocurrio un problema con el vuelco de datos de la tabla MateriaCarrera.  Favor verificar el mismo: {str(e)}.  Atte equipo AcOms.'
        title = 'Error en vuelco de datos AcOMs'
        enviarcorreo(title, contenido)
    else:
        contenido= f'Estimad@: Le informamos que ha finalizado con exito el proceso de insersion/actualizacion de datos academicos. Atte equipo AcOms.'
        title = 'Finalizacion de datos AcOMs'
        enviarcorreo(title, contenido)
        
    finally:
        print('Finalizo Materia Carrera...')
        
    print('Finalizo la tarea...')
        
    #respuestas incorrectas lado del cliente
    # elif (199 < response.status_code < 300):  
    #     error_text = response.text
    #     contenido= f'Estimad@: Le informamos que ocurrio un problema con el vuelco de datos de la tabla Materia Carrera. ' + error_text +  '. Atte equipo AcOms.'
    #     title = 'Error en vuelco de datos AcOMs'
    #     enviarcorreo(title, contenido)

    # respuestas incorrectas lado del servidor
    # elif (199 < response.status_code < 300):
    #     error_text = response.text
    #     contenido= f'Estimad@: Le informamos que ocurrio un problema con el vuelco de datos de la tabla Materia Carrera. ' + error_text + '.  Atte equipo AcOms.'
    #     title = 'Error en vuelco de datos AcOMs'
    #     enviarcorreo(title, contenido)

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def enviarcorreo(asunto, contenido): 
    #destinatario= 'hcorrea@uaa.edu.py '
    destinatario= 'karendreammoon@gmail.com '
    # Configura tus credenciales de Outlook
    sender_email = 'kaliuzzi@uaa.edu.py'
    sender_password = 'Yad92906'

    # Configura el servidor SMTP de Outlook
    smtp_server = 'smtp-mail.outlook.com'
    smtp_port = 587  # Puerto de Outlook para TLS (587)

    # Crea un objeto SMTP
    server = smtplib.SMTP(smtp_server, smtp_port)

    # Inicia la conexión TLS (segura)
    server.starttls()

    # Inicia sesión en tu cuenta de Gmail
    server.login(sender_email, sender_password)

    # Crea el mensaje de correo
    subject = asunto
    body = contenido
    recipient_email = destinatario

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Envía el correo
        server.sendmail(sender_email, recipient_email, msg.as_string())
        # Cierra la conexión SMTP
        server.quit()
        print('Correo enviado con éxito')
    except Exception as e:
        print(f"Se ha producido un error: {e}")
        