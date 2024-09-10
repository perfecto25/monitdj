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
    path("main/admin/hostgroup/get", admin.hostgroup_get, name="hostgroup_get"),
    path("main/admin/hostgroup/create", admin.hostgroup_create, name="hostgroup_create"),
    path("main/admin/hostgroup/delete/<int:id>", admin.hostgroup_delete, name="hostgroup_delete"),
    path("main/admin/hostgroup/edit/<int:id>/", admin.hostgroup_edit, name="hostgroup_edit"),
    path("main/admin/notification/connector/get", admin.connector_get, name="connector_get"),
    path("main/admin/notification/connector/create/<str:connector_type>/", admin.connector_create, name="connector_create"),
    path("main/admin/notification/connector/edit/<int:id>/", admin.connector_edit, name="connector_edit"),
    path("main/admin/notification/connector/delete/<int:id>/", admin.connector_delete, name="connector_delete"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
