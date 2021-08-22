FROM ubuntu:20.10

RUN apt-get update -y && apt-get install -y python3-pip python-dev

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt

COPY validate.py /app

COPY wsgi.py /app

CMD gunicorn --certfile=/certs/webhook.crt --keyfile=/certs/webhook.key --bind 0.0.0.0:443 wsgi:webhook