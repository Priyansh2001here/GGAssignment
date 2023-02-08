FROM python:3.11-bullseye

RUN mkdir -p "/opt/services/src"
WORKDIR /opt/services/src

COPY requirements.txt .
RUN pip install -r requirements.txt


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]