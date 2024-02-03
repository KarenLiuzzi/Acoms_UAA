FROM python:3.8

WORKDIR /app

COPY requirements.txt /app/
RUN apt-get update && apt-get install -y apache2-dev && pip install mod-wsgi==4.7.1
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
COPY data.sql /app/  

CMD ["python", "manage.py", "runserver", "localhost:8000"]