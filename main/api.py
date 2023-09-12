from ninja import NinjaAPI
from ninja.security import django_auth
from asgiref.sync import sync_to_async

from loguru import logger
import json
import xmltodict
from dictor import dictor as D
from .models import Agent, Service


api = NinjaAPI(csrf=False)

#!!!! need way to pull all agent queryset periodically, otherwise will read once during startup, but not update during runtime
## if a new agent is added
agents = Agent.objects.all().select_related()


async def save_svc(name, status, monitor, svc_data, svc_type, agent):
    # update or create a service record
    logger.warning(agent)
    logger.warning(name)
    logger.warning(svc_data)
    try:
        svc = await Service.objects.get(name=name, agent=agent)
        svc.status = status
        svc.monitor = monitor
        svc.data = svc_data
        svc.save()
    except Service.DoesNotExist:
        svc = Service(name=name, agent=agent, svc_type=svc_type, status=status, monitor=monitor, data=svc_data)
        svc.save()

@api.post("/collector")
async def collector(request):
    json_data = json.loads(json.dumps(xmltodict.parse(request.body)))
    logger.info(json_data)
    monit_id = D(json_data, "monit.@id")
    name = D(json_data, "monit.server.localhostname")
    # create new agent record if non existent
    try:
        agent = Agent.objects.get(pk=monit_id)
    except Agent.DoesNotExist:
        agent = Agent(name=name, monit_id=monit_id)
        agent.save()

    if D(json_data, "monit.services.service"):
        # if list of services
        if isinstance(D(json_data, "monit.services.service"), list):
            for svc_data in D(json_data, "monit.services.service"):
                name = D(svc_data, "@name")
                svc_type = D(svc_data, "type")
                status = D(svc_data, "status")
                monitor = D(svc_data, "monitor")
                await save_svc(name, status, monitor, svc_data, svc_type, agent)
        else:
            # if single service
            svc_data = D(json_data, "monit.services.service")
            name = D(json_data, "monit.services.service.@name")
            svc_type = D(json_data, "monit.services.service.type")
            status = D(json_data, "monit.services.service.status")
            monitor = D(json_data, "monit.services.service.monitor")

            logger.debug(name)
            logger.debug(svc_type)
            logger.debug(monitor)
            await save_svc(name, status, monitor, svc_data, svc_type, agent)

    else:
        return "No services found"

    return "collectgor"