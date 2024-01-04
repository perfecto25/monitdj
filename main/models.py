from django.db import models


class Agent(models.Model):
    monit_id = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=30, blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    last_checkin = models.DateTimeField(auto_now=True)
    monit_version = models.CharField(max_length=30, blank=True, null=True)
    uptime = models.IntegerField(blank=True, null=True)
    os_name = models.CharField(max_length=30, blank=True, null=True)
    os_release = models.CharField(max_length=35, blank=True, null=True)
    os_version = models.CharField(max_length=40, blank=True, null=True)
    os_arch = models.CharField(max_length=15, blank=True, null=True)
    cpu = models.IntegerField(blank=True, null=True)
    mem = models.IntegerField(blank=True, null=True)
    swap = models.IntegerField(blank=True, null=True)
    cycle = models.IntegerField(blank=True, null=True) # polling cycle in seconds
    

    def __unicode__(self):
       return self.name
    class Meta: 
        constraints = [models.UniqueConstraint(fields=["name"], name="unique_agent_name")]

# class Alert(models.Model):
#     agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name="agent", blank=False, null=False, primary_key=False)
#     service = models.CharField(blank=True, null=True, default="")

class Service(models.Model):
    name = models.CharField(max_length=40, blank=False, null=False, default="", db_index=True)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name="service")
    status = models.IntegerField(blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    svc_type = models.IntegerField(blank=True, null=True)
    monitor = models.IntegerField(blank=True, null=True)
    event = models.CharField(max_length=300, blank=True, null=True)
    data = models.JSONField(blank=True, null=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["name", "agent"], name="unique_svc_name")]

    def __unicode__(self):
       return self.name

class Ack(models.Model):
    service = models.OneToOneField(Service, on_delete=models.CASCADE, blank=True, null=True, related_name="service_object", db_index=True)
    state = models.BooleanField(default=False) 
    last_modified = models.DateTimeField(auto_now=True)
