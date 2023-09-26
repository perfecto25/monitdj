# monitdj

a Django based M/Monit alternative for monitoring hosts using Tildeslash Monit agent


## Requirements

developed on Ubuntu 22.04

- python 3.11
- pipenv (python3.11 -m pip install pipenv)
- postgres (tested on postgres 14)
- django 4.2.5

OS pkgs

- python3.11-dev
- postgresql postgresql-contrib libpq-dev python3-dev


## DB setup

postgres setup

    sudo -u postgres psql
    postgres=# create user monitdj with password 'monitdj';
    postgres=# create database monitdjdb with encoding 'utf8' owner=monitdj;
    \c monitdjdb
    monitdjdb=# alter default privileges grant all on tables to monitdj;

## Components

- bootstrap version 5.2.3
- theme: https://demos.themeselection.com/sneat-bootstrap-html-admin-template-free/html/index.html

## Developing

### initial setup of project

    python3.11 -m pip install django
    django-admin startproject monitdj
    cd monitdj
    manage.py startapp main
    manage.py migrate
    ./manage.py collectstatic --noinput (creates static_pub directory for serving js/css/img)


## Prod deploy

    uvicorn monitdj.asgi:application --reload --host 0.0.0.0