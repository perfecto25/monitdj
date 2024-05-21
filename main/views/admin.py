from loguru import logger
from django.shortcuts import render
from django.http import HttpResponse
from main.models import Service, Host
from main.utils import show_queryset, show_object, bytesto


def hosts(request):
    pending = Host.objects.filter(active=True, approved=False)
    allhosts = Host.objects.filter(approved=True)
    context = {"pending": pending, "allhosts": allhosts}
    return render(request, "admin/hosts.html", context=context)


def approve_host(request, monit_id):
    """ approves or declines a new host """
    logger.debug(request)
    logger.warning("XXX")
    return HttpResponse("approved")
