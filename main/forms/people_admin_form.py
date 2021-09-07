from main.models.people import People
from django import forms
from main.models import People
from main.models import Experiments

class PeopleAdminForm(forms.ModelForm):   
    first_name = forms.CharField(label='First Name',
                                 widget=forms.TextInput(attrs={"size":"125"}))

    last_name = forms.CharField(label='Last Name',
                                 widget=forms.TextInput(attrs={"size":"125"}))

    email = forms.EmailField(label='Email Address',
                                widget=forms.TextInput(attrs={"size":"125"}))

    organization = forms.CharField(label='Organization',
                                 widget=forms.TextInput(attrs={"size":"125"}))    

    # user_name = forms.CharField(label='User Name',
    #                              widget=forms.TextInput(attrs={'readonly':'readonly'}))   

    experiments = forms.ModelMultipleChoiceField(label="Grant Access",
                                                 required=False,
                                                 queryset=Experiments.objects.all().order_by("name"),
                                                 widget = forms.CheckboxSelectMultiple(attrs={}))                                                                                                                                                                                                                                                           

    class Meta:
        model=People   
        exclude=['password','user_name']