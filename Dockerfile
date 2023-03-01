FROM python:3.8-slim-buster

WORKDIR /opt/garbage-collector-api

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

ENV WEBSCRAPER_SLEEP 3600

COPY . /opt/garbage-collector-api/

ENTRYPOINT ["/opt/garbage-collector-api/docker-entrypoint.sh"]

CMD ["sh"]