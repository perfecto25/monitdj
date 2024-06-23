from loguru import logger
from django.shortcuts import render, redirect
from django.http import HttpResponse
from main.models import Service, Host, HostGroup
from main.utils import show_queryset, show_object, bytesto
from dictor import dictor


def get_hosts(request):
    pending = Host.objects.filter(active=True, approved=False)
    allhosts = Host.objects.filter(approved=True).order_by('active', 'name')
    context = {"pending": pending, "allhosts": allhosts}
    return render(request, "admin/hosts.html", context=context)

def host_action(request):
    """ approve/delete/ignore a host """
    if request.method == "POST":
        action = dictor(request.POST, "action")
        monit_id = dictor(request.POST, "monit_id")
        logger.debug(request.POST)
        if action == "approve":
            logger.info(f"approving host ID: {monit_id}")
            host = Host.objects.filter(pk=monit_id)
            host.update(approved=1)
        if action == "delete":
            logger.info(f"deleting host ID: {monit_id}")
            Host.objects.filter(pk=monit_id).delete()
        if action == "ignore":
            logger.info(f"ignoring host ID: {monit_id}")
            Host.objects.filter(pk=monit_id).update(ignore=ignore)
        return redirect("get_hosts")


def get_hostgroup(request):
    pending = Host.objects.filter(active=True, approved=False)
    allhosts = Host.objects.filter(approved=True).order_by('active', 'name')
    context = {"pending": pending, "allhosts": allhosts}
    return render(request, "admin/hosts.html", context=context)