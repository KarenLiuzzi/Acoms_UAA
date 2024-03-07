INSERT INTO public.accounts_tipodocumento (descripcion_tipo_documento) VALUES ('CI');
INSERT INTO public.accounts_persona (nombre, apellido, documento, correo, telefono, celular, id_tipo_documento_id) VALUES ('Hugo', 'Correa', '4978990', '', '', '', 1);
INSERT INTO public.accounts_persona (nombre, apellido, documento, correo, telefono, celular, id_tipo_documento_id) VALUES ('Maria', 'Aguero', '147258', '', '', '', 1);
INSERT INTO public.accounts_persona (nombre, apellido, documento, correo, telefono, celular, id_tipo_documento_id) VALUES ('Karen', 'Liuzzi', '6109876', '', '', '', 1);
INSERT INTO public.accounts_persona (nombre, apellido, documento, correo, telefono, celular, id_tipo_documento_id) VALUES ('Blanca', 'Baez', '789654', '', '', '', 1);
INSERT INTO public.accounts_persona (nombre, apellido, documento, correo, telefono, celular, id_tipo_documento_id) VALUES ('Ricardo', 'De Castro', '3040653', '', '', '', 1);
INSERT INTO public.accounts_persona (nombre, apellido, documento, correo, telefono, celular, id_tipo_documento_id) VALUES ('Sebastian', 'Grillo', '6040302', '', '', '', 1);
INSERT INTO public.calendarapp_dia (descripcion_dia) VALUES ('Lunes');
INSERT INTO public.calendarapp_dia (descripcion_dia) VALUES ('Martes');
INSERT INTO public.calendarapp_dia (descripcion_dia) VALUES ('Miércoles');
INSERT INTO public.calendarapp_dia (descripcion_dia) VALUES ('Jueves');
INSERT INTO public.calendarapp_dia (descripcion_dia) VALUES ('Viernes');
INSERT INTO public.calendarapp_dia (descripcion_dia) VALUES ('Sábado');
INSERT INTO public.calendarapp_tipotarea (descripcion_tipo_tarea) VALUES ('Seguimiento');
INSERT INTO public.calendarapp_tipotarea (descripcion_tipo_tarea) VALUES ('Llamada');
INSERT INTO public.calendarapp_tipotarea (descripcion_tipo_tarea) VALUES ('Gestión');
INSERT INTO public.calendarapp_tipotarea (descripcion_tipo_tarea) VALUES ('Reunión');
INSERT INTO public.calendarapp_unidadmedida (descripcion_unidad_medida) VALUES ('Minutos');
INSERT INTO public.calendarapp_parametro (descripcion_parametro, valor, es_orientacion_academica, es_tutoria, id_unidad_medida_id) VALUES ('Rango de minutos para orientación académica', 15, true, false, 1);
INSERT INTO public.calendarapp_parametro (descripcion_parametro, valor, es_orientacion_academica, es_tutoria, id_unidad_medida_id) VALUES ('Rango de minutos para tutoria', 30, false, true, 1);
INSERT INTO public.calendarapp_tipoorientacionacademica (descripcion_tipo_orientacion_academica) VALUES ('Solicitud');
INSERT INTO public.calendarapp_tipoorientacionacademica (descripcion_tipo_orientacion_academica) VALUES ('Consulta');
INSERT INTO public.calendarapp_tipoorientacionacademica (descripcion_tipo_orientacion_academica) VALUES ('Orientación');
INSERT INTO public.calendarapp_motivo (descripcion_motivo, id_tipo_orientacion_academica_id) VALUES ('Malla curricular', 1);
INSERT INTO public.calendarapp_motivo (descripcion_motivo, id_tipo_orientacion_academica_id) VALUES ('Procedimiento Trabajo de Grado Licenciatura', 3);
INSERT INTO public.calendarapp_motivo (descripcion_motivo, id_tipo_orientacion_academica_id) VALUES ('Procedimiento Trabajo de Grado Ingeniería', 3);
INSERT INTO public.calendarapp_motivo (descripcion_motivo, id_tipo_orientacion_academica_id) VALUES ('Aprobación de cambio de Curso', 1);
INSERT INTO public.calendarapp_motivo (descripcion_motivo, id_tipo_orientacion_academica_id) VALUES ('Estado académico', 2);
INSERT INTO public.calendarapp_motivo (descripcion_motivo, id_tipo_orientacion_academica_id) VALUES ('Horario de Profesor', 2);
INSERT INTO public.calendarapp_estadotarea (descripcion_estado_tarea) VALUES ('Iniciada');
INSERT INTO public.calendarapp_estadotarea (descripcion_estado_tarea) VALUES ('Cancelada');
INSERT INTO public.calendarapp_estadotarea (descripcion_estado_tarea) VALUES ('Finalizada');
INSERT INTO public.calendarapp_estadotarea (descripcion_estado_tarea) VALUES ('Pendiente');
INSERT INTO public.calendarapp_estadoactividadacademica (descripcion_estado_actividad_academica) VALUES ('Iniciada');
INSERT INTO public.calendarapp_estadoactividadacademica (descripcion_estado_actividad_academica) VALUES ('Confirmada');
INSERT INTO public.calendarapp_estadoactividadacademica (descripcion_estado_actividad_academica) VALUES ('Finalizada');
INSERT INTO public.calendarapp_estadoactividadacademica (descripcion_estado_actividad_academica) VALUES ('Cancelada');
INSERT INTO public.calendarapp_estadoactividadacademica (descripcion_estado_actividad_academica) VALUES ('Rechazada');
INSERT INTO public.calendarapp_estadoactividadacademica (descripcion_estado_actividad_academica) VALUES ('Pendiente');
INSERT INTO public.calendarapp_semestre (descripcion_semestre) VALUES ('Verano');
INSERT INTO public.calendarapp_semestre (descripcion_semestre) VALUES ('Otoño');
INSERT INTO public.calendarapp_semestre (descripcion_semestre) VALUES ('Primavera');
INSERT INTO public.calendarapp_convocatoria (anho, fecha_inicio, fecha_fin, id_semestre_id) VALUES (2023, '2023-12-28', '2024-01-31', 1);
INSERT INTO public.calendarapp_convocatoria (anho, fecha_inicio, fecha_fin, id_semestre_id) VALUES (2024, '2024-02-01', '2024-06-30', 2);
INSERT INTO public.calendarapp_tipotutoria (descripcion_tipo_tutoria) VALUES ('Trabajo de Grado');
INSERT INTO public.calendarapp_tipotutoria (descripcion_tipo_tutoria) VALUES ('Académica');
INSERT INTO public.accounts_user (password, last_login, is_superuser, documento, lector, email, is_staff, is_active, date_joined, last_updated, id_persona_id) VALUES ('pbkdf2_sha256$260000$GB8o1UBcjAW58DXdeJCdkj$pQkYb/zy0yg1EJunVyKUqx+4HdvMdp+8GKppaOu/yEI=', '2024-01-29 18:51:21.277463-03', true, '4978990', true, 'prueba@test.com', true, true, '2023-12-28 07:17:50.385747-03', '2024-01-24 11:45:19.70612-03', 1);
INSERT INTO public.accounts_user (password, last_login, is_superuser, documento, lector, email, is_staff, is_active, date_joined, last_updated, id_persona_id) VALUES ('pbkdf2_sha256$260000$jY5w8viuxNTDNXohgYaatD$yNEKXoUsznOgj9l5yV25VjlVnBT4MmiHgV5yAeacRLo=', '2024-01-30 11:08:13.535584-03', false, '147258', true, 'karendreammoon@gmail.com', false, true, '2023-12-28 10:25:36.105251-03', '2023-12-28 10:25:36.105251-03', 2);
INSERT INTO public.accounts_user (password, last_login, is_superuser, documento, lector, email, is_staff, is_active, date_joined, last_updated, id_persona_id) VALUES ('pbkdf2_sha256$260000$wKNjZFm8qUPz5TgeQ3azwp$eryXF4yWaubHD2ql9bCfs0mL7EX6Itu97sUENip685M=', '2024-01-30 13:09:20.436121-03', false, '789654', true, 'blanca.baez@test.com', true, true, '2023-12-28 10:26:39.32369-03', '2024-01-24 11:44:31.706973-03', 4);
INSERT INTO public.accounts_user (password, last_login, is_superuser, documento, lector, email, is_staff, is_active, date_joined, last_updated, id_persona_id) VALUES ('pbkdf2_sha256$260000$rOVPBt7QUEVSYVsoJkQOCM$ziU656iuT4VzdglVcKCBrnP/YGeoAaWPLWpKr0veXmA=', '2024-01-30 17:45:23.270654-03', false, '6109876', true, 'karen.liuzzi@test.com', false, true, '2023-12-28 10:25:59.80392-03', '2023-12-28 10:25:59.80392-03', 3);
INSERT INTO public.accounts_user (password, last_login, is_superuser, documento, lector, email, is_staff, is_active, date_joined, last_updated, id_persona_id) VALUES ('pbkdf2_sha256$260000$HZo0mNhD4VKJeWBLp2ZFEP$kQhINNb85o15INMhJjIKnffbA/JCd22veUk+VZaXvQg=', '2024-01-25 11:01:22.62687-03', false, '3040653', true, 'ricardocastro@test.com', true, true, '2023-12-28 10:26:59.045553-03', '2024-01-24 11:44:58.544741-03', 5);
INSERT INTO public.accounts_facultad (descripcion_facultad) VALUES ('Facultad de Ciencias y Tecnología');
INSERT INTO public.accounts_departamento (descripcion_departamento, telefono, id_facultad_id) VALUES ('Departamento de E-learning', '123456', 1);
INSERT INTO public.accounts_departamento (descripcion_departamento, telefono, id_facultad_id) VALUES ('Informática', '78946', 1);
INSERT INTO public.accounts_departamento (descripcion_departamento, telefono, id_facultad_id) VALUES ('Ciencias Exactas', '654987', 1);
INSERT INTO public.accounts_funcionariodocente (id_funcionario_docente_id, id_departamento_id, id_facultad_id) VALUES (1, NULL, 1);
INSERT INTO public.accounts_funcionariodocente (id_funcionario_docente_id, id_departamento_id, id_facultad_id) VALUES (4, 2, NULL);
INSERT INTO public.accounts_funcionariodocente (id_funcionario_docente_id, id_departamento_id, id_facultad_id) VALUES (5, 1, NULL);
INSERT INTO public.accounts_funcionariodocente (id_funcionario_docente_id, id_departamento_id, id_facultad_id) VALUES (6, 1, NULL);
INSERT INTO public.accounts_alumno (id_alumno_id) VALUES (3);
INSERT INTO public.accounts_alumno (id_alumno_id) VALUES (2);
INSERT INTO public.calendarapp_horariosemestral (hora_inicio, hora_fin, id_convocatoria_id, id_dia_id, id_funcionario_docente_id) VALUES ('19:00:00', '21:00:00', 1, 1, 1);
INSERT INTO public.calendarapp_horariosemestral (hora_inicio, hora_fin, id_convocatoria_id, id_dia_id, id_funcionario_docente_id) VALUES ('18:00:00', '20:00:00', 1, 2, 1);
INSERT INTO public.calendarapp_horariosemestral (hora_inicio, hora_fin, id_convocatoria_id, id_dia_id, id_funcionario_docente_id) VALUES ('18:30:00', '20:30:00', 1, 4, 1);
INSERT INTO public.calendarapp_horariosemestral (hora_inicio, hora_fin, id_convocatoria_id, id_dia_id, id_funcionario_docente_id) VALUES ('19:00:00', '21:00:00', 1, 1, 5);
INSERT INTO public.calendarapp_horariosemestral (hora_inicio, hora_fin, id_convocatoria_id, id_dia_id, id_funcionario_docente_id) VALUES ('18:00:00', '21:00:00', 1, 3, 5);
INSERT INTO public.calendarapp_horariosemestral (hora_inicio, hora_fin, id_convocatoria_id, id_dia_id, id_funcionario_docente_id) VALUES ('18:30:00', '20:30:00', 1, 5, 5);
INSERT INTO public.calendarapp_horariosemestral (hora_inicio, hora_fin, id_convocatoria_id, id_dia_id, id_funcionario_docente_id) VALUES ('15:00:00', '18:00:00', 1, 1, 4);
INSERT INTO public.calendarapp_horariosemestral (hora_inicio, hora_fin, id_convocatoria_id, id_dia_id, id_funcionario_docente_id) VALUES ('09:00:00', '12:00:00', 1, 6, 4);
INSERT INTO public.calendarapp_horariosemestral (hora_inicio, hora_fin, id_convocatoria_id, id_dia_id, id_funcionario_docente_id) VALUES ('19:00:00', '21:00:00', 1, 4, 4);
INSERT INTO public.calendarapp_horariosemestral (hora_inicio, hora_fin, id_convocatoria_id, id_dia_id, id_funcionario_docente_id) VALUES ('19:00:00', '21:00:00', 2, 1, 1);
INSERT INTO public.calendarapp_horariosemestral (hora_inicio, hora_fin, id_convocatoria_id, id_dia_id, id_funcionario_docente_id) VALUES ('18:00:00', '20:00:00', 2, 2, 1);
INSERT INTO public.calendarapp_horariosemestral (hora_inicio, hora_fin, id_convocatoria_id, id_dia_id, id_funcionario_docente_id) VALUES ('18:30:00', '20:30:00', 2, 4, 1);
INSERT INTO public.calendarapp_horariosemestral (hora_inicio, hora_fin, id_convocatoria_id, id_dia_id, id_funcionario_docente_id) VALUES ('19:00:00', '21:00:00', 2, 1, 5);
INSERT INTO public.calendarapp_horariosemestral (hora_inicio, hora_fin, id_convocatoria_id, id_dia_id, id_funcionario_docente_id) VALUES ('18:00:00', '21:00:00', 2, 3, 5);
INSERT INTO public.calendarapp_horariosemestral (hora_inicio, hora_fin, id_convocatoria_id, id_dia_id, id_funcionario_docente_id) VALUES ('18:30:00', '20:30:00', 2, 5, 5);
INSERT INTO public.calendarapp_horariosemestral (hora_inicio, hora_fin, id_convocatoria_id, id_dia_id, id_funcionario_docente_id) VALUES ('15:00:00', '18:00:00', 2, 1, 4);
INSERT INTO public.calendarapp_horariosemestral (hora_inicio, hora_fin, id_convocatoria_id, id_dia_id, id_funcionario_docente_id) VALUES ('09:00:00', '12:00:00', 2, 6, 4);
INSERT INTO public.calendarapp_horariosemestral (hora_inicio, hora_fin, id_convocatoria_id, id_dia_id, id_funcionario_docente_id) VALUES ('19:00:00', '21:00:00', 2, 4, 4);
INSERT INTO public.accounts_materia (descripcion_materia, id_departamento_id) VALUES ('INTRODUCCIÓN A LAS TECNOLOGÍAS DE INFORMACIÓN Y LA COMUNICACIÓN', 1);
INSERT INTO public.accounts_materia (descripcion_materia, id_departamento_id) VALUES ('INTRODUCCIÓN A LA INFORMÁTICA', 2);
INSERT INTO public.accounts_materia (descripcion_materia, id_departamento_id) VALUES ('ÁLGEBRA', 3);
INSERT INTO public.accounts_materia (descripcion_materia, id_departamento_id) VALUES ('INTRODUCCIÓN AL DISEÑO Y CONSTRUCCIÓN DE PÁGINAS WEB', 2);
INSERT INTO public.accounts_materia (descripcion_materia, id_departamento_id) VALUES ('LÓGICA DE PROGRAMACIÓN DE COMPUTADORAS I', 2);
INSERT INTO public.accounts_materia (descripcion_materia, id_departamento_id) VALUES ('TRABAJO DE GRADO PARA INGENIERÍA EN INFORMÁTICA ÉNFASIS CIENCIAS DE LA COMPUTACIÓN', 2);
INSERT INTO public.accounts_carrera (descripcion_carrera, id_facultad_id) VALUES ('Ingeniería en Informática Énfasis en: Ciencias de la Computación', 1);
INSERT INTO public.accounts_carrera (descripcion_carrera, id_facultad_id) VALUES ('Licenciatura en Ciencias Informáticas Énfasis en: Bases de Datos', 1);
INSERT INTO public.accounts_carreraalumno (id_alumno_id, id_carrera_id) VALUES (2, 1);
INSERT INTO public.accounts_carreraalumno (id_alumno_id, id_carrera_id) VALUES (3, 2);
INSERT INTO public.accounts_materiacarrera (id_carrera_id, id_materia_id) VALUES (1, 1);
INSERT INTO public.accounts_materiacarrera (id_carrera_id, id_materia_id) VALUES (2, 1);
INSERT INTO public.accounts_materiacarrera (id_carrera_id, id_materia_id) VALUES (1, 2);
INSERT INTO public.accounts_materiacarrera (id_carrera_id, id_materia_id) VALUES (2, 2);
INSERT INTO public.accounts_materiacarrera (id_carrera_id, id_materia_id) VALUES (1, 3);
INSERT INTO public.accounts_materiacarrera (id_carrera_id, id_materia_id) VALUES (2, 4);
INSERT INTO public.accounts_materiacarrera (id_carrera_id, id_materia_id) VALUES (2, 3);
INSERT INTO public.accounts_materiacarrera (id_carrera_id, id_materia_id) VALUES (1, 4);
INSERT INTO public.accounts_materiacarrera (id_carrera_id, id_materia_id) VALUES (1, 5);
INSERT INTO public.accounts_materiacarrera (id_carrera_id, id_materia_id) VALUES (2, 5);
INSERT INTO public.accounts_materiacarrera (id_carrera_id, id_materia_id) VALUES (1, 6);
INSERT INTO public.auth_group (name) VALUES ('Funcionario/Docente');
INSERT INTO public.accounts_user_groups (user_id, group_id) VALUES (5, 1);
INSERT INTO public.accounts_user_groups (user_id, group_id) VALUES (3, 1);
INSERT INTO public.accounts_user_groups (user_id, group_id) VALUES (1, 1);
INSERT INTO public.accounts_user_materia_func_doc (user_id, materia_id) VALUES (5, 4);
INSERT INTO public.accounts_user_materia_func_doc (user_id, materia_id) VALUES (5, 6);
INSERT INTO public.accounts_user_materia_func_doc (user_id, materia_id) VALUES (3, 1);
INSERT INTO public.accounts_user_materia_func_doc (user_id, materia_id) VALUES (3, 2);
INSERT INTO public.accounts_user_materia_func_doc (user_id, materia_id) VALUES (3, 5);
INSERT INTO public.accounts_user_materia_func_doc (user_id, materia_id) VALUES (1, 5);
INSERT INTO public.accounts_user_materia_func_doc (user_id, materia_id) VALUES (1, 6);

INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,1) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,2) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,3) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,4) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,8) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,12) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,13) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,14) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,15) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,16) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,17) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,18) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,19) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,20) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,21) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,22) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,23) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,24) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,25) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,26) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,27) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,28) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,29) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,30) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,31) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,32) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,33) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,34) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,35) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,36) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,37) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,38) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,39) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,40) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,41) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,42) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,43) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,44) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,45) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,46) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,47) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,48) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,49) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,50) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,51) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,52) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,53) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,54) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,55) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,56) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,57) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,58) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,59) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,60) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,61) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,62) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,63) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,64) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,65) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,66) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,67) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,68) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,69) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,70) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,71) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,72) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,73) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,74) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,75) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,76) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,77) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,78) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,79) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,80) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,81) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,82) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,83) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,84) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,85) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,86) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,87) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,88) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,89) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,90) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,91) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,92) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,93) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,94) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,95) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,96) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,97) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,98) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,99) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,100) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,101) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,102) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,103) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,104) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,105) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,106) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,107) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,108) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,109) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,110) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,111) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,112) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,113) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,114) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,115) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,116) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,117) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,118) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,119) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,120) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,121) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,122) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,123) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,124) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,125) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,126) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,127) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,128) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,129) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,130) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,131) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,132) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,133) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,134) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,135) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,139) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,140) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,141) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,142) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,143) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,147) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,148) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,149) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,150) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,151) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,152) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,153) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,154) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,155) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,156) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,157) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,158) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,159) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,160) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,161) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,162) ;
INSERT INTO public.auth_group_permissions (group_id, permission_id) VALUES (1 ,163) ;

