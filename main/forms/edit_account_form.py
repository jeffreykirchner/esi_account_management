'''
edit account form
'''
from django import forms
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User

class EditAccountForm(forms.Form):
    '''
    edit account form
    '''
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    email = forms.EmailField(label='Email Address (Verification required.)')
    organization = forms.CharField(label='Organization', max_length=100)

    password1 = forms.CharField(label='Password (Leave blank if no change.)',
                                widget=forms.PasswordInput(),
                                required=False)
    password2 = forms.CharField(label='Repeat Password',
                                widget=forms.PasswordInput(),
                                required=False)

    def __init__(self, *args, **kwargs):
         self.user = kwargs.pop('user', None)
         super(EditAccountForm, self).__init__(*args, **kwargs)

    def clean_first_name(self):
        #prevent url injection
        first_name = self.cleaned_data['first_name'].strip()
        if "." in first_name or first_name.startswith('http://') or first_name.startswith('https://'):
            raise forms.ValidationError('URLs are not allowed.')
        
        return first_name
    
    def clean_last_name(self):
        #prevent url injection
        last_name = self.cleaned_data['last_name'].strip()
        if "." in last_name or last_name.startswith('http://') or last_name.startswith('https://'):
            raise forms.ValidationError('URLs are not allowed.')
        
        return last_name
    
    def clean_organization(self):
        #prevent url injection
        organization = self.cleaned_data['organization'].strip()
        if "." in organization or organization.startswith('http://') or organization.startswith('https://'):
            raise forms.ValidationError('URLs are not allowed.')
        
        return organization

    #check that passwords match
    def clean_password1(self):
        if self.data['password1'] != "":        
            password1 = self.data['password1']

            if password1 != self.data['password2']:
                raise forms.ValidationError('Passwords are not the same')
            
            if validate_password(password1):
                raise forms.ValidationError('Password Error')

            return password1
        else:
            return ""
    
    #check that username/email not already in use
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(username=email).exclude(id=self.user.id).exists():
            raise forms.ValidationError(u'Email "%s" is already in use.' % email)
        return email