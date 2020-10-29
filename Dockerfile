FROM python:3.8

WORKDIR /usr/src/csv_handler

ENV PYTHONDONTWRITEBYTECODE 1
ENV IS_DOCKER 1

RUN apt-get update && apt-get install netcat -y

COPY requirements.txt /usr/src/requirements.txt
RUN pip install -r /usr/src/requirements.txt

COPY . /usr/src/csv_handler

RUN chmod +x /usr/src/csv_handler/entrypoint.sh

ENTRYPOINT ["bash", "/usr/src/csv_handler/entrypoint.sh"]