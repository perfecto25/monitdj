from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.conf import settings
from django.db.models import Q, Count
from django.urls import reverse
import datetime
from loguru import logger
from .models import Service, Host, Ack
from .utils import show_queryset, show_object, bytesto

#def index(request):
    #return render(request, "index.html")

def index(request):

    # 1 min ago
    current_dt = datetime.datetime.now() - datetime.timedelta(minutes=1)
    #logger.debug(datetime.datetime.now())
    logger.debug(current_dt)

    #warning = Host.objects.filter(~Q(state=2).exclude(~Q) & Q(service__status=1)).distinct() \
    #    .filter(last_checkin__gt=current_dt).order_by("name").prefetch_related("service")
    
    # get all Hosts that have services with problems (ie, service status != 0), exclude any Host that does not have any problems
    warning = Host.objects.annotate(nonzero=Count("service", filter=~Q(service__status=0))) \
        .filter(last_checkin__gt=current_dt).order_by("name").prefetch_related("service").filter(nonzero__gt=0)
    
    for h in warning:
       logger.debug(h.name)
       logger.success(h.service.all())
       for svc in h.service.all():
           logger.success(svc.state)
    #warning = Service.objects.filter(~Q(status=0)).filter(last_modified__gt=current_dt).select_related("host").order_by("host__name")
    #warning = Host.objects.filter(~Q(state=2)).filter(last_checkin__gt=current_dt).order_by("name")
    #logger.error(show_queryset(warning))
    # agents with no response (dead)
    #noresp = Host.objects.filter(Q(state=2) | Q(last_checkin__lt=current_dt)).order_by("name")
    #logger.warning(noresp)
    
    # ok = Host.objects.filter(~Q(state=2), Q(service__status=1), last_checkin__gt=current_dt).order_by("name")
    # logger.warning(ok)
    # if warning:
    #     for host in warning:
    #         host.services = Service.objects.filter(host_id=host.monit_id).select_related().all()
    #         for svc in host.services:
    #             svc.ack = Ack.objects.filter(service=svc)
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
    #logger.debug(warning)
    context = {"settings": settings, "warning": warning}

    return render(request, "index.html", context=context)


def ack_service(request, svc_id):
    """ acks incoming svc """

    try:
        ack = Ack.objects.get(service__id=svc_id)
        logger.warning(ack.state)
        if ack:
            if ack.state == True:
                ack.state = False
                msg = "Ack"
                color = "primary"
            else:
                ack.state = True
                msg = "Un-Ack"
                color = "secondary"
            ack.save()
    except Ack.DoesNotExist:
        ack = Ack(state=True, service_id=svc_id)
        ack.save()
        msg = "Un-Ack"
        color = "secondary"


    if request.method == "GET":
        logger.warning(svc_id)
        resp = f"""
        <button id='btn_{svc_id}'
        class='btn btn-{color} btn-sm agent-btn ack_btn' 
        hx-get='/ack_service/{svc_id}/'
        hx-trigger='click' 
        hx-target='#target_{svc_id}' 
        hx-swap='OuterHTML'>{msg}
        </button>"""
        return HttpResponse(resp)

#def show_agent_info(request):
#    """ show details information about agent """

def test(request):
    return render(request, "test1.html")



def host_detail(request, monit_id):
    resp = """
    ok
    """
    host = Host.objects.get(pk=monit_id)
    services = Service.objects.filter(host_id=monit_id)
    memory = bytesto(host.mem, 'm')
    swap = bytesto(host.swap, 'm')
    resp = """
    

    """
    context = {"obj": host, "services": services, "memory": memory, "swap": swap}
#    return HttpResponse(monit_id)
    return render(request, "modal/host.html", context=context)