--cita Tutoria

-- cita tutoria finalizada, karen, blanca

INSERT INTO public.calendarapp_event (datetime_inicio_estimado, datetime_fin_estimado, datetime_inicio_real, datetime_fin_real, datetime_registro, 
observacion, nro_curso, id_convocatoria_id, id_departamento_id, id_estado_actividad_academica_id, id_facultad_id, 
id_funcionario_docente_encargado_id, id_materia_id, id_persona_alta_id, id_persona_solicitante_id, id_persona_ultima_modificacion_id) 
VALUES ('2024-03-04 20:30:00-03', '2024-03-04 21:00:00-03', '2024-03-05 20:30:00-03', '2024-03-05 21:00:00-03', '2024-03-05 14:16:19.716404-03', 
'Se reforzo el ultimo tema dado en la clase', '1234', 2, 1, 3, 1, 4, 1, 3, 3, 4);

INSERT INTO public.calendarapp_cita (id_cita_id, es_tutoria, es_orientacion_academica, es_notificable, motivo, motivo_cancelacion, motivo_rechazo, id_parametro_id) 
VALUES (1, true, false, true, 'Reforzar ultima clase', NULL, NULL, 2);

INSERT INTO public.calendarapp_tutoria (id_tutoria_id, nombre_trabajo, id_cita_id, id_tipo_tutoria_id, motivo_cancelacion) VALUES (1, '', 1, 2, NULL);

