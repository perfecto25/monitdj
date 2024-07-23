from django.contrib import admin

from .models import Host, HostGroup


@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    list_display = ("name", "monit_id")
    # def show_email(self, obj):
    #    return obj.user.email
    # result = User.objects.filter(application=obj)n
    # return result.objects.values('email')


@admin.register(HostGroup)
class HostGroupAdmin(admin.ModelAdmin):
    pass
#    list_display = ("name", "host", "description")
