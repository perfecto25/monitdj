from django import forms 
from .models import HostGroup, Host
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
    
   
       # If an instance is provided, set the initial values for the host field
    #    if 'instance' in kwargs:
    #        logger.warning(kwargs["instance"])
   
                
            #self.fields['host'].initial = [host.monit_id for host in kwargs['instance'].host.all()]
   #         logger.debug(self.fields['host'].initial)

    
    # def save(self, commit=True):
    #     hostgroup = super().save()
    #     if commit:
    #         hostgroup.save()
    #         self.save_m2m()
    #     return hostgroup