from loguru import logger
from main.models import Service, Host
from main.utils import show_queryset, show_object, bytesto


def hosts(request):
    pending = Host.objects.filter(active=True, approved=False)
    allhosts = Host.objects.filter(approved=True)
    context = {"pending": pending, "allhosts": allhosts}
    return render(request, "admin/hosts.html", context=context)