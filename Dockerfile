# Dockerfile, Image, Container
FROM python:3.10

WORKDIR /flask-app

COPY pip-reqs.txt .

RUN pip install -r pip-reqs.txt

COPY ./FlaskDemo ./app

CMD ["python", "./app/azure-ls-app.py"]