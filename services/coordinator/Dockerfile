FROM python:3.12-slim
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update

#get python packages
RUN pip install confluent-kafka jsonschema "psycopg[binary]"
RUN pip install -e common_helpers