INSERT INTO public.calendarapp_detalleactividadacademica ( id_actividad_academica_id, id_participante_id) VALUES ( 1, 2);

INSERT INTO public.calendarapp_tarea (datetime_inicio_estimado, datetime_inicio_real, datetime_vencimiento, datetime_alta, datetime_finalizacion, 
datetime_ultima_modificacion, observacion, es_notificable, id_estado_tarea_id, id_persona_alta_id, id_persona_finalizacion_id, id_persona_responsable_id, 
id_persona_ultima_modificacion_id, id_tipo_tarea_id, id_orientacion_academica_id, id_tutoria_id) 
VALUES ('2024-03-05 14:18:00-03', NULL, '2024-03-04 14:18:00-03', '2024-03-05 14:19:19.379231-03', NULL, 
'2024-03-05 14:19:19.379604-03', 'Realizar tareas adicionales', true, 4, 4, NULL, 3, 4, 3, NULL, 1);

INSERT INTO public.calendarapp_tarea (datetime_inicio_estimado, datetime_inicio_real, datetime_vencimiento, datetime_alta, datetime_finalizacion, 
datetime_ultima_modificacion, observacion, es_notificable, id_estado_tarea_id, id_persona_alta_id, id_persona_finalizacion_id, id_persona_responsable_id, 
id_persona_ultima_modificacion_id, id_tipo_tarea_id, id_orientacion_academica_id, id_tutoria_id) 
VALUES ('2024-03-05 14:18:00-03', NULL, '2024-03-06 14:18:00-03', '2024-03-05 14:19:19.39329-03', NULL, 
'2024-03-05 14:19:19.393713-03', 'Seguimiento a la tarea solicitada', true, 4, 4, NULL, 4, 4, 1, NULL, 1);

INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'cita_tutoria', 1, 4, 'Nueva solicitud de cita', false, true, false, '2024-02-25 13:16:19.736013-03', 34, 3);

INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'cita_tutoria', 1, 3, 'Cita de Tutoria confirmada.', false, true, false, '2024-02-25 13:19:34.920669-03', 34, 4);

INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'tarea_cita_tutoria', 1, 3, 'Te asignaron una tarea en una cita de tutoría', false, true, false, '2024-02-25 13:19:40.401062-03', 34, 4);

-- cita orientacion finalizada con tareas, hugo, karen

INSERT INTO public.calendarapp_event (datetime_inicio_estimado, datetime_fin_estimado, datetime_inicio_real, datetime_fin_real, datetime_registro, 
observacion, nro_curso, id_convocatoria_id, id_departamento_id, id_estado_actividad_academica_id, id_facultad_id, 
id_funcionario_docente_encargado_id, id_materia_id, id_persona_alta_id, id_persona_solicitante_id, id_persona_ultima_modificacion_id) 
VALUES ('2024-03-08 20:15:00-03', '2024-03-08 20:30:00-03', '2024-03-05 20:15:00-03', '2024-03-05 20:30:00-03', '2024-03-05 14:16:54.842648-03', 
'Se dio orientacion sobre el procedimiento del trabajo final', '1596', 2, 2, 3, 1, 1, 6, 3, 3, 1);

INSERT INTO public.calendarapp_cita (id_cita_id, es_tutoria, es_orientacion_academica, es_notificable, motivo, motivo_cancelacion, motivo_rechazo, id_parametro_id) 
VALUES (2, false, true, true, 'Trabajo Final de grado', NULL, NULL, 1);

INSERT INTO public.calendarapp_orientacionacademica (id_orientacion_academica_id, id_cita_id, id_motivo_id, id_tipo_orientacion_academica_id, motivo_cancelacion) 
VALUES (2, 2, 2, 3, NULL);

INSERT INTO public.calendarapp_detalleactividadacademica (id_actividad_academica_id, id_participante_id) VALUES (2, 2);

INSERT INTO public.calendarapp_tarea (datetime_inicio_estimado, datetime_inicio_real, datetime_vencimiento, datetime_alta, datetime_finalizacion, 
datetime_ultima_modificacion, observacion, es_notificable, id_estado_tarea_id, id_persona_alta_id, id_persona_finalizacion_id, id_persona_responsable_id, 
id_persona_ultima_modificacion_id, id_tipo_tarea_id, id_orientacion_academica_id, id_tutoria_id) 
VALUES ('2024-03-05 14:20:00-03', '2024-03-05 14:20:00-03', '2024-03-04 14:20:00-03', '2024-03-05 14:21:49.670119-03', NULL, 
'2024-03-05 14:21:49.670412-03', 'lectura del procedimiento de trabajo de grado', true, 1, 1, NULL, 2, 1, 1, 2, NULL);

INSERT INTO public.calendarapp_tarea (datetime_inicio_estimado, datetime_inicio_real, datetime_vencimiento, datetime_alta, datetime_finalizacion, 
datetime_ultima_modificacion, observacion, es_notificable, id_estado_tarea_id, id_persona_alta_id, id_persona_finalizacion_id, id_persona_responsable_id, 
id_persona_ultima_modificacion_id, id_tipo_tarea_id, id_orientacion_academica_id, id_tutoria_id) 
VALUES ('2024-03-05 14:20:00-03', '2024-03-05 14:20:00-03', '2024-03-04 14:20:00-03', '2024-03-05 14:21:49.682394-03', NULL, 
'2024-03-05 14:21:49.682627-03', 'lectura del procedimiento de trabajo de grado', true, 1, 1, NULL, 3, 1, 3, 2, NULL);

INSERT INTO public.calendarapp_tarea (datetime_inicio_estimado, datetime_inicio_real, datetime_vencimiento, datetime_alta, datetime_finalizacion, 
datetime_ultima_modificacion, observacion, es_notificable, id_estado_tarea_id, id_persona_alta_id, id_persona_finalizacion_id, id_persona_responsable_id, 
id_persona_ultima_modificacion_id, id_tipo_tarea_id, id_orientacion_academica_id, id_tutoria_id) 
VALUES ('2024-03-05 14:21:00-03', NULL, '2024-03-06 14:21:00-03', '2024-03-05 14:21:49.694923-03', NULL, 
'2024-03-05 14:21:49.695136-03', 'Seguimiento a lo solicitado...', true, 4, 1, NULL, 1, 1, 1, 2, NULL);

INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'cita_orientacion', 2, 4, 'Nueva solicitud de cita', false, true, false, '2024-02-05 15:16:54.857948-03', 34, 1);

INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'cita_orientacion', 2, 1, 'Cita de Orientación Académica confirmada.', false, true, false, '2024-02-05 15:19:34.920669-03', 34, 4);

INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'tarea_cita_orientacion', 2, 1, 'Te asignaron una tarea en una cita de orientación académica', false, true, false, '2024-02-05 15:21:49.678051-03', 34, 2);

INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'tarea_cita_orientacion', 2, 1, 'Te asignaron una tarea en una cita de orientación académica', false, true, false, '2024-02-05 15:2:49.690909-03', 34, 4);

--citas tutoria, karen, ricardo, rechazada

INSERT INTO public.calendarapp_event (datetime_inicio_estimado, datetime_fin_estimado, datetime_inicio_real, datetime_fin_real, datetime_registro, 
observacion, nro_curso, id_convocatoria_id, id_departamento_id, id_estado_actividad_academica_id, id_facultad_id, 
id_funcionario_docente_encargado_id, id_materia_id, id_persona_alta_id, id_persona_solicitante_id, id_persona_ultima_modificacion_id) 
VALUES ('2024-03-07 20:30:00-03', '2024-03-07 21:00:00-03', NULL, NULL, '2024-03-06 14:44:25.706021-03', 
'', '', 2, 2, 5, 1, 5, 4, 3, 3, 5);

INSERT INTO public.calendarapp_cita (id_cita_id, es_tutoria, es_orientacion_academica, es_notificable, motivo, motivo_cancelacion, motivo_rechazo, id_parametro_id) 
VALUES (3, true, false, true, 'reforzar etiquetados de listas', NULL, 'No podre estar en ese horario', 2);

INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'cita_tutoria', 3, 4, 'Nueva solicitud de cita', true, true, false, '2024-02-25 14:44:25.725355-03', 34, 5);

INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'cita_tutoria', 3, 5, 'Cita de Tutoría rechazada.', false, true, false, '2024-02-25 16:47:50.603754-03', 34, 4);

-- cita tutoria karen, blanca, confirmada

INSERT INTO public.calendarapp_event (datetime_inicio_estimado, datetime_fin_estimado, datetime_inicio_real, datetime_fin_real, datetime_registro, 
observacion, nro_curso, id_convocatoria_id, id_departamento_id, id_estado_actividad_academica_id, id_facultad_id, 
id_funcionario_docente_encargado_id, id_materia_id, id_persona_alta_id, id_persona_solicitante_id, id_persona_ultima_modificacion_id) 
VALUES ('2024-03-08 15:30:00-03', '2024-03-08 16:00:00-03', NULL, NULL, '2024-03-06 14:46:13.177488-03', 
'', '', 2, 2, 2, 1, 4, 5, 3, 3, 4);

INSERT INTO public.calendarapp_cita (id_cita_id, es_tutoria, es_orientacion_academica, es_notificable, motivo, motivo_cancelacion, motivo_rechazo, id_parametro_id) 
VALUES (4, true, false, true, 'reforzar estructura de condicionales', NULL, NULL, 2);

INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'cita_tutoria', 4, 4, 'Nueva solicitud de cita', true, true, false, '2024-02-25 14:46:13.193324-03', 34, 3);

INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'cita_tutoria', 4, 3, 'Cita de Tutoría confirmada.', false, true, false, '2024-02-25 15:46:56.940998-03', 34, 4);

-- Citas orientaciones
-- cita orientacion karen, ricardo, confirmada
INSERT INTO public.calendarapp_event (datetime_inicio_estimado, datetime_fin_estimado, datetime_inicio_real, datetime_fin_real, datetime_registro, 
observacion, nro_curso, id_convocatoria_id, id_departamento_id, id_estado_actividad_academica_id, id_facultad_id, 
id_funcionario_docente_encargado_id, id_materia_id, id_persona_alta_id, id_persona_solicitante_id, id_persona_ultima_modificacion_id) 
VALUES ('2024-03-08 20:45:00-03', '2024-03-08 21:00:00-03', NULL, NULL, '2024-03-06 14:52:04.843632-03', 
'', '', 2, 1, 2, 1, 5, NULL, 3, 3, 5);

INSERT INTO public.calendarapp_cita (id_cita_id, es_tutoria, es_orientacion_academica, es_notificable, motivo, motivo_cancelacion, motivo_rechazo, id_parametro_id) 
VALUES (5, false, true, true, 'consultar horarios de profesores', NULL, NULL, 1);

INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'cita_orientacion', 5, 4, 'Nueva solicitud de cita', false, true, false, '2024-02-24 14:52:04.85838-03', 34, 5);

INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'cita_orientacion', 5, 5, 'Cita de Orientación Académica confirmada.', false, true, false, '2024-02-24 17:54:26.493727-03', 34, 4);

-- cita orientacion karen, hugo, rechazada
INSERT INTO public.calendarapp_event (datetime_inicio_estimado, datetime_fin_estimado, datetime_inicio_real, datetime_fin_real, datetime_registro, 
observacion, nro_curso, id_convocatoria_id, id_departamento_id, id_estado_actividad_academica_id, id_facultad_id, 
id_funcionario_docente_encargado_id, id_materia_id, id_persona_alta_id, id_persona_solicitante_id, id_persona_ultima_modificacion_id) 
VALUES ('2024-03-08 20:45:00-03', '2024-03-08 21:00:00-03', NULL, NULL, '2024-03-06 14:52:24.506587-03', 
'', '', 2, 1, 5, 1, 1, NULL, 3, 3, 1);

INSERT INTO public.calendarapp_cita (id_cita_id, es_tutoria, es_orientacion_academica, es_notificable, motivo, motivo_cancelacion, motivo_rechazo, id_parametro_id) 
VALUES (6, false, true, true, 'estado academico actual', NULL, 'reposo por enfermedad', 1);

INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'cita_orientacion', 6, 4, 'Nueva solicitud de cita', false, true, false, '2024-02-25 16:52:24.52096-03', 34, 1);

INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'cita_orientacion', 6, 1, 'Cita de Orientación Académica rechazada.', false, true, false, '2024-02-25 18:55:06.633176-03', 34, 4);

--cita orientacion pendiente karen, hugo, pendiente
INSERT INTO public.calendarapp_event (datetime_inicio_estimado, datetime_fin_estimado, datetime_inicio_real, datetime_fin_real, datetime_registro, 
observacion, nro_curso, id_convocatoria_id, id_departamento_id, id_estado_actividad_academica_id, id_facultad_id, 
id_funcionario_docente_encargado_id, id_materia_id, id_persona_alta_id, id_persona_solicitante_id, id_persona_ultima_modificacion_id) 
VALUES ('2024-03-05 18:15:00-03', '2024-03-05 18:30:00-03', NULL, NULL, '2024-02-25 16:47:52.437661-03', 
'', '', 2, 1, 6, 1, 1, NULL, 3, 3, 3);

INSERT INTO public.calendarapp_cita (id_cita_id, es_tutoria, es_orientacion_academica, es_notificable, motivo, motivo_cancelacion, motivo_rechazo, id_parametro_id) 
VALUES (7, false, true, true, 'horario de clases', NULL, NULL, 1);

INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'cita_orientacion', 7, 4, 'Nueva solicitud de cita', false, true, false, '2024-02-25 16:47:52.446938-03', 34, 1);

