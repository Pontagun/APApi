FROM python:3-alpine

LABEL maintainer="pontagun@gmail.com"
LABEL version="0.0.1"
LABEL description="-"

ENV FLASK_APP=main.py
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apk add --no-cache mariadb-connector-c-dev ;\
    apk add --no-cache --virtual .build-deps \
        build-base \
        mariadb-dev ;\
    pip install mysqlclient;\
    apk del .build-deps ;\
    apk add bash


COPY . .
RUN ls
RUN pip3 install --no-cache-dir -r requirements.txt


CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

EXPOSE 5000