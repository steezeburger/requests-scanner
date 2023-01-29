FROM python:3.10-slim as base
ENV PYTHONUNBUFFERED 1

# install pipenv and compilation dependencies
RUN apt-get update && apt-get install -y build-essential gcc
RUN pip install --upgrade pip pipenv
RUN pip install idna_ssl

# install python dependencies
RUN mkdir /code
WORKDIR /code
COPY Pipfile /code
COPY Pipfile.lock /code
RUN pipenv install --dev --deploy --system

# install application into container
COPY . /code

# run application
EXPOSE 8053

WORKDIR /code/app

# this CMD is overridden by the command in docker-compose.yml for local development
#CMD daphne -b 0.0.0.0 -p 8001 app.asgi:application