--cita orientacion pendiente maria, hugo, pendiente
INSERT INTO public.calendarapp_event (datetime_inicio_estimado, datetime_fin_estimado, datetime_inicio_real, datetime_fin_real, datetime_registro, 
observacion, nro_curso, id_convocatoria_id, id_departamento_id, id_estado_actividad_academica_id, id_facultad_id, 
id_funcionario_docente_encargado_id, id_materia_id, id_persona_alta_id, id_persona_solicitante_id, id_persona_ultima_modificacion_id) 
VALUES ('2024-03-05 19:15:00-03', '2024-03-05 19:25:00-03', NULL, NULL, '2024-02-26 21:47:52.437661-03', 
'', '', 2, 1, 6, 1, 1, NULL, 2, 2, 2);

INSERT INTO public.calendarapp_cita (id_cita_id, es_tutoria, es_orientacion_academica, es_notificable, motivo, motivo_cancelacion, motivo_rechazo, id_parametro_id) 
VALUES (8, false, true, true, 'horario de clases', NULL, NULL, 1);

INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'cita_orientacion', 8, 2, 'Nueva solicitud de cita', false, true, false, '2024-02-25 21:47:52.446938-03', 34, 1);

-- cita tutoria cancelada karen, hugo, cancelada
INSERT INTO public.calendarapp_event (datetime_inicio_estimado, datetime_fin_estimado, datetime_inicio_real, datetime_fin_real, datetime_registro, 
observacion, nro_curso, id_convocatoria_id, id_departamento_id, id_estado_actividad_academica_id, id_facultad_id, 
id_funcionario_docente_encargado_id, id_materia_id, id_persona_alta_id, id_persona_solicitante_id, id_persona_ultima_modificacion_id) 
VALUES ('2024-03-07 19:30:00-03', '2024-03-07 20:00:00-03', NULL, NULL, '2024-02-25 16:48:57.96843-03', 
'', '', 2, 2, 4, 1, 1, 5, 3, 3, 3);

INSERT INTO public.calendarapp_cita (id_cita_id, es_tutoria, es_orientacion_academica, es_notificable, motivo, motivo_cancelacion, motivo_rechazo, id_parametro_id) 
VALUES (9, true, false, true, 'repaso de estructuras condicionales', 'otro compromiso', NULL, 2);

INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'cita_tutoria', 9, 4, 'Nueva solicitud de cita', false, true, false, '2024-02-25 16:48:57.978112-03', 34, 1);

INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'cita_tutoria', 9, 4, 'Cita de Tutoría cancelada.', false, true, false, '2024-02-25 20:49:42.842303-03', 34, 1);


-- actividades academicas sin cita
-- tutoria
INSERT INTO public.calendarapp_event (datetime_inicio_estimado, datetime_fin_estimado, datetime_inicio_real, datetime_fin_real, datetime_registro, 
observacion, nro_curso, id_convocatoria_id, id_departamento_id, id_estado_actividad_academica_id, id_facultad_id, 
id_funcionario_docente_encargado_id, id_materia_id, id_persona_alta_id, id_persona_solicitante_id, id_persona_ultima_modificacion_id) 
VALUES ('2024-03-06 19:00:00-03', '2024-03-06 19:30:00-03', '2024-03-06 19:05:00-03', '2024-03-06 19:35:43.487092-03', '2024-03-06 19:35:50.090436-03', 
'Se realizo la tutoria correspondiente al trabajo de grado final...', '456', 2, 2, 3, 1, 1, 6, 1, 3, 1);

INSERT INTO public.calendarapp_tutoria (id_tutoria_id, nombre_trabajo, id_cita_id, id_tipo_tutoria_id, motivo_cancelacion) VALUES (10, 'AcOMs', NULL, 1, NULL);

INSERT INTO public.calendarapp_detalleactividadacademica ( id_actividad_academica_id, id_participante_id) VALUES ( 10, 2);

INSERT INTO public.calendarapp_tarea (datetime_inicio_estimado, datetime_inicio_real, datetime_vencimiento, datetime_alta, datetime_finalizacion, 
datetime_ultima_modificacion, observacion, es_notificable, id_estado_tarea_id, id_persona_alta_id, id_persona_finalizacion_id, id_persona_responsable_id, 
id_persona_ultima_modificacion_id, id_tipo_tarea_id, id_orientacion_academica_id, id_tutoria_id) 
VALUES ('2024-03-06 10:23:00-03', NULL, '2024-03-11 10:23:00-03', '2024-03-06 10:23:10.096905-03', NULL, 
'2024-03-06 10:26:48.883227-03', 'Inscripcion a trabajo de grado...', true, 4, 1, NULL, 3, 1, 3, NULL, 10);

INSERT INTO public.calendarapp_tarea (datetime_inicio_estimado, datetime_inicio_real, datetime_vencimiento, datetime_alta, datetime_finalizacion, 
datetime_ultima_modificacion, observacion, es_notificable, id_estado_tarea_id, id_persona_alta_id, id_persona_finalizacion_id, id_persona_responsable_id, 
id_persona_ultima_modificacion_id, id_tipo_tarea_id, id_orientacion_academica_id, id_tutoria_id) 
VALUES ('2024-03-06 10:24:00-03', NULL, '2024-03-11 21:00:00-03', '2024-03-06 10:26:10.107039-03', NULL, 
'2024-03-06 10:26:48.886086-03', 'Hacer seguimiento a la inscripcion', true, 4, 1, NULL, 1, 1, 1, NULL, 10);

INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'tutoria', 10,1, 'Tutoría finalizada.', true, true, false, '2024-03-06 19:35:50.842303-03', 34, 4);

INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'tarea_tutoria', 10,1, 'Te asignaron una tarea en una tutoría.', true, true, false, '2024-03-06 19:40:42.842303-03', 34, 4);



-- orientaciones
INSERT INTO public.calendarapp_event (datetime_inicio_estimado, datetime_fin_estimado, datetime_inicio_real, datetime_fin_real, datetime_registro, 
observacion, nro_curso, id_convocatoria_id, id_departamento_id, id_estado_actividad_academica_id, id_facultad_id, 
id_funcionario_docente_encargado_id, id_materia_id, id_persona_alta_id, id_persona_solicitante_id, id_persona_ultima_modificacion_id) 
VALUES ('2024-03-07 18:30:00-03', '2024-03-07 18:50:00-03', '2024-03-07 18:40:41.355316-03', '2024-03-07 19:00:06.731462-03', '2024-03-07 19:00:41.355333-03', 
'Consulta sobre estado academico actual de las alumnas', '456', 2, NULL, 3, 1, 1, NULL, 1, 3, 1);

INSERT INTO public.calendarapp_orientacionacademica (id_orientacion_academica_id, id_cita_id, id_motivo_id, id_tipo_orientacion_academica_id, motivo_cancelacion) 
VALUES (11, NULL, 5, 2, NULL);

INSERT INTO public.calendarapp_detalleactividadacademica ( id_actividad_academica_id, id_participante_id) VALUES (11, 2);

