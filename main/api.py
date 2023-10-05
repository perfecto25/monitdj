from ninja import NinjaAPI
from ninja.security import django_auth
from asgiref.sync import sync_to_async
from django.db import DatabaseError, Error, IntegrityError, OperationalError
import asyncio
from loguru import logger
import json
import xmltodict
from dictor import dictor as D
from .models import Agent, Service


api = NinjaAPI(csrf=False)

#!!!! need way to pull all agent queryset periodically, otherwise will read once during startup, but not update during runtime
## if a new agent is added
agents = Agent.objects.all().select_related()


@sync_to_async
def save_agent(monit_id, name):
    try:
        agent = Agent.objects.get(pk=monit_id)
        agent.state = 1
        agent.save()
    except Agent.DoesNotExist:
        agent = Agent(name=name, monit_id=monit_id, state=1)
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
    except (DatabaseError, Error, IntegrityError, OperationalError) as exception:
        logger.error(exception)

@api.post("/collector")
async def collector(request):
    #logger.success(request.body)
    json_data = json.loads(json.dumps(xmltodict.parse(request.body)))
    #logger.info(json_data)
    monit_id = D(json_data, "monit.@id")
    name = D(json_data, "monit.server.localhostname")
    # create new agent record if non existent
    agent = await save_agent(monit_id, name)
    
    #logger.warning(agent)
    if D(json_data, "monit.services.service"):
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