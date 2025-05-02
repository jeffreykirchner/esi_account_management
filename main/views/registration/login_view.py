'''
log in user functionality
'''
import json
import logging
import pyotp

from datetime import timedelta

from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.utils import timezone

from main.models import Parameters
from main.models import FrontPageNotice
from main.models import ProfileLoginAttempt

from main.forms import LoginForm

from main.views import HelpDocsMixin

class LoginView(HelpDocsMixin, TemplateView):
    '''
    log in class view
    '''

    template_name = 'registration/login.html'

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

        request.session['redirect_path'] = request.GET.get('next','/')

        parameters = Parameters.objects.first()

        form = LoginForm()

        form_ids=[]
        for i in form:
            form_ids.append(i.html_name)

        fpn_list = FrontPageNotice.objects.filter(enabled = True)

        return render(request, self.template_name, {"contact_email":parameters.contact_email,
                                                    "help_text" : self.get_help_text(request.path),
                                                    "form":form,
                                                    "fpn_list":fpn_list,
                                                    "form_ids":form_ids})

def login_function(request,data):
    logger = logging.getLogger(__name__) 
    #logger.info(data)

    #convert form into dictionary
    form_data_dict = data["formData"]           

    # for field in data["formData"]:            
    #     form_data_dict[field["name"]] = field["value"]
    
    f = LoginForm(form_data_dict)

    if f.is_valid():

        username = f.cleaned_data['username']
        password = f.cleaned_data['password']
        two_factor = data["two_factor_code"]

        #check rate limit
        user_rl = User.objects.filter(username=username.lower()).first()
        if user_rl:
            failed_login_attempts = user_rl.profile.profile_login_attempts.filter(success=False, timestamp__gte=timezone.now()-timedelta(minutes=1)).count()

            if failed_login_attempts > 5:
                return JsonResponse({"status":"error", "message":"Login failed, try again later."}, safe=False)

        #authenticate user
        user = authenticate(request, username=username.lower(), password=password)

        if user is not None:

            if not user.is_active or user.profile.disabled:
                ProfileLoginAttempt.objects.create(my_profile=user.profile, success=False, note="Inactive Account")
                logger.error(f"Login user {username} inactive account.")                
                return JsonResponse({"status":"error", "message":"Your account is not active. Contact us for more information."}, safe=False)
            
            #check if two factor code required
            if user.profile.mfa_required and two_factor == "":
                if not user.profile.mfa_setup_complete:
                    
                    if user.profile.mfa_hash == "" or user.profile.mfa_hash == None:
                        #user has not setup two factor code
                        user.profile.mfa_hash = pyotp.random_base32()
                        user.profile.save()

                    two_factor_uri = pyotp.totp.TOTP(user.profile.mfa_hash).provisioning_uri(user.username,issuer_name="ESI Recruiter")
                    return JsonResponse({"status":"two_factor_setup", 
                                            "message":"Two factor setup required.",
                                            "two_factor_uri":two_factor_uri,
                                            "two_factor_hash":user.profile.mfa_hash}, safe=False)
                else:    
                    #if user has two factor code enabled, return two factor code required
                    return JsonResponse({"status":"two_factor", "message":"Two factor code required."}, safe=False)
                
            #check two factor code if required
            elif user.profile.mfa_required and two_factor != "":
                totp = pyotp.TOTP(user.profile.mfa_hash)

                if not totp.verify(two_factor, valid_window=1):
                    ProfileLoginAttempt.objects.create(my_profile=user.profile, success=False, note="Invalid Two Factor Code")
                    return JsonResponse({"status":"error", "message":"Invalid Code"}, safe=False)
                else:
                    if user.profile.mfa_setup_complete == False:
                        user.profile.mfa_setup_complete = True
                        user.profile.save()

            #standard user, no two factor code required
            login(request, user) 
            ProfileLoginAttempt.objects.create(my_profile=user.profile, success=True)

            rp = request.session.get('redirect_path','/')        

            logger.info(f"Login user {username} success , redirect {rp}")

            return JsonResponse({"status":"success","redirect_path":rp}, safe=False)
        else:
            logger.warning(f"Login user {username} fail user / pass")
            user = User.objects.filter(username=username.lower()).first()
            if user:
                ProfileLoginAttempt.objects.create(my_profile=user.profile, success=False, note="Invalid Password")

            return JsonResponse({"status":"error", "message":"Username or Password is incorrect."}, safe=False)
    else:
        logger.info(f"Login user form validation error")
        return JsonResponse({"status":"validation","errors":dict(f.errors.items())}, safe=False)
