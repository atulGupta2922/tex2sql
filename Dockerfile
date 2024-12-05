# pull the official docker image
FROM python:3.12.0-slim

# set work directory
WORKDIR /

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_SECRET b840841ab65d5a17c9efaa6b8e355747cda66f89c06ea2c7c2ed303e09644be7

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .