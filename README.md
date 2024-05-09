# monitdj

a Django based M/Monit alternative for monitoring hosts using Tildeslash Monit agent


## Requirementsfrom django_cron import CronJobBase, Schedule

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 120 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'my_app.my_cron_job'    # a unique code

    def do(self):
        pass    # do your thing here

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


## Crontab

MonitDJ uses a cron that updates all hosts and service Active field to False if the host or service hasnt checked in over a minute.

    ./manage.py crontab add
    

## Components

- bootstrap version 5.2.3
- theme: https://zuramai.github.io/mazer/demo/layout-default.html

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


# feature list

- allow alert Ack / Unack - if alert is acked, dont send notifications for X amount of time as defined in config
- allow alert urgency - urgency of 1 will notify every 5 min, urg2 every 15 min , urg3 every 30 min etc

Alerting

- 4 layers / tiers of alerts

1st layer = default, all agents unless specified get default alert settings, 
ie, alert every 10min unti problem is resolved

2nd layer - per host group
each host group has specific alert settings, ie prod = alert every 5 min
sim = alert every 15 min
dev = alert every 1 hr etc

3rd layer = per host
each host has unique alert setting 
host1 = alert every 5 min
host2 = alert every 24hrs 

4th layer = per service
on a host, each service can have multiple notifications variations
ie nginx = alert every 3 hrs 
db svc = alert every 5 min (alert a specific slack channel)
postfix svc = alert every 30 min (alert a specific email addr)

when monit agent checks in, if service triggers alert, DJ will check 4th layer and move on up
- does agent have 4th layer config for each svc? if yes, use 4th tier to notify
- if no, does agent have 3rd tier config for the host? if yes, alert for the host
- if no, does host group have notification settings?
- if no, use default notification setting


- each host should have ability to schedule maint windows where alerts are suppressed (DOWNTIME WINDOW)
- each host should have ability to silence all alerts on predefined time, ie silence all alerts on nycweb1 for 15min, 30min, 45min, 1hr, 3hr, 6hr, 12hr, 24hr (SILENCE)

### Dashboards

have dashboards by

- service (show me status of all inbound gateways)
- region (show me all servers in Chicago)
- host groups (show me all servers that are production trading hosts)
- env (show me all production servers)
- 

### Connectors
- have ability to add a Connector (email, slack, etc)
each connector is separate py file that handles notification logic
ie slack is API handler, takes slack webhook URL and sends request


