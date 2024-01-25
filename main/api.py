from ninja import NinjaAPI
from ninja.security import django_auth
from asgiref.sync import sync_to_async
from django.db import DatabaseError, Error, IntegrityError, OperationalError
import asyncio
import datetime
from loguru import logger
import json
import xmltodict
from dictor import dictor as D
from .models import Agent, Service

from django.shortcuts import render

api = NinjaAPI(csrf=False)

#!!!! need way to pull all agent queryset periodically, otherwise will read once during startup, but not update during runtime
## if a new agent is added
agents = Agent.objects.all().select_related()



@sync_to_async
def save_agent(monit_id, name, data):
    try:
        agent = Agent.objects.get(pk=monit_id)
        agent.state = 1
        agent.uptime = D(data, "monit.server.uptime")
        agent.name = name
        agent.cycle = D(data, "monit.server.poll")
        agent.monit_version = D(data, "monit.@version")
        agent.os_name = D(data, "monit.platform.name")
        agent.os_version = D(data, "monit.platform.version")
        agent.os_arch = D(data, "monit.platform.machine")
        agent.os_release = D(data, "monit.platform.release")
        agent.cpu = D(data, "monit.platform.cpu")
        agent.mem = D(data, "monit.platform.memory")
        agent.swap = D(data, "monit.platform.swap")
        agent.save()
    except Agent.DoesNotExist:
        agent = Agent(
            name=name, 
            monit_id=monit_id, 
            state=1,
            cycle=D(data, "monit.server.poll"),
            monit_version=D(data, "monit_version"),
            uptime=D(data, "monit.server.uptime"),
            os_name=D(data, "monit.platform.name"),
            os_version=D(data, "monit.platform.version"),
            os_arch=D(data, "monit.platform.machine"),
            os_release=D(data, "monit.platform.release"),
            cpu=D(data, "monit.platform.cpu"),
            mem=D(data, "monit.platform.memory"),
            swap=D(data, "monit.platform.swap")
        )
        agent.save()
    except (DatabaseError, Error, IntegrityError, OperationalError) as exception:
        logger.error(exception)
    return agent

@sync_to_async
def save_svc(name, status, monitor, svc_data, svc_type, agent):
    # update or create a service record
    try:
        svc = Service.objects.get(name=name, agent=agent)
        svc.status = status
        svc.monitor = monitor
        svc.data = svc_data
        svc.save()
    except Service.DoesNotExist:
        svc = Service(name=name, agent=agent, svc_type=svc_type, status=status, monitor=monitor, data=svc_data)
        svc.save()

@sync_to_async
def save_event(svc_name, event, state, agent):
    #logger.debug(svc_name)
    #logger.debug(event)
    #logger.debug(agent)
    #logger.debug(state)

    # update or create a service Event record
    try:
        svc = Service.objects.get(name=svc_name, agent=agent)
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
        agent = Agent.objects.get(pk=monit_id)
        agent.state = state 
        agent.save()
    except (DatabaseError, Error, IntegrityError, OperationaError) as exception:
        logger.error(exception)


@api.get("/test")
def test(request):
    return render(request, "test1.html")

@api.post("/collector")
async def collector(request):
    #logger.success(request.body)
    json_data = json.loads(json.dumps(xmltodict.parse(request.body)))
    logger.info(json_data)
    monit_id = D(json_data, "monit.@id")
    name = D(json_data, "monit.server.localhostname")
    # create new agent record if non existent
    agent = await save_agent(monit_id, name, json_data)
    

    if D(json_data, "monit.services.service"):
        # delete all services that are not fresh for this agent ID
#        service_names = D(json_data, "monit.services.service", search="@name")
#        qs = Service.objects.get(agent_id=monit_id)


        # if list of services
        if isinstance(D(json_data, "monit.services.service"), list):
            for svc_data in D(json_data, "monit.services.service"):
                name = D(svc_data, "@name")
                svc_type = D(svc_data, "type")
                status = D(svc_data, "status")
                monitor = D(svc_data, "monitor")
     #           logger.debug(agent)
                await save_svc(name, status, monitor, svc_data, svc_type, agent)
        else:
            # if single service
            svc_data = D(json_data, "monit.services.service")
            name = D(json_data, "monit.services.service.@name")
            svc_type = D(json_data, "monit.services.service.type")
            status = D(json_data, "monit.services.service.status")
            monitor = D(json_data, "monit.services.service.monitor")
            await save_svc(name, status, monitor, svc_data, svc_type, agent)

    # check incoming event messages
    if D(json_data, "monit.event"):
        event = D(json_data, "monit.event.message")
        svc_name = D(json_data, "monit.event.service")
        state = D(json_data, "monit.event.state")
        if svc_name == "Monit":
            await save_monit_state(state, monit_id)
        else:
            await save_event(svc_name, event, state, agent)
    return "collectgor"