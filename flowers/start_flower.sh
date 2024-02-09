#!/bin/sh
# #!/bin/bash

# echo "Waiting for celery..."

#     while ! nc -v -z celery 6400; do
#       sleep 1
#     done

# echo "Celery started"

# echo 'Iniciado flower'
# celery -A eventcalendar flower

until timeout 10s celery inspect ping; do
    >&2 echo "Celery workers not available"
done

echo 'Starting flower'
celery flower