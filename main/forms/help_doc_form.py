from django import forms
from main.models import HelpDocs


class HelpDocForm(forms.ModelForm):


    title = forms.CharField(label='Title',
                                         widget=forms.TextInput(attrs={"size":"125"}))
    
    path = forms.CharField(label='URL Path',
                                         widget=forms.TextInput(attrs={"size":"125"}))

    text = forms.CharField(label='Text',
                                     widget=forms.Textarea(attrs={"rows":"30", "cols":"125"}))


    class Meta:
        model=HelpDocs
        fields = ('__all__')