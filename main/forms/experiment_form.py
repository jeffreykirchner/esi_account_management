

from django import forms

from main.models import Experiments


class ExperimentForm(forms.ModelForm):   
    '''
    edit experiment parameters
    '''

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
        fields = ['name', 'url', 'available_to_all', 'disabled']

