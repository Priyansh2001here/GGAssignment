FROM python:3.10-bullseye

RUN mkdir -p "/opt/services/src"
WORKDIR /opt/services/src

COPY requirements.txt .
RUN pip install -r requirements.txt

