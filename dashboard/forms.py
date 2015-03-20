from django.forms import HiddenInput, ModelForm
from monitor.models import BuzzartUpdate
from django.contrib.admin import widgets



class UpdateForm(ModelForm):
     class Meta:
         model = BuzzartUpdate
         fields = ['update', 'title', 'posted', 'fa_class','project']
         widgets = {
            'project': HiddenInput(),
         }

