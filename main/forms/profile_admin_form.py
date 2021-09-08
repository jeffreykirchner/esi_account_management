
from django import forms

from main.models import Profile
from main.models import Experiments

class ProfileAdminForm(forms.ModelForm):   

    organization = forms.CharField(label='Organization',
                                   widget=forms.TextInput(attrs={"size":"125"}))    

    email_confirmed = forms.CharField(label='Email Confirmed (no/code/yes)',
                                      widget=forms.TextInput(attrs={"size":"125"}))

    experiments = forms.ModelMultipleChoiceField(label="Grant Access",
                                                 required=False,
                                                 queryset=Experiments.objects.all().order_by("name"),
                                                 widget = forms.CheckboxSelectMultiple(attrs={}))                                                                                                                                                                                                                                                           

    class Meta:
        model=Profile   
        exclude=['global_id','user']