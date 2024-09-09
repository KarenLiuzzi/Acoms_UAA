
<div align="center">
    <h1 align="center">Academic Orientation Management System</h1>
</div>

Welcome to my repository. Here, you will find a project done for the "Universidad Autónoma de Asunción" that deals with the management of academic orientation activities (tutoring appointments and academic orientations) provided by the faculty for the students.

## Build and run the docker container

```bash
docker compose build && docker compose up
```

## 🚀 Documentation
### Project Structure
- **credentials**: to use the system you can find some basic credentials in the file `credentials.txt`.
- **.env**: you must create your own variables environments in the file .env:

`.env:`
```
DEBUG=
SECRET_KEY=
DJANGO_ALLOWED_HOSTS=
TZ=
CELERY_BROKER=
CELERY_BACKEND=
FLOWER_LOCALE=
FLOWER_PORT=
SQL_ENGINE=
SQL_DATABASE=
SQL_USER=
SQL_PASSWORD=
SQL_HOST=
SQL_PORT=
DATABASE=
PGADMIN_DEFAULT_EMAIL=
PGADMIN_DEFAULT_PASSWORD=
DESTINATARY_EMAIL=
SENDER_EMAIL=
SENDER_PASSWORD=
```
-------------------------------------------------


## 🤖 Tech stack
- [Django](https://www.djangoproject.com/) as the main development framework.
- [docker](https://www.docker.com/) to contain our services.
- [nginx](https://nginx.org/en/) our HTTP and reverse proxy server.
- [Celery](https://docs.celeryq.dev/en/stable/) responsible for the execution of asynchronous tasks for the collection of data from external service.
- [Redis](https://redis.io/) our message broker between django and celery.
- [flowers](https://flower.readthedocs.io/en/latest/) to supervise and manage Celery's tasks.

## Some System screenshots 

### Main View

![plot](./screenshoots/Vista_func_doc.png)

### Appointment Monthly Calendar

![plot](./screenshoots/Vista_func_doc_mes_calendario.png)

### Appointment Daily Calendar

![plot](./screenshoots/Vista_func_doc_dia_calendario.png)

### Main Administration view

![plot](./screenshoots/Vista_func_doc_panel_administrativo.png)

## 📜 License


Distributed under the GNU General Public License v3.0. See [`LICENSE`](./LICENSE) for more information.
