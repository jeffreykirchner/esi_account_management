
import json
import logging
import uuid

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import logout
from django.views.generic import TemplateView
from django.contrib.auth.hashers import make_password

from main.models import Parameters
from main.models import Profile
from main.forms import PasswordResetChangeForm
from main.globals import send_mass_email_service

from main.views import HelpDocsMixin

class PasswordResetChangeView(HelpDocsMixin, TemplateView):
    '''
    password reset change class view
    '''
    template_name = 'registration/password_reset_change.html'

    def post(self, request, *args, **kwargs):
        '''
        handle post requests
        '''
        data = json.loads(request.body.decode('utf-8'))
        token = kwargs['token']

        if data["action"] == "change_password":
            return change_password(request, data, token)

        return JsonResponse({"response" :  "error"}, safe=False)

    def get(self, request, *args, **kwargs):
        '''
        handle get requests
        '''

        logout(request)        

        token = kwargs['token']

        form = PasswordResetChangeForm()

        parameters = Parameters.objects.first()

        form_ids=[]
        for i in form:
            form_ids.append(i.html_name)

        #check that code is valid
        valid_code_profile = check_valid_code(token)

        return render(request,self.template_name,{"form":form,
                                                  "token":token,
                                                  "help_text" : self.get_help_text(request.path),
                                                  "contact_email":'asdf',
                                                  "valid_code":False if not valid_code_profile else True,
                                                  "form_ids":form_ids})
    
def check_valid_code(token):
    logger = logging.getLogger(__name__) 

    try:
        p = Profile.objects.filter(password_reset_key=token)

        if p.count() != 1:
            logger.warning(f"Password reset failed for {token}, count: {p.count()}")
            return None
        else:
            return p.first()
    except:
        logger.warning(f"Password reset invalid code format {token}")
        return None


def change_password(request, data, token):
    logger = logging.getLogger(__name__) 
   
    # p = Parameters.objects.first()

    #convert form into dictionary
    form_data_dict = {}             

    for field in data["formData"]:            
        form_data_dict[field["name"]] = field["value"]
    
    f = PasswordResetChangeForm(form_data_dict)

    if f.is_valid():
        
        p = check_valid_code(token)

        if not p:
            return JsonResponse({"status":"error","message":"Valid code not found."}, safe=False)
        else:
            p.user.password = make_password(f.cleaned_data['password1'])
            p.user.is_active = True

            p.password_reset_key = uuid.uuid4()
            p.email_confirmed = 'yes'
            p.save()
            p.user.save()

            logger.info(f"Reset password for {p}")
        
            return JsonResponse({"status":"success"}, safe=False)
    else:
        logger.info(f"Reset password validation error")
        return JsonResponse({"status":"validation","errors":dict(f.errors.items())}, safe=False)