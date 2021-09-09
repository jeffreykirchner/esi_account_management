'''
experiments view
'''
import logging
import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.db.models import CharField, F, Value
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from main.decorators import email_confirmed
from main.models import help_docs

class ExperimentsView(TemplateView):
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

        try:
            helpText = help_docs.objects.annotate(rp = Value(request.path, output_field=CharField()))\
                                        .filter(rp__icontains=F('path')).first().text

        except Exception  as e:
            helpText = "No help doc was found."

        return render(request, self.template_name, {'helpText': helpText})

