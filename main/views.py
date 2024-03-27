from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.conf import settings
from django.db.models import Q, Count
from django.urls import reverse
from django.views.decorators.cache import cache_page
import datetime
from loguru import logger
from .models import Service, Host
from .utils import show_queryset, show_object, bytesto

#def index(request):
    #return render(request, "index.html")



def dashboard2(request):
    logger.debug("DASHBOARD")
    ts = datetime.datetime.now()
    last_min = datetime.datetime.now() - datetime.timedelta(seconds=60)
    #warning = Host.objects.annotate(nonzero=Count("service", filter=~Q(service__status=0))) \
        #.filter(last_checkin__gt=current_dt).order_by("name").prefetch_related("service").filter(nonzero__gt=0).distinct()
    
    #allhosts = Host.objects.annotate(nonzero=Count("service")).prefetch_related("service").filter(nonzero__gt=0).distinct().order_by("name")


#.filter(service__monitor=1) \

    ## all hosts and their services (both up, down, host unreachable, etc)
    allhosts = Host.objects.filter(last_checkin__gt=last_min).prefetch_related("service") \
        .filter(service__last_modified__gt=last_min) \
        .annotate(svc_ok=Count("service", filter=Q(service__status=0))) \
        .annotate(svc_count=Count("service")) \
        .order_by("name").distinct()

    ## only hosts with services that have problems
    #warning = allhosts.annotate(nonzero=Count("service", filter=~Q(service__status=0))).order_by("name").filter(nonzero__gt=0).filter(service__last_modified__gt=current_dt).distinct()
    
    ## only hosts that are not responsive
    noresp = Host.objects.filter(last_checkin__lt=last_min)

    context = {"settings": settings, "noresp": noresp, "allhosts": allhosts, "ts": ts, "last_min": last_min }

    return render(request, "index2.html", context=context)


#@cache_page(10*1)
def dashboard(request):
    logger.debug("DASHBOARD")
    ts = datetime.datetime.now()
    last_min = datetime.datetime.now() - datetime.timedelta(seconds=60)
    #warning = Host.objects.annotate(nonzero=Count("service", filter=~Q(service__status=0))) \
        #.filter(last_checkin__gt=current_dt).order_by("name").prefetch_related("service").filter(nonzero__gt=0).distinct()
    
    #allhosts = Host.objects.annotate(nonzero=Count("service")).prefetch_related("service").filter(nonzero__gt=0).distinct().order_by("name")


#.filter(service__monitor=1) \

    ## all hosts and their services (both up, down, host unreachable, etc)
    allhosts = Host.objects.filter(last_checkin__gt=last_min).prefetch_related("service") \
        .filter(service__last_modified__gt=last_min) \
        .annotate(svc_ok=Count("service", filter=Q(service__status=0))) \
        .annotate(svc_count=Count("service")) \
        .order_by("name").distinct()

    ## only hosts with services that have problems
    #warning = allhosts.annotate(nonzero=Count("service", filter=~Q(service__status=0))).order_by("name").filter(nonzero__gt=0).filter(service__last_modified__gt=current_dt).distinct()
    
    ## only hosts that are not responsive
    noresp = Host.objects.filter(last_checkin__lt=last_min)

    context = {"settings": settings, "noresp": noresp, "allhosts": allhosts, "ts": ts, "last_min": last_min }

    return render(request, "dashboard.html", context=context)
    
def index(request):
    
    context = {"settings": settings}

    return render(request, "index.html", context=context)


def ack_service(request, svc_id):
    """ acks incoming svc """

    
    svc = Service.objects.get(pk=svc_id)
    logger.warning(svc.state)
    
    if svc.ack == True:
        svc.ack = False
        msg = "Ack"
        color = "primary"
    else:
        svc.ack = True
        msg = "Un-Ack"
        color = "secondary"
    svc.save()

    if request.method == "GET":
        logger.warning(svc_id)
        resp = f"""
        <button id='btn_{svc_id}'
        class='btn btn-{color} btn-sm agent-btn .ack_{svc.id}' 
        hx-get='/ack_service/{svc_id}/'
        hx-trigger='click' 
        hx-target='.ack_{svc_id}' 
        hx-swap='OuterHTML'>{msg}
        </button>"""
        return HttpResponse(resp)

#def show_agent_info(request):
#    """ show details information about agent """

def test(request):
    return render(request, "test1.html")

def host_delete(request, monit_id):
    """ delete monit agent """
    #try:
        #row = 
    return monit_id




def host_detail(request, monit_id):
    resp = """
    ok
    """
    current_dt = datetime.datetime.now() - datetime.timedelta(seconds=60)
    host = Host.objects.get(pk=monit_id)
    logger.debug(host.service)
    services = Service.objects.filter(host_id=monit_id).filter(last_modified__gt=current_dt).order_by("-status")
    logger.debug(services)
    memory = bytesto(host.mem, 'm')
    swap = bytesto(host.swap, 'm')
    resp = """
    

    """
    context = {"obj": host, "services": services, "memory": memory, "swap": swap, "current_dt": current_dt}
#    return HttpResponse(monit_id)
    return render(request, "modal/host.html", context=context)