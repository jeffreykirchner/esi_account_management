
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound

from main.views import VerifyAccountResend
from main.models import Experiments

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
    wrap.__name__ = function.__name__
    return wrap

def is_manager(function):
    def wrap(request, *args, **kwargs):   
        try:
            experiment = Experiments.objects.get(id=kwargs['pk'])    
        except Experiments.DoesNotExist:
            return HttpResponseNotFound("Error: Experiment not found.")
        
        #allow if super user or manager
        if request.user.is_superuser or experiment.manager == request.user.profile:
            return function(request, *args, **kwargs)
        
        return HttpResponseNotFound("Error: You are not the manager.")

    return wrap
   