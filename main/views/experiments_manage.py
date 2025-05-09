'''
experiments manage view
'''
import logging
import json
import re

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django import forms

from main.decorators import email_confirmed
from main.decorators import is_manager

from main.models import Parameters
from main.models import Experiments
from main.models import Profile

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
    @method_decorator(is_manager)
    def post(self, request, *args, **kwargs):
        '''
        handle post requests
        '''
        experiment = self.get_object()

        data = json.loads(request.body.decode('utf-8'))

        experiment = self.get_object()

        data = json.loads(request.body.decode('utf-8'))         
        
        if data["status"] == "get":
            # get experiment data
            return JsonResponse({"experiment" :  experiment.json(),
                                 }, safe=False)
        elif data["status"] == "update":
            # update experiment data
            form_data_dict = data["form_data"]

            form = ExperimentForm(form_data_dict,instance=experiment)
            if form.is_valid():
                e = form.save()
                return JsonResponse({"experiment" : e.json(),"status":"success"}, safe=False)
            else:
                return JsonResponse({"status":"fail","errors":dict(form.errors.items())}, safe=False)
        elif data["status"] == "remove_collaborator":
            # remove collaborator from experiment
            collaborator_id = data["collaborator_id"]
            experiment.profiles_a.remove(collaborator_id)
            return JsonResponse({"experiment" : experiment.json(),"status":"success"}, safe=False)
        elif data["status"] == "add_collaborators":
            # add collaborators to experiment

            status = "success"
            raw_list = data["csv_data"]

            raw_list = raw_list.splitlines()

            for i in range(len(raw_list)):
                raw_list[i] = re.split(r',|\t', raw_list[i])
            
            email_list = []

            for i in raw_list:
                for j in i:
                    if "@" in j:
                        email_list.append(j)
                    elif j == "":
                        pass
                    else:
                        status = "fail"
                        error_message = f"Invalid email address: {j}"

            if status == "success":
                u_list = []
                for i in email_list:
                    try:
                        u = User.objects.get(email=i)
                        u_list.append(u.id)
                    except ObjectDoesNotExist:
                        status = "fail"
                        error_message = f"User not found: {i}"
                        break

                if status == "success":
                    experiment.profiles_a.add(*u_list)                   

                    return JsonResponse({"experiment" : experiment.json(),"status":"success"}, safe=False)

        if status == "fail":
            return JsonResponse({"error_message" : error_message,"status":"fail"}, safe=False)
            

    @method_decorator(login_required)
    @method_decorator(email_confirmed)    
    @method_decorator(is_manager)    
    def get(self, request, *args, **kwargs):
        '''
        handle get requests
        '''

        parameters = Parameters.objects.first()
        # experiment = self.get_object()

        edit_experiment_form = ExperimentForm()

        return render(request, self.template_name, {'help_text' : self.get_help_text('/experiments-manage/'),
                                                    'contact_email':parameters.contact_email,
                                                    'edit_experiment_form': edit_experiment_form,
                                                    })

