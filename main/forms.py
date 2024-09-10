from django import forms
from .models import HostGroup, Host, SlackConnector
from loguru import logger


class HostGroupForm(forms.ModelForm):
    class Meta:
        model = HostGroup
        fields = "__all__"

    name = forms.CharField(max_length=40, required=True)
    description = forms.CharField(max_length=50, required=False)
    host = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple())

    def __init__(self, *args, **kwargs):
        super(HostGroupForm, self).__init__(*args, **kwargs)
        self.fields['host'].choices = [(host.monit_id, host.name) for host in Host.objects.filter(approved=True)]


class SlackConnectorForm(forms.ModelForm):
    class Meta:
        model = SlackConnector
        fields = {"name", "webhook", "active"}
