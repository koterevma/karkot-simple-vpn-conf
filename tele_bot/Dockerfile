# syntax=docker/dockerfile:1

FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

VOLUME /app/data
VOLUME /app/wireguard

CMD [ "python3", "main.py" ]
