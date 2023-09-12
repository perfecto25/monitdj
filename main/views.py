from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.conf import settings
from django.db.models import Q

from loguru import logger
from .models import Service, Agent

def index(request):
    warning = {}
    #qs = Agent.objects.prefetch_related("service").all()
    qs = Service.objects.filter(~Q(status=0)).select_related("agent").order_by("agent")
    for s in qs:
        logger.debug(s.name)
        logger.debug(s.agent.name)
    #Service.objects.filter(status=2).select_related()

    context = {"settings": settings, "qs": qs}

    return render(request, "index.html", context=context)

@csrf_exempt
def collector(request):

    if request.method == "POST":
        logger.debug(request.body)
        return HttpResponse("ok")
    if request.method == "GET":
        logger.warning(request)
