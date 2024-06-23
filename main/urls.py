from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from main.views import general, admin
from main.api import api

urlpatterns = [

    path("", general.index, name="index"),
    path("index2/", general.index2, name="index2"),
    path("api/", api.urls),
    path("dashboard/", general.dashboard, name="dashboard"),

    path("ack/service/<int:svc_id>/", general.ack_service, name="ack_service"),
    path("host/detail/<uuid:monit_id>/", general.host_detail, name="host_detail"),
    path("main/admin/hosts/", admin.get_hosts, name="get_hosts"),   
    path("main/admin/host/action/", admin.host_action, name="host_action"),
#    path("main/admin/hostgroup/", admin.get_hostgroups, name="get_hostgroups"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
