from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import debug_toolbar

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path("__debug__/", include(debug_toolbar.urls))
]

urlpatterns += staticfiles_urlpatterns()
