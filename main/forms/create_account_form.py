'''
create account form
'''
from django import forms
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User

import logging

class CreateAccountForm(forms.Form):
    '''
    create account form
    '''
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    email = forms.EmailField(label='Email Address')
    organization = forms.CharField(label='Organization', max_length=100)

    password1 = forms.CharField(label='Password',widget=forms.PasswordInput())
    password2 = forms.CharField(label='Repeat Password',widget=forms.PasswordInput())

    #check that passwords match
    def clean_password1(self):    
        logger = logging.getLogger(__name__) 
        logger.info("Clean Password1")

        password1 = self.data['password1']

        if password1 != self.data['password2']:
            raise forms.ValidationError('Passwords are not the same')
        
        if validate_password(password1):
            raise forms.ValidationError('Password Error')

        return password1
    
    #check that username/email not already in use
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError(u'Email "%s" is already in use.' % email)
        return email