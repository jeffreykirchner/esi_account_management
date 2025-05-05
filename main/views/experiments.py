'''
experiments view
'''
import logging
import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from main.decorators import email_confirmed

from main.models import Parameters
from main.models.experiments import Experiments

from main.views import HelpDocsMixin

class ExperimentsView(HelpDocsMixin, TemplateView):
    '''
    experiments class view
    '''
    template_name = 'experiments.html'

    @method_decorator(login_required)
    @method_decorator(email_confirmed)
    def post(self, request, *args, **kwargs):
        '''
        handle post requests
        '''
        data = json.loads(request.body.decode('utf-8'))

        #valid action not found        
        return JsonResponse({"status" :  "error"}, safe=False)

    @method_decorator(login_required)
    @method_decorator(email_confirmed)
    def get(self, request, *args, **kwargs):
        '''
        handle get requests
        '''

        parameters = Parameters.objects.first()

        #if user is superuser, show all experiments
        if request.user.is_superuser:
            user_experiments = Experiments.objects.all().order_by('name')
        else:
            #if user is not superuser, show only experiments that are available to all or owned by the user
            user_experiments = request.user.profile.experiments.filter(disabled=False).order_by('name')

        return render(request, self.template_name, {'help_text' : self.get_help_text('/experiments/'),
                                                    'contact_email':parameters.contact_email,
                                                    'experiments': user_experiments})

