from ninja import NinjaAPI
from ninja.security import django_auth
from asgiref.sync import sync_to_async
from django.db import DatabaseError, Error, IntegrityError, OperationalError
import asyncio
import datetime
from loguru import logger
import json
import xmltodict
from dictor import dictor
from .models import Host, Service

from django.shortcuts import render
from django.utils import timezone


api = NinjaAPI(csrf=False)

#!!!! need way to pull all agent queryset periodically, otherwise will read once during startup, but not update during runtime
## if a new agent is added
#hosts = Host.objects.all().select_related()



@sync_to_async
def save_host(monit_id, name, data):
    try:
        host = Host.objects.get(pk=monit_id)
        host.state = 1
        host.active = True
        host.uptime = dictor(data, "monit.server.uptime")
        host.name = name
        host.cycle = dictor(data, "monit.server.poll")
        host.monit_version = dictor(data, "monit.@version")
        host.os_name = dictor(data, "monit.platform.name")
        host.os_version = dictor(data, "monit.platform.version")
        host.os_arch = dictor(data, "monit.platform.machine")
        host.os_release = dictor(data, "monit.platform.release")
        host.cpu = dictor(data, "monit.platform.cpu")
        host.mem = dictor(data, "monit.platform.memory")
        host.swap = dictor(data, "monit.platform.swap")
        host.last_checkin = timezone.now()
        host.save()
    except Host.DoesNotExist:
        host = Host(
            name=name, 
            monit_id=monit_id, 
            state=1,
            active=True,
            cycle=dictor(data, "monit.server.poll"),
            monit_version=dictor(data, "monit_version"),
            uptime=dictor(data, "monit.server.uptime"),
            os_name=dictor(data, "monit.platform.name"),
            os_version=dictor(data, "monit.platform.version"),
            os_arch=dictor(data, "monit.platform.machine"),
            os_release=dictor(data, "monit.platform.release"),
            cpu=dictor(data, "monit.platform.cpu"),
            mem=dictor(data, "monit.platform.memory"),
            swap=dictor(data, "monit.platform.swap")
        )
        host.save()
    except (DatabaseError, Error, IntegrityError, OperationalError) as exception:
        logger.error(exception)
    return host

@sync_to_async
def save_svc(name, status, monitor, svc_data, svc_type, host):
    logger.debug("save svc")
    # update or create a service record
    try:
        svc = Service.objects.get(name=name, host=host)
        svc.status = status
        svc.monitor = monitor
        svc.data = svc_data
        svc.active = True
        svc.last_checkin = timezone.now()
        svc.save()
    except Service.DoesNotExist:
        svc = Service(name=name, host=host, svc_type=svc_type, status=status, monitor=monitor, data=svc_data)
        svc.save()

@sync_to_async
def save_event(svc_name, event, state, host):
    logger.debug("save event")
    logger.debug(svc_name)
    logger.debug(event)
    logger.debug(state)
    logger.debug(host)

    # update or create a service Event record
    try:
        svc = Service.objects.get(name=svc_name, host=host)
        if event:
            svc.event = event
            svc.state = state
        svc.save()
    except Service.DoesNotExist:
        raise "Error service does not exist"
        #svc = Service(name=name, agent=agent, svc_type=svc_type, status=status, monitor=monitor, data=svc_data)
        #svc.save()

@sync_to_async
def save_monit_state(state, monit_id):
    try:
        host = Host.objects.get(pk=monit_id)
        host.state = state 
        host.save()
    except (DatabaseError, Error, IntegrityError, OperationalError) as exception:
        logger.error(exception)


@api.get("/test")
def test(request):
    return render(request, "test1.html")

@api.post("/collector")
async def collector(request):
    #logger.success(request.body)
    json_data = json.loads(json.dumps(xmltodict.parse(request.body)))
    logger.info(json_data)
    monit_id = dictor(json_data, "monit.@id")
    name = dictor(json_data, "monit.server.localhostname")
    # create new agent record if non existent
    host = await save_host(monit_id, name, json_data)
    if dictor(json_data, "monit.services.service"):
        # delete all services that are not fresh for this agent ID
#        service_names = dictor(json_data, "monit.services.service", search="@name")
#        qs = Service.objects.get(agent_id=monit_id)


        # if list of services
        if isinstance(dictor(json_data, "monit.services.service"), list):
            for svc_data in dictor(json_data, "monit.services.service"):
                name = dictor(svc_data, "@name")
                svc_type = dictor(svc_data, "type")
                status = dictor(svc_data, "status")
                monitor = dictor(svc_data, "monitor")
     #           logger.debug(agent)
                await save_svc(name, status, monitor, svc_data, svc_type, host)
        else:
            # if single service
            svc_data = dictor(json_data, "monit.services.service")
            name = dictor(json_data, "monit.services.service.@name")
            svc_type = dictor(json_data, "monit.services.service.type")
            status = dictor(json_data, "monit.services.service.status")
            monitor = dictor(json_data, "monit.services.service.monitor")
            await save_svc(name, status, monitor, svc_data, svc_type, host)

    # check incoming event messages
    if dictor(json_data, "monit.event"):
        logger.info(dictor(json_data, "monit.event"))
        event = dictor(json_data, "monit.event.message")
        svc_name = dictor(json_data, "monit.event.service")
        state = dictor(json_data, "monit.event.state")
        if svc_name == "Monit":
            await save_monit_state(state, monit_id)
        else:
            await save_event(svc_name, event, state, host)
    return "collectgor"