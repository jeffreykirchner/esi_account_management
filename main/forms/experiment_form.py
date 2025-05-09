

from django import forms

from main.models import Experiments
from main.models import Profile


class ExperimentForm(forms.ModelForm):   
    '''
    edit experiment parameters
    '''

    manager = forms.ModelChoiceField(label="Manager",
                                     queryset=Profile.objects.all(),
                                     empty_label=None,
                                     widget=forms.Select(attrs={"v-model":"experiment.manager"}))

    name = forms.CharField(label='Title',
                           widget=forms.TextInput(attrs={"v-model":"experiment.name", }))
                                                        
    
    url = forms.CharField(label='URL',
                          widget=forms.TextInput(attrs={"v-model":"experiment.url",
                                                        "placeholder":"https://www.example.com"}))

    available_to_all = forms.ChoiceField(label='Available to All',
                                         choices=((1, 'Yes'), (0, 'No')),
                                         widget=forms.Select(attrs={"v-model":"experiment.available_to_all",}))
    
    disabled = forms.ChoiceField(label='Disabled',
                                 choices=((1, 'Yes'), (0, 'No')),
                                 widget=forms.Select(attrs={"v-model":"experiment.disabled",}))
    
    class Meta:
        model=Experiments
        fields = ['name', 'manager', 'url', 'available_to_all', 'disabled']

