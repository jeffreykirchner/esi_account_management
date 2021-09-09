
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.shortcuts import render

def email_confirmed(function):
    def wrap(request, *args, **kwargs):       
        if request.user.profile.email_confirmed=="yes":
            return function(request, *args, **kwargs)
        else:
            #email not verified redirect to verifiction resend          

            return render(request, 'registration/verify_account_resend.html',{})
    return wrap

def in_debug_mode(function):
    def wrap(request, *args, **kwargs):       
        if settings.DEBUG==True:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ 