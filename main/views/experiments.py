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

        if data["status"] == "get":
            if request.user.is_superuser:
                user_experiments = Experiments.objects.all().order_by('name')
                managed_experiments = Experiments.objects.all().values_list('id', flat=True)
            else:
                #get experiments that are available to user
                valid_experiments = request.user.profile.experiments.filter(disabled=False).values_list('id', flat=True)

                #available to all experiments
                valid_experiments = valid_experiments | Experiments.objects.filter(available_to_all=True).values_list('id', flat=True)

                #get experiments that users is a manager of
                managed_experiments = Experiments.objects.filter(manager=request.user.profile).values_list('id', flat=True)

                valid_experiments = valid_experiments | managed_experiments

                user_experiments = Experiments.objects.filter(id__in=valid_experiments).order_by('name')

            return JsonResponse({"experiments" : [experiment.json() for experiment in user_experiments],
                                 "managed_experiments" : list(managed_experiments)},
                                status=200,
                                safe=False)
        elif data["status"] == "add":
            if request.user.is_superuser:
                # get experiment data
                experiment_name = f'*** New Experiment *** {len(Experiments.objects.all()) + 1}'
                experiment = Experiments.objects.create(name=experiment_name)
                user_experiments = Experiments.objects.all().order_by('name')
                managed_experiments = Experiments.objects.all().values_list('id', flat=True)

                return JsonResponse({"experiments" : [experiment.json() for experiment in user_experiments],
                                    "managed_experiments" : list(managed_experiments)},
                            status=200,
                            safe=False)
        elif data["status"] == "delete":
            if request.user.is_superuser:
                # delete experiment
                experiment = Experiments.objects.get(id=data["experiment_id"])
                experiment.delete()
                user_experiments = Experiments.objects.all().order_by('name')
                managed_experiments = Experiments.objects.all().values_list('id', flat=True)

                return JsonResponse({"experiments" : [experiment.json() for experiment in user_experiments],
                                    "managed_experiments" : list(managed_experiments)},
                            status=200,
                            safe=False)

        #valid action not found
        return JsonResponse({"status" :  "error"}, status=400, safe=False)

    @method_decorator(login_required)
    @method_decorator(email_confirmed)
    def get(self, request, *args, **kwargs):
        '''
        handle get requests
        '''

        parameters = Parameters.objects.first()

        # #if user is superuser, show all experiments
        # if request.user.is_superuser:
        #     user_experiments = Experiments.objects.all().order_by('name')
        # else:
        #     #if user is not superuser, show only experiments that are available to all or owned by the user
        #     user_experiments_ids = request.user.profile.experiments.filter(disabled=False).values_list('id', flat=True)
        #     user_experiments_ids = user_experiments_ids | Experiments.objects.filter(available_to_all=True).values_list('id', flat=True)
        #     user_experiments = Experiments.objects.filter(id__in=user_experiments_ids).order_by('name')

        return render(request, self.template_name, {'help_text' : self.get_help_text('/experiments/'),
                                                    'contact_email':parameters.contact_email,
                                                    })