INSERT INTO public.calendarapp_tarea (datetime_inicio_estimado, datetime_inicio_real, datetime_vencimiento, datetime_alta, datetime_finalizacion, 
datetime_ultima_modificacion, observacion, es_notificable, id_estado_tarea_id, id_persona_alta_id, id_persona_finalizacion_id, id_persona_responsable_id, 
id_persona_ultima_modificacion_id, id_tipo_tarea_id, id_orientacion_academica_id, id_tutoria_id) 
VALUES ('2024-03-07 10:29:00-03', NULL, '2024-03-08 10:29:00-03', '2024-03-08 10:30:41.364898-03', NULL, 
'2024-03-08 10:31:11.647624-03', 'solicitar el estado academico actual', true, 4, 1, NULL, 1, 1, 3, 11, NULL);

INSERT INTO public.calendarapp_tarea (datetime_inicio_estimado, datetime_inicio_real, datetime_vencimiento, datetime_alta, datetime_finalizacion, 
datetime_ultima_modificacion, observacion, es_notificable, id_estado_tarea_id, id_persona_alta_id, id_persona_finalizacion_id, id_persona_responsable_id, 
id_persona_ultima_modificacion_id, id_tipo_tarea_id, id_orientacion_academica_id, id_tutoria_id) 
VALUES ('2024-03-07 10:29:00-03', NULL, '2024-03-08 10:29:00-03', '2024-03-08 10:30:30.368715-03', NULL, 
'2024-03-08 10:31:41.650758-03', 'seguimiento a la solicitud...', true, 4, 1, NULL, 3, 1, 1, 11, NULL);

INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'orientacion', 11,1, 'Orientación Académica finalizada.', true, true, false, '2024-03-07 19:01:42.842303-03', 34, 4);

INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'tarea_orientacion', 11,1, 'Te asignaron una tarea en una orientación académica', true, true, false, '2024-03-07 19:01:50.842303-03', 34, 4);



INSERT INTO public.calendarapp_event (datetime_inicio_estimado, datetime_fin_estimado, datetime_inicio_real, 
datetime_fin_real, datetime_registro, observacion, nro_curso, id_convocatoria_id, id_departamento_id, id_estado_actividad_academica_id, 
id_facultad_id, id_funcionario_docente_encargado_id, id_materia_id, id_persona_alta_id, id_persona_solicitante_id, id_persona_ultima_modificacion_id) 
VALUES ('2024-03-11 16:30:00-03', '2024-03-11 17:00:00-03', NULL, NULL, '2024-03-03 17:48:33.51623-03', NULL, '', 2, 1, 6, 1, 4, 1, 3, 3, 3);

INSERT INTO public.calendarapp_cita (id_cita_id, es_tutoria, es_orientacion_academica, es_notificable, motivo, motivo_cancelacion, motivo_rechazo, id_parametro_id) 
VALUES (12, true, false, true, 'reforzar ultima clase', NULL, NULL, 2);

INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'cita_tutoria', 12, 4, 'Nueva solicitud de cita', false, true, false, '2024-03-03 17:48:33.52697-03', 34, 3);


INSERT INTO public.calendarapp_event (datetime_inicio_estimado, datetime_fin_estimado, datetime_inicio_real, 
datetime_fin_real, datetime_registro, observacion, nro_curso, id_convocatoria_id, id_departamento_id, id_estado_actividad_academica_id, 
id_facultad_id, id_funcionario_docente_encargado_id, id_materia_id, id_persona_alta_id, id_persona_solicitante_id, id_persona_ultima_modificacion_id) 
VALUES ('2024-03-11 19:15:00-03', '2024-03-11 19:30:00-03', NULL, NULL, '2024-03-03 17:49:19.663301-03', NULL, '', 2, 1, 2, 1, 1, NULL, 3, 3, 1);

INSERT INTO public.calendarapp_cita (id_cita_id, es_tutoria, es_orientacion_academica, es_notificable, motivo, motivo_cancelacion, motivo_rechazo, id_parametro_id) 
VALUES (13, false, true, true, 'trabajo de grado final...', NULL, NULL, 1);

INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'cita_orientacion', 13, 4, 'Nueva solicitud de cita', false, true, false, '2024-03-03 17:49:19.670574-03', 34, 1);
INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'cita_orientacion', 13, 1, 'Cita de Orientación Académica confirmada.', false, true, false, '2024-03-03 17:52:20.507935-03', 34, 4);


INSERT INTO public.calendarapp_event (datetime_inicio_estimado, datetime_fin_estimado, datetime_inicio_real,
 datetime_fin_real, datetime_registro, observacion, nro_curso, id_convocatoria_id, id_departamento_id, id_estado_actividad_academica_id, 
 id_facultad_id, id_funcionario_docente_encargado_id, id_materia_id, id_persona_alta_id, id_persona_solicitante_id, id_persona_ultima_modificacion_id) 
 VALUES ('2024-03-11 20:30:00-03', '2024-03-11 21:00:00-03', NULL, NULL, '2024-03-03 17:50:26.301538-03', NULL, '', 2, 2, 2, 1, 1, 5, 2, 2, 1);

INSERT INTO public.calendarapp_cita (id_cita_id, es_tutoria, es_orientacion_academica, es_notificable, motivo, motivo_cancelacion, motivo_rechazo, id_parametro_id) 
VALUES (14, true, false, true, 'reforzar ultima clase', NULL, NULL, 2);

INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'cita_tutoria', 14, 2, 'Nueva solicitud de cita', false, true, false, '2024-03-03 17:50:26.30981-03', 34, 1);
INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'cita_tutoria', 14, 1, 'Cita de Tutoría confirmada.', false, true, false, '2024-03-03 17:53:12.425585-03', 34, 2);

INSERT INTO public.calendarapp_event (datetime_inicio_estimado, datetime_fin_estimado, datetime_inicio_real, 
datetime_fin_real, datetime_registro, observacion, nro_curso, id_convocatoria_id, id_departamento_id, id_estado_actividad_academica_id, 
id_facultad_id, id_funcionario_docente_encargado_id, id_materia_id, id_persona_alta_id, id_persona_solicitante_id, id_persona_ultima_modificacion_id) 
VALUES ('2024-03-11 19:00:00-03', '2024-03-11 19:15:00-03', NULL, NULL, '2024-03-03 17:51:12.449341-03', NULL, '', 2, 1, 5, 1, 1, NULL, 2, 2, 1);


INSERT INTO public.calendarapp_cita (id_cita_id, es_tutoria, es_orientacion_academica, es_notificable, motivo, motivo_cancelacion, motivo_rechazo, id_parametro_id)
VALUES (15, false, true, true, 'refuerzo de ultima clase', NULL, 'horario no disponible', 1);

INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'cita_orientacion', 15, 2, 'Nueva solicitud de cita', false, true, false, '2024-03-03 17:51:12.456679-03', 34, 1);
INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'cita_orientacion', 15, 1, 'Cita de Orientación Académica rechazada.', false, true, false, '2024-03-03 17:52:04.338739-03', 34, 2);

INSERT INTO public.calendarapp_event (datetime_inicio_estimado, datetime_fin_estimado, datetime_inicio_real, 
datetime_fin_real, datetime_registro, observacion, nro_curso, id_convocatoria_id, id_departamento_id, id_estado_actividad_academica_id, 
id_facultad_id, id_funcionario_docente_encargado_id, id_materia_id, id_persona_alta_id, id_persona_solicitante_id, id_persona_ultima_modificacion_id) 
VALUES ('2024-03-12 19:30:00-03', '2024-03-12 20:00:00-03', NULL, NULL, '2024-03-03 18:00:10.566193-03', NULL, '', 2, 2, 6, 1, 1, 5, 3, 3, 3);

