from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.conf import settings
from django.db.models import Q, Count
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.cache import cache_page
import datetime


from loguru import logger
from main.models import Service, Host
from main.utils import show_queryset, show_object, bytesto

def index2(request):
    return render(request, "index2.html")

# @cache_page(10*1)


def dashboard(request):

    ts = timezone.now()
    last_min = ts - datetime.timedelta(seconds=60)

    # all hosts and their services (both up, down, host unreachable, etc)
    allhosts = Host.objects.filter(active=True, approved=True).prefetch_related("service") \
        .annotate(svc_ok=Count("service", filter=Q(service__status=0))) \
        .annotate(svc_error=Count("service", filter=~Q(service__status=0))) \
        .annotate(svc_count=Count("service")) \
        .order_by("name").distinct()

    # only hosts that are not responsive
    noresp = Host.objects.filter(active=False, approved=True)

    context = {"settings": settings, "noresp": noresp, "allhosts": allhosts, "ts": ts, "last_min": last_min}

    return render(request, "dashboard.html", context=context)


def index(request):
    """ main DJ page """
    context = {"settings": settings}
    return render(request, "index.html", context=context)


def ack_service(request, svc_id):
    """ acks incoming svc """
    svc = Service.objects.get(pk=svc_id)
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
        resp = f"""
        <button id='btn_{svc_id}'
        class='btn btn-{color} btn-sm agent-btn .ack_{svc.id}' 
        hx-get='/ack_service/{svc_id}/'
        hx-trigger='click' 
        hx-target='.ack_{svc_id}' 
        hx-swap='OuterHTML'>{msg}
        </button>"""
        return HttpResponse(resp)

def host_detail(request, monit_id):
    resp = """
    ok
    """
    current_dt = timezone.now() - datetime.timedelta(seconds=60)
    host = Host.objects.filter(pk=monit_id, approved=1)[0]
    services = Service.objects.filter(host_id=monit_id).order_by("-status")
    memory = bytesto(host.mem, 'm')
    swap = bytesto(host.swap, 'm')
    resp = """
    

    """
    context = {"obj": host, "services": services, "memory": memory, "swap": swap, "current_dt": current_dt}
#    return HttpResponse(monit_id)
    return render(request, "modal/host.html", context=context)


