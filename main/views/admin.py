from loguru import logger
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from main.models import Service, Host, HostGroup
from main.forms import HostGroupForm
from main.utils import show_queryset, show_object, bytesto
from asgiref.sync import sync_to_async
from dictor import dictor


def get_hosts(request):
    pending = Host.objects.filter(active=True, approved=False)
    allhosts = Host.objects.filter(approved=True).order_by('active', 'name')
    context = {"pending": pending, "allhosts": allhosts}
    return render(request, "admin/hosts.html", context=context)


@sync_to_async
def host_action(request):
    """ approve/delete/ignore a host """
    if request.method == "POST":
        logger.debug(request.POST)
        action = dictor(request.POST, "action")
        monit_id = dictor(request.POST, "monit_id")
        logger.warning(monit_id)

        if action == "approve":
            logger.info(f"approving host ID: {monit_id}")
            host = Host.objects.filter(pk=monit_id)
            host.update(approved=1)

        if action == "delete":
            logger.info(f"deleting host ID: {monit_id}")
            Host.objects.filter(pk=monit_id).delete()
            if dictor(request.POST, "source") == "htmx":
                return HttpResponse("deleted")

        if action == "ignore":
            logger.info(f"ignoring host ID: {monit_id}")
            host = Host.objects.get(pk=monit_id)

            if host.ignore == 1:
                host.ignore = 0
                msg = "Ignore Host"
                warning = "<span id='warning-result'></span>"
                color = "outline-info"
            else:
                host.ignore = 1
                msg = "Monitor Host"
                color = "info"
                warning = "<span id='warning-result'><span class='badge text-bg-info'>Ignored</span></span>"
            host.save()

            resp = f"""
                {warning}
                <button
                id='btn-ignore'
                class='btn btn-{color} btn-sm' 
                hx-post="/main/admin/host/action/"
                hx-vals='{{\"action\": \"ignore\", \"source\": \"htmx\", \"monit_id\": "{monit_id}" }}'
                hx-swap="multi:#warning-result,#btn-ignore:outerHTML">
                {msg}
                </button>
                """
            return HttpResponse(resp)

        if action == "monitor":
            logger.info(f"monitoring host ID: {monit_id}")
            Host.objects.filter(pk=monit_id).update(ignore=0)
        return redirect("get_hosts")


def hostgroup_get(request):
    host_groups = HostGroup.objects.all().order_by('name')
 #   pending = Host.objects.filter(active=True, approved=False)
 #   allhosts = Host.objects.filter(approved=True).order_by('active', 'name')
    context = {"host_groups": host_groups}
    return render(request, "admin/hostgroups.html", context=context)


def hostgroup_create(request):
    if request.method == "GET":
        form = HostGroupForm()
        context = {"form": form}

    if request.method == "POST":
        form = HostGroupForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context = {"message": "Group created"}
        else:
            for key, error in list(form.errors.items()):
                logger.error(key)
                logger.error(error)
            context= {"message" : "error"}
    return render(request, "admin/hostgroup_new.html", context)

def hostgroup_delete(request):
    if request.method == "POST":
        return HttpResponse("deleted")

def hostgroup_edit(request, id):
    if request.method == "GET":
        logger.info(id)
        obj = HostGroup.objects.get(pk=id)
        form = HostGroupForm(instance=obj)
        context = { "form": form, "id": id }
        return render(request, "admin/hostgroup_edit.html", context=context)