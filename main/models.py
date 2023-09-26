from django.db import models


class Agent(models.Model):
    monit_id = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=30, blank=True, null=True)
    def __unicode__(self):
       return self.name

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
        constraints = [models.UniqueConstraint(fields=["name", "agent"], name="unique_match")]

    def __unicode__(self):
       return self.name