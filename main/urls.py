from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from .views import index, ack_service, test, agent_detail
from .api import api

urlpatterns = [
    ## AllAuth URLS here:  https://github.com/pennersr/django-allauth/blob/master/allauth/account/urls.py
  #  path("accounts/", include("allauth.urls")),
    #path("accounts/password/reset", TemplateView.as_view(template_name="account/password_reset.html"), name="password_reset"),


    #path("accounts/logout/user", views.logout_user, name="logout"),
    #path("accounts/signup/", TemplateView.as_view(template_name="account/signup.html"), name="register"),
    #path("accounts/email/", TemplateView.as_view(template_name="account/email.html"), name="email"),

    path("", index, name="index"),
    #path("collector", collector, name="collector"),
    path("api/", api.urls),
    path("ack_service/<int:svc_id>/", ack_service, name="ack_service"),
    path("agent_detail/<uuid:monit_id>/", agent_detail, name="agent_detail")
    #path("collector/", views.api.urls, name="collector")
#     path("home/", views.home, name="home"),
#     path("search/<str:target>/", views.search, name="search"),
#     path("search/<str:target>/<userid>/", views.search, name="search"),
#     path("application/", views.application, name="application"),
#     path("upload/", views.upload_photos,  name="upload_photos"),
#     path("view/<int:userid>/", views.view_application, name="view"),
#     path("view_matches/<int:userid>/", views.view_matches, name="view_matches"),
#     path("edit/<int:userid>/", views.edit_application, name="edit"),
#     #path("search/match/<int:userid>/", views.search_match, name="search_match"),
#     path("create/match/<int:userid>/<int:matchid>", views.create_match, name="create_match"),
#     path("delete/match/<int:matchid>", views.delete_match, name="delete_match"),
#     path("update/match/", views.update_match, name="update_match"),
#     path("action/<int:userid>/<str:action>", views.action_application, name="action"),
#     path("media/<path:path>", serve_media, name="serve_media"),
#     path("events/show/", views.show_events, name="show_events"),
#     path("mm/show/events/", views.mm_show_events, name="mm_show_events"),
#     path("mm/update/events/<int:event_id>", views.update_event, name="update_event"),
#     path("mm/delete/events/<int:event_id>", views.delete_event, name="delete_event"),
#     path("mm/create/events/", views.create_event, name="create_event"),
#     path("mm/create/applicant/", views.mm_create_applicant, name="mm_create_applicant"),
#     path("mm/email/applicants/", views.mm_email_applicants, name="mm_email_applicants"),
#     path("contact/", views.contact, name="contact"),

#     path("email/mm/", views.email_mm, name="email_mm"),
#    # path("applicant/view/<int:pk>", views.ViewApplicant.as_view(), name="view_applicant")

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)