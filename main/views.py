from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.conf import settings
from django.db.models import Q
import datetime
from loguru import logger
from .models import Service, Agent, Ack
from .utils import show_queryset, show_object

def index(request):

    # 1 min ago
    current_dt = datetime.datetime.now() - datetime.timedelta(minutes=1)

    warning = Agent.objects.filter(~Q(state=2), ~Q(service__status=0)).filter(last_checkin__gt=current_dt).order_by("name")
    logger.warning(warning)
    # agents with no response (dead)
    noresp = Agent.objects.filter(Q(state=2) | Q(last_checkin__lt=current_dt)).order_by("name")
    logger.warning(noresp)
    
    ok = Agent.objects.filter(~Q(state=2), Q(service__status=1), last_checkin__gt=current_dt).order_by("name")
    logger.warning(ok)
    if warning:
        for agent in warning:
            agent.services = Service.objects.filter(agent_id=agent.monit_id).all()

#        show_queryset(w)
#        show_object(w.service)
#        venue = Event.objects.filter(venue__id=venue_id)

 #   qs = Agent.objects.all().select_related().order_by("name")
    #show_queryset(qs)

    # for svc in qs:
    #     if svc.status == 2:
    #         logger.error(svc.event)
    #         if not svc.agent.name in warning.keys():
    #             warning[svc.agent.name] = []
    #         warning[svc.agent.name].append(svc)

    #for svc in warning:
    #    logger.error(f"svc name: {svc.name}, svc status: {svc.status}")

        # if not svc.agent.name in warning.keys():
        #     warning[svc.agent.name] = []
        # warning[svc.agent.name].append(svc)
        #logger.debug(s.agent.name)
    #Service.objects.filter(status=2).select_related()
    logger.debug(warning)
    context = {"settings": settings, "warning": warning, "noresp": noresp, "ok": ok}

    return render(request, "index.html", context=context)


def ack_service(request, svc_id):
    """ acks incoming svc """
    if request.method == "GET":
        try:
            ack = Ack.objects.get(service__id=svc_id)
            if ack:
                svc.save()
        except Ack.DoesNotExist:
            ack = 
        
        logger.warning(svc_id)
        
        logger.debug(qs)
        return HttpResponse("akc ack ack")
        