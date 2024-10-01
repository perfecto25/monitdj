from loguru import logger
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from main.models import Service, Host, HostGroup, Connector
from main.forms import HostGroupForm, SlackConnectorForm
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


# HOSTGROUP

def hostgroup_get(request):
    """ return all Host Groups """
    host_groups = HostGroup.objects.all().prefetch_related("host").order_by('name')    
    context = {"host_groups": host_groups}
    return render(request, "admin/hostgroups.html", context=context)


def hostgroup_edit(request, id):
    if request.method == "GET":
        obj = HostGroup.objects.get(pk=id)
        all_hosts = Host.objects.filter(approved=True)
        hosts_in_group = list(obj.host.values_list("monit_id", flat=True))
        form = HostGroupForm(instance=obj)
        context = {"form": form, "id": id, "hosts_in_group": hosts_in_group, "obj": obj, "all_hosts": all_hosts}
        return render(request, "admin/hostgroup_edit.html", context=context)

    if request.method == "POST":
        obj = HostGroup.objects.get(pk=id)
        form = HostGroupForm(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save(commit=True)
            obj.host.set(request.POST.getlist("host"))
            messages.success(request, f"HostGroup {obj.name} modified")
        else:
            messages.error(request, form.errors)
        return redirect("hostgroup_get")


def hostgroup_create(request):
    """ create a new Host Group """
    if request.method == "GET":
        form = HostGroupForm()
        context = {"form": form}
        return render(request, "admin/hostgroup_new.html", context)

    if request.method == "POST":
        form = HostGroupForm(request.POST)
        logger.debug(form)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            messages.success(request, f"Host Group: {obj.name} created")
        else:
            messages.error(request, f"Host Group errors: {form.errors.items()}")
            for key, error in list(form.errors.items()):
                logger.error(key)
                logger.error(error)
        return redirect("hostgroup_get")


def hostgroup_delete(request, id):
    if request.method == "DELETE":
        try:
            hg = HostGroup.objects.filter(pk=id)
            name = hg[0].name
            hg.delete()
        except Exception as ex:
            logger.error(ex)
        return HttpResponse("")




# NOTIFICATIONS
def connector_get(request):
    """ return all Notification Connectors """
    connectors = Connector.objects.all()

#    slack_connectors = SlackConnector.objects.all().order_by('name')
#    email_connectors = EmailConnector.objects.all().order_by('name')
    context = {"connectors": connectors }
    return render(request, "admin/connectors.html", context=context)


def connector_create(request, ctype: str):
    """ create new notification connector """
    if request.method == "GET":

        logger.warning(type(request))
        if ctype == "slack":
            form = SlackConnectorForm()
        context = {"form": form, "ctype": ctype}
        return render(request, "admin/connector_new.html", context)

    if request.method == "POST":
        if ctype == "slack":
            form = SlackConnectorForm(request.POST)
        logger.debug(form)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            messages.success(request, f"Connector: {obj.name} created")
        else:
            messages.error(request, f"Connector create errors: {form.errors.items()}")
            for key, error in list(form.errors.items()):
                logger.error(key)
                logger.error(error)
        return redirect("connector_get")


def connector_edit(request, id):
    """ edits a given connector """

    if request.method == "GET":
#        ctype = request.GET.get("ctype", None)
#        if ctype == "slack":`
        obj = Connector.objects.get(pk=id)
        if obj.ctype == "slack":
            form = SlackConnectorForm(instance=obj)
        context = {"form": form, "id": id, "obj": obj}
        return render(request, "admin/connector_edit.html", context=context)

    if request.method == "POST":
        obj = Connector.objects.get(pk=id)
        if obj.ctype == "slack":
            form = SlackConnectorForm(request.POST, instance=obj)

        if form.is_valid():
            obj = form.save(commit=True)
            messages.success(request, f"Connector {obj.name} modified")
        else:
            messages.error(request, form.errors)
    return redirect("connector_get")


def connector_delete(request, id):
    if request.method == "POST":
        try:
            logger.debug("DELETE")
            obj = Connector.objects.filter(pk=id)
            name = obj[0].name
            obj.delete()
            messages.success(request, f"Connector {name} Deleted.")
        except Exception as ex:
            messages.error(request, f"Connector {name} - error deleting: {ex} ")
            logger.error(error)
        return redirect("connector_get")
