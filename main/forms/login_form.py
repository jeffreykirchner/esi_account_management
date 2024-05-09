from django import forms

#form
class LoginForm(forms.Form):

    username =  forms.EmailField(label='Email address (lower case)',
                                 widget=forms.TextInput(attrs={"v-on:keyup.enter":"login",
                                                               "v-model":"username"}))

    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={"v-on:keyup.enter":"login",
                                                                 "v-model":"password"}))               
