'''
create account functionality
'''
import json
import logging

from django.contrib.auth import logout
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.db.models import CharField, F, Value

from main.models import HelpDocs
from main.forms import CreateAccountForm


class CreateAccountView(TemplateView):
    '''
    create account class view
    '''
    template_name = 'registration/account_create.html'

    def post(self, request, *args, **kwargs):
        '''
        handle post requests
        '''
        data = json.loads(request.body.decode('utf-8'))

        if data["action"] == "create":
            return create_account(request, data)

        return JsonResponse({"response" :  "error"}, safe=False)

    def get(self, request, *args, **kwargs):
        '''
        handle get requests
        '''
        logout(request)
        
        form = CreateAccountForm()

        #logger.info(reverse('profile'))
        try:
            helpText = HelpDocs.objects.annotate(rp = Value(request.path, output_field=CharField()))\
                                       .filter(rp__icontains = F('path')).first().text

        except Exception  as e:   
            helpText = "No help doc was found."

        form_ids=[]
        for i in form:
            form_ids.append(i.html_name)

        return render(request, self.template_name ,{'form': form,
                                                    'helpText':helpText,
                                                    'form_ids':form_ids})

def create_account(request, data):
    '''
    create a new account
    '''
