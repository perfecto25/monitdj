from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.conf import settings
from django.db.models import Q

from loguru import logger
from .models import Service, Agent

def index(request):
    logger.debug(settings.STATIC_ROOT)
    logger.debug(settings.STATIC_URL)
    #qs = Agent.objects.select_related().all()
    agents = {}
    warning = {}
    agents["ok"] = {}
    agents["noresponse"] = {}
    qs = Service.objects.filter(~Q(status=0)).select_related("agent").order_by("agent")
    for svc in qs:
        if svc.status == 2:
            logger.error(svc.event)
            if not svc.agent.name in warning.keys():
                warning[svc.agent.name] = []
            warning[svc.agent.name].append(svc)



    logger.debug(type(warning))
    logger.debug(warning)
        #logger.debug(s.agent.name)
    #Service.objects.filter(status=2).select_related()

    context = {"settings": settings, "agents": agents, "warning": warning}

    return render(request, "index.html", context=context)

@csrf_exempt
def collector(request):

    if request.method == "POST":
        logger.debug(request.body)
        return HttpResponse("ok")
    if request.method == "GET":
        logger.warning(request)
