'''
create account functionality
'''
import json
import logging

from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.db.models import CharField, F, Value

from main.models import Parameters
from main.models import HelpDocs
from main.forms import LoginForm


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

        if data["action"] == "login":
            return login_function(request,data)

        return JsonResponse({"response" :  "error"},safe=False)

    def get(self, request, *args, **kwargs):
        '''
        handle get requests
        '''
        logout(request)
        
        form = None

        #logger.info(reverse('profile'))
        try:
            helpText = HelpDocs.objects.annotate(rp = Value(request.path, output_field=CharField()))\
                                        .filter(rp__icontains = F('path')).first().text

        except Exception  as e:   
            helpText = "No help doc was found."

        form_ids=[]
        for i in form:
            form_ids.append(i.html_name)

        return render(request, 'registration/profileCreate.html',{'form': form,
                                                                  'helpText':helpText,
                                                                  'form_ids':form_ids})

def login_function(request,data):
    '''
    handle login
    '''
    logger = logging.getLogger(__name__)
    #logger.info(data)

    #convert form into dictionary
    form_data_dict = {}

    for field in data["formData"]:
        form_data_dict[field["name"]] = field["value"]

    form = LoginForm(form_data_dict)

    if form.is_valid():

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        #logger.info(f"Login user {username}")

        user = authenticate(request, username=username.lower(), password=password)

        if user is not None:
            login(request, user)

            redirect_path = request.session.get('redirect_path','/')

            logger.info(f"Login user {username} success , redirect {redirect_path}")

            return JsonResponse({"status":"success", "redirect_path" : redirect_path}, safe=False)
        else:
            logger.warning(f"Login user {username} fail user / pass")

            return JsonResponse({"status" : "error"}, safe=False)
    else:
        logger.info("Login user form validation error")
        return JsonResponse({"status":"validation", "errors":dict(form.errors.items())}, safe=False)
