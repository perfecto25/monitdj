from loguru import logger
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
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
    """ return all Host Groups """
    host_groups = HostGroup.objects.all().order_by('name')
    context = {"host_groups": host_groups}
    return render(request, "admin/hostgroups.html", context=context)


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
    

def hostgroup_delete(request):
    if request.method == "POST":
        try:
            hgid = dictor(request.POST, "id", checknone=True)
            hg = HostGroup.objects.filter(pk=hgid)
            name = hg[0].name
            hg.delete()
            messages.success(request, f"HostGroup {name} Deleted.")
        except Exception as ex:
            messages.error(request, f"HostGroup {name} - error deleting: {ex} ")
            logger.error(error)
        return redirect("hostgroup_get")

def hostgroup_edit(request, id):
    if request.method == "GET":
        
        obj = HostGroup.objects.get(pk=id)
        all_hosts = Host.objects.filter(approved=True)
        hosts_in_group = list(obj.host.values_list("monit_id", flat=True))
        logger.error(hosts_in_group)

        form = HostGroupForm(instance=obj)
        logger.debug(hosts_in_group)
        #logger.success(form.fields["host"])
        for host in all_hosts:
            logger.debug(host.monit_id)
        context = { "form": form, "id": id, "hosts_in_group": hosts_in_group, "obj": obj, "all_hosts": all_hosts }
        return render(request, "admin/hostgroup_edit.html", context=context)
    
    if request.method == "POST":
        obj = HostGroup.objects.get(pk=id)
        form = HostGroupForm(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save(commit=True)
            obj.host.set(request.POST.getlist("host"))
            #for h in request.POST.getlist('host'):
            #    logger.warning(h)
            #    obj.host.add(h)
            #form.save_m2m()
            
            for item in form:
                logger.debug(item)

            logger.debug(obj)
            messages.success(request, "modified")
        else:
            messages.error(request, form.errors)

    
        return redirect("hostgroup_get")