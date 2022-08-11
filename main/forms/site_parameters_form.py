from tinymce.widgets import TinyMCE

from django import forms

from main.models import Parameters

class ParametersAdminForm(forms.ModelForm):   

    contact_email = forms.CharField(label='Contact Email',
                                   widget=forms.TextInput(attrs={"size":"125"}))    

    site_URL = forms.CharField(label='Site URL',
                               widget=forms.TextInput(attrs={"size":"125"}))

    email_verification_text_subject = forms.CharField(label='Verification email, subject',
                                                      widget=forms.TextInput(attrs={"size":"125"}))
    
    email_verification_text = forms.CharField(label='Verification email, body',
                                               widget=TinyMCE(attrs={"rows":10, "cols":200, "plugins": "link image code"}))

    password_reset_text_subject = forms.CharField(label='Password reset email, subject',
                                                  widget=forms.TextInput(attrs={"size":"125"}))
    
    password_reset_text = forms.CharField(label='Password reset email, body',
                                           widget=TinyMCE(attrs={"rows":10, "cols":200, "plugins": "link image code"}))
                                                                                                                                                                                                                                                     
    class Meta:
        model=Parameters   
        exclude=[]