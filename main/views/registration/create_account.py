'''
create account functionality
'''
import json
import logging
from main.models.experiments import Experiments

from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth import get_user_model

from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.db.models import CharField, F, Value

from main.models import HelpDocs
from main.models import Profile
from main.models import Parameters

from main.forms import CreateAccountForm

from main.globals import profile_create_send_email
from main.views import HelpDocsMixin

class CreateAccountView(HelpDocsMixin, TemplateView):
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
            return take_create_account(request, data)

        return JsonResponse({"response" :  "error"}, safe=False)

    def get(self, request, *args, **kwargs):
        '''
        handle get requests
        '''
        logout(request)
        
        form = CreateAccountForm()
        parameters = Parameters.objects.first()

        #logger.info(reverse('profile'))
        try:
            help_text = HelpDocs.objects.annotate(rp = Value(request.path, output_field=CharField()))\
                                       .filter(rp__icontains = F('path')).first().text

        except Exception  as e:   
            help_text = "No help doc was found."

        form_ids=[]
        for i in form:
            form_ids.append(i.html_name)

        return render(request, self.template_name ,{'form': form,
                                                    'contact_email':parameters.contact_email, 
                                                    'help_text' : self.get_help_text(request.path),
                                                    'form_ids':form_ids})

def take_create_account(request, data):
    '''
    take create a new account post
    '''

    logger = logging.getLogger(__name__) 
    logger.info(f"Create Account")

    form_data_dict = {}             

    for field in data["formData"]:            
        form_data_dict[field["name"]] = field["value"]

        #remove caps from email form
        if field["name"] == "email":
            form_data_dict["email"] = form_data_dict["email"].strip().lower()
    
    f = CreateAccountForm(form_data_dict)

    if f.is_valid():
        
        user = create_acocunt(f.cleaned_data['email'].strip().lower(),
                             f.cleaned_data['email'].strip().lower(),
                             f.cleaned_data['password1'],
                             f.cleaned_data['first_name'].strip().capitalize(),
                             f.cleaned_data['last_name'].strip().capitalize(),
                             f.cleaned_data['organization'].strip(),)

        #send email verification
        try:
            result = profile_create_send_email(user)   
            status = "success"

            if result["mail_count"] == 0:
                status = "fail"
        except:
            status = "fail"

        #log new user in
        #user = authenticate(request, username=u.username, password=u.password)
        login(request, user) 
         
        return JsonResponse({"status":status}, safe=False)

    else:
        logger.info(f"createUser validation error")
        return JsonResponse({"status":"error", "errors":dict(f.errors.items())}, safe=False)

def create_acocunt(email, user_name, password, first_name, last_name, organization):
    '''
    create new account
    '''

    logger = logging.getLogger(__name__) 

    #create new user
    user = get_user_model().objects.create_user(username=user_name,
                                                email=email,
                                                password=password,                                         
                                                first_name=first_name,
                                                last_name=last_name)

    user.save()

    #attach profile to user
    profile = Profile(user=user,
                      organization=organization)
    profile.save()
    
    # add default experiments to profile
    profile.experiments.set(Experiments.objects.filter(available_to_all=True))
    profile.save()    

    logger.info(f'Account created: {user}')

    return user