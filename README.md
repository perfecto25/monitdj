# Monitbee

a Django based M/Monit alternative for monitoring hosts using Tildeslash Monit agent


## Requirements

developed on Ubuntu 22.04

- python 3.11
- python3.11-dev (pkg)
- pipenv (python3.11 -m pip install pipenv)
- postgres (tested on postgres 14)

## DB setup

postgres setup

    sudo -u postgres psql
    postgres=# create user monitbee with password 'monitbee';
    postgres=# create database mb with encoding 'utf8' owner=monitbee;
    \c mb
    mb=# alter default privileges grant all on tables to monitbee;

## Components

- bootstrap version 5.2.3
- theme: https://demos.themeselection.com/sneat-bootstrap-html-admin-template-free/html/index.html

## Developing

### initial setup of project

    python3.11 -m pip install django
    django-admin startproject monitbee
    cd monitbee
    manage.py startapp main
    manage.py migrate


