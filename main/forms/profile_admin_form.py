
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

    mfa_required = forms.BooleanField(label='Multi-factor Required',
                                      required=False)

    mfa_setup_complete = forms.BooleanField(label='Multi-factor Setup Complete',
                                            required=False)

    mfa_hash = forms.CharField(label='Multi-factor Hash',
                               widget=forms.TextInput(attrs={"size":"125"}))

    disabled = forms.BooleanField(label='Disabled',
                                  required=False)


    class Meta:
        model=Profile   
        exclude=['global_id', 'user', 'password_reset_key']