FROM python:3.10-bullseye

RUN mkdir -p "/opt/services/src"
WORKDIR /opt/services/src

COPY requirements.txt .
RUN pip install -r requirements.txt

#COPY . .

#EXPOSE 8000
#EXPOSE 8000-9000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]