
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect

from main.views import VerifyAccountResend

def email_confirmed(function):
    def wrap(request, *args, **kwargs):       
        if request.user.profile.email_confirmed=="yes":
            return function(request, *args, **kwargs)
        else:
            #email not verified redirect to verifiction resend          

            #return render(request, 'registration/verify_account_resend.html',{})
            return HttpResponseRedirect('/verify-account-resend/')
    return wrap

def in_debug_mode(function):
    def wrap(request, *args, **kwargs):       
        if settings.DEBUG==True:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ 