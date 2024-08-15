from django.db import models
from django.utils import timezone


class Host(models.Model):
    monit_id = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=50, blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    last_checkin = models.DateTimeField(default=timezone.now)
    monit_version = models.CharField(max_length=30, blank=True, null=True)
    uptime = models.IntegerField(blank=True, null=True)
    os_name = models.CharField(max_length=30, blank=True, null=True)
    os_release = models.CharField(max_length=35, blank=True, null=True)
    os_version = models.CharField(max_length=40, blank=True, null=True)
    os_arch = models.CharField(max_length=15, blank=True, null=True)
    cpu = models.IntegerField(blank=True, null=True)
    mem = models.IntegerField(blank=True, null=True)
    swap = models.IntegerField(blank=True, null=True)
    cycle = models.IntegerField(blank=True, null=True)  # polling cycle in seconds
    active = models.BooleanField(default=True)
    approved = models.BooleanField(default=False)
    ignore = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        constraints = [models.UniqueConstraint(fields=["monit_id"], name="unique_monit_id")]


class HostGroup(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    description = models.CharField(max_length=100, blank=True, null=True)
    host = models.ManyToManyField(Host, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        constraints = [models.UniqueConstraint(fields=["name"], name="unique_hostgroup_name")]

# class Alert(models.Model):
#     agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name="agent", blank=False, null=False, primary_key=False)
#     service = models.CharField(blank=True, null=True, default="")


class Service(models.Model):
    name = models.CharField(max_length=40, blank=False, null=False, default="", db_index=True)
    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name="service")
    status = models.IntegerField(blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    svc_type = models.IntegerField(blank=True, null=True)
    monitor = models.IntegerField(blank=True, null=True)
    event = models.CharField(max_length=300, blank=True, null=True)
    data = models.JSONField(blank=True, null=True)
    last_checkin = models.DateTimeField(default=timezone.now)
    ack = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["name", "host"], name="unique_svc_name")]

    def __unicode__(self):
        return self.name


# class NotificationSetting(models.Model):
#     tier = models.IntegerField(blank=True, null=True) # 4 tiers of notification
#     # 1st tier = default notification setting
#     # 2nd tier = per host group
#     # 3rd tier = per host
#     # 4th tier = per service

class Connector(models.Model):
    name = models.CharField(max_length=40, blank=False, null=False, db_index=True)
    active = models.BooleanField(default=False) 
    class Meta:
        abstract = True 
#        constraints = [models.UniqueConstraint(fields=["name"], name="unique_connector_name")]

class SlackConnector(Connector):
    webhook = models.CharField(max_length=500, blank=False, null=False)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["name"], name="unique_slack_connector_name")]

class EmailConnector(Connector):
    smtp_server = models.CharField(max_length=50, blank=False, null=False)
    smtp_port = models.IntegerField()
    class Meta:
        constraints = [models.UniqueConstraint(fields=["name"], name="unique_email_connector_name")]



# class SlackConnector
#     connector = foreign key to COnnnector
#     webhook url =
#     channel_id =

# class EmailConnector
#     connector = FK to connector
#     from_address
