FROM python:3.7.13-alpine3.14

WORKDIR /app

ADD .  /app

RUN pip install -r requirements.txt

CMD ["python", "./example/main.py"]