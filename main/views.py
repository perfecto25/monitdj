from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.conf import settings
from django.db.models import Q

from loguru import logger
from .models import Service, Agent

def show_queryset(queryset):
    """ show all fields inside a queryset object """
    if queryset:
        model = queryset.model
        fields = model._meta.fields
        for field in fields:
            logger.debug(field.name)
    else:
        logger.debug("The queryset is empty.")

def index(request):
    #qs = Agent.objects.select_related().all()
    agents = {}
    warning = {}
    agents["ok"] = {}
    agents["down"] = {}
    #qs = Service.objects.filter(~Q(status=0)).select_related("agent").order_by("agent")
    warning = Service.objects.filter(~Q(agent__state=2), ~Q(status=0)).order_by("agent__name")    

#        venue = Event.objects.filter(venue__id=venue_id)

 #   qs = Agent.objects.all().select_related().order_by("name")
    #show_queryset(qs)

    # for svc in qs:
    #     if svc.status == 2:
    #         logger.error(svc.event)
    #         if not svc.agent.name in warning.keys():
    #             warning[svc.agent.name] = []
    #         warning[svc.agent.name].append(svc)

    for svc in warning:
        logger.error(f"svc name: {svc.name}, svc status: {svc.status}")

        # if not svc.agent.name in warning.keys():
        #     warning[svc.agent.name] = []
        # warning[svc.agent.name].append(svc)
        #logger.debug(s.agent.name)
    #Service.objects.filter(status=2).select_related()
    logger.debug(warning)
    context = {"settings": settings, "agents": agents, "warning": warning}

    return render(request, "index.html", context=context)

@csrf_exempt
def collector(request):

    if request.method == "POST":
        logger.debug(request.body)
        return HttpResponse("ok")
    if request.method == "GET":
        logger.warning(request)
