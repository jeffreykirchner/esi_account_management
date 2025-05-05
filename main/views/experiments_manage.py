'''
experiments manage view
'''
import logging
import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from django import forms

from main.decorators import email_confirmed

from main.models import Parameters
from main.models.experiments import Experiments

from main.views import HelpDocsMixin

from main.forms import ExperimentForm

class ExperimentsManageView(SingleObjectMixin, HelpDocsMixin, View):
    '''
    experiments manage class view
    '''
    template_name = 'experiments_manage.html'
    model = Experiments

    @method_decorator(login_required)
    @method_decorator(email_confirmed)
    def post(self, request, *args, **kwargs):
        '''
        handle post requests
        '''
        experiment = self.get_object()

        data = json.loads(request.body.decode('utf-8'))

        experiment = self.get_object()

        data = json.loads(request.body.decode('utf-8'))         
        
        if data["status"] == "get":
            return JsonResponse({"experiment" :  experiment.json(),
                                 }, safe=False)
        elif data["status"] == "update":
            form_data_dict = data["formData"]

            form = ExperimentForm(form_data_dict,instance=experiment)
            if form.is_valid():
                e = form.save()
                return JsonResponse({"experiment" : e.json(),"status":"success"}, safe=False)
            else:
                return JsonResponse({"status":"fail","errors":dict(form.errors.items())}, safe=False)
            

    @method_decorator(login_required)
    @method_decorator(email_confirmed)
    def get(self, request, *args, **kwargs):
        '''
        handle get requests
        '''

        parameters = Parameters.objects.first()
        # experiment = self.get_object()

        edit_experiment_form = ExperimentForm()

        return render(request, self.template_name, {'help_text' : self.get_help_text('/experiments/'),
                                                    'contact_email':parameters.contact_email,
                                                    'edit_experiment_form': edit_experiment_form,
                                                    })

