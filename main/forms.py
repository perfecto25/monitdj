from django import forms 
from .models import HostGroup, Host


class HostGroupForm(forms.ModelForm):
    name = forms.CharField(max_length=40, required=True)
    description = forms.CharField(max_length=50, required=False)
    host = forms.MultipleChoiceField(
        required=False, widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = HostGroup
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(HostGroupForm, self).__init__(*args, **kwargs)
        choices = []
        for i in Host.objects.all():
            choices.append((i.monit_id, i.name))
        self.fields["host"].choices = (x.monit_id,x.name) for x in Host.objects.all() #choices