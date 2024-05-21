from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from main.views import general, admin
from main.api import api

urlpatterns = [

    path("", general.index, name="index"),
    path("api/", api.urls),
    path("dashboard/", general.dashboard, name="dashboard"),

    path("ack/service/<int:svc_id>/", general.ack_service, name="ack_service"),
    path("host/detail/<uuid:monit_id>/", general.host_detail, name="host_detail"),
    path("host/delete/<uuid:monit_id>/", general.host_delete, name="host_delete"),
    path("admin/hosts/", admin.hosts, name="admin_hosts")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
