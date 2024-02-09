FROM python:3.8.12-slim-buster

WORKDIR /home/flower

COPY start_flower.sh .
RUN apt-get update && apt-get install -y --no-install-recommends netcat
RUN pip install flower

USER root
RUN chmod 755 start_flower.sh
ENTRYPOINT ["/home/flower/start_flower.sh"]