INSERT INTO public.calendarapp_cita (id_cita_id, es_tutoria, es_orientacion_academica, es_notificable, motivo, motivo_cancelacion, motivo_rechazo, id_parametro_id) 
VALUES (16, true, false, true, 'refuerzo de clase', NULL, NULL, 2);

INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'cita_tutoria', 16, 4, 'Nueva solicitud de cita', false, true, false, '2024-03-03 18:00:10.576918-03', 34, 1);

INSERT INTO public.calendarapp_event (datetime_inicio_estimado, datetime_fin_estimado, datetime_inicio_real, 
datetime_fin_real, datetime_registro, observacion, nro_curso, id_convocatoria_id, id_departamento_id, id_estado_actividad_academica_id, 
id_facultad_id, id_funcionario_docente_encargado_id, id_materia_id, id_persona_alta_id, id_persona_solicitante_id, id_persona_ultima_modificacion_id) 
VALUES ('2024-03-14 19:00:00-03', '2024-03-14 19:15:00-03', NULL, NULL, '2024-03-03 18:00:57.845317-03', NULL, '', 2, 1, 6, 1, 4, NULL, 3, 3, 3);

INSERT INTO public.calendarapp_cita (id_cita_id, es_tutoria, es_orientacion_academica, es_notificable, motivo, motivo_cancelacion, motivo_rechazo, id_parametro_id) 
VALUES (17, false, true, true, 'consultar horario de clase', NULL, NULL, 1);

INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'cita_orientacion', 17, 4, 'Nueva solicitud de cita', false, true, false, '2024-03-03 18:00:57.852512-03', 34, 3);




INSERT INTO public.calendarapp_event (datetime_inicio_estimado, datetime_fin_estimado, datetime_inicio_real, 
datetime_fin_real, datetime_registro, observacion, nro_curso, id_convocatoria_id, id_departamento_id, id_estado_actividad_academica_id, 
id_facultad_id, id_funcionario_docente_encargado_id, id_materia_id, id_persona_alta_id, id_persona_solicitante_id, id_persona_ultima_modificacion_id) 
VALUES ('2024-03-07 15:45:00-03', '2024-03-07 16:30:00-03', '2024-03-07 15:45:00-03', '2024-03-07 16:46:32.847457-03', '2024-03-07 15:46:32.847475-03', 'Se brindo la informacion solicitada', '6549', 2, 1, 3, 1, 1, 1, 1, 2, 1);

INSERT INTO public.calendarapp_orientacionacademica (id_orientacion_academica_id, id_cita_id, id_motivo_id, id_tipo_orientacion_academica_id, motivo_cancelacion) 
VALUES (18, NULL, 6, 2, NULL);

INSERT INTO public.calendarapp_event (datetime_inicio_estimado, datetime_fin_estimado, datetime_inicio_real, 
datetime_fin_real, datetime_registro, observacion, nro_curso, id_convocatoria_id, id_departamento_id, id_estado_actividad_academica_id, 
id_facultad_id, id_funcionario_docente_encargado_id, id_materia_id, id_persona_alta_id, id_persona_solicitante_id, id_persona_ultima_modificacion_id) 
VALUES ('2024-03-08 15:46:00-03', '2024-03-08 16:46:00-03', '2024-03-08 15:47:38.812658-03', NULL, '2024-03-08 15:47:38.812677-03', 'Alumno solicito tutoria de trabajo de grado final...', '', 2, 2, 4, 1, 1, 5, 1, 3, 1);
INSERT INTO public.calendarapp_tutoria (id_tutoria_id, nombre_trabajo, id_cita_id, id_tipo_tutoria_id, motivo_cancelacion) 
VALUES (19, 'AcOms', NULL, 1, 'no se pudo concretar la tutoria');
INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'tutoria', 19, 1, 'Tutoría cancelada.', false, true, false, '2024-03-08 15:48:25.740161-03', 34, 4);

INSERT INTO public.calendarapp_event (datetime_inicio_estimado, datetime_fin_estimado, datetime_inicio_real, 
datetime_fin_real, datetime_registro, observacion, nro_curso, id_convocatoria_id, id_departamento_id, id_estado_actividad_academica_id, 
id_facultad_id, id_funcionario_docente_encargado_id, id_materia_id, id_persona_alta_id, id_persona_solicitante_id, id_persona_ultima_modificacion_id) 
VALUES ('2024-03-08 15:48:00-03', '2024-03-12 15:48:00-03', '2024-03-08 15:51:00.272615-03', NULL, '2024-03-08 15:51:00.272626-03', 'Solicita cambio de curso...', '9706', 2, 3, 1, 1, 1, 3, 1, 2, 1);
INSERT INTO public.calendarapp_orientacionacademica (id_orientacion_academica_id, id_cita_id, id_motivo_id, id_tipo_orientacion_academica_id, motivo_cancelacion) 
VALUES (20, NULL, 4, 1, NULL);



INSERT INTO public.calendarapp_tarea (datetime_inicio_estimado, datetime_inicio_real, datetime_vencimiento, datetime_alta, datetime_finalizacion, 
datetime_ultima_modificacion, observacion, es_notificable, id_estado_tarea_id, id_persona_alta_id, id_persona_finalizacion_id, id_persona_responsable_id, 
id_persona_ultima_modificacion_id, id_tipo_tarea_id, id_orientacion_academica_id, id_tutoria_id) 
VALUES ('2024-03-08 15:49:00-03', NULL, '2024-03-12 15:49:00-03', '2024-03-04 15:51:00.277881-03', NULL, '2024-03-08 15:51:00.278098-03', 'Realizar seguimiento a la solicitud', true, 4, 1, NULL, 2, 1, 1, 20, NULL);
INSERT INTO public.calendarapp_tarea (datetime_inicio_estimado, datetime_inicio_real, datetime_vencimiento, datetime_alta, datetime_finalizacion, 
datetime_ultima_modificacion, observacion, es_notificable, id_estado_tarea_id, id_persona_alta_id, id_persona_finalizacion_id, id_persona_responsable_id, 
id_persona_ultima_modificacion_id, id_tipo_tarea_id, id_orientacion_academica_id, id_tutoria_id) 
VALUES ('2024-03-08 15:50:00-03', '2024-03-08 15:50:00-03', '2024-03-12 15:50:00-03', '2024-03-08 15:51:00.286279-03', NULL, '2024-03-08 15:51:00.286446-03', 'Solicitar cambio de curso', true, 1, 1, NULL, 1, 1, 3, 20, NULL);

INSERT INTO public.notify_notification (level, tipo, id_tipo, object_id_actor, verbo, read, publico, eliminado, "timestamp", actor_content_type_id, destiny_id) 
VALUES ('info', 'tarea_orientacion', 20, 1, 'Te asignaron una tarea en una orientación académica', false, true, false, '2024-03-08 15:51:00.284114-03', 34, 2);

-- cargar blanca finalizada con karen y cancelada con ricardo