import logging
import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from main.globals import profile_create_send_email

from main.models import Parameters

from main.views import HelpDocsMixin

class VerifyAccountResend(HelpDocsMixin, TemplateView):
    '''
    verify account class view
    '''
    template_name = 'registration/verify_account_resend.html'

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        '''
        handle post requests
        '''
        data = json.loads(request.body.decode('utf-8'))

        if data["action"] == "getUser":
            return get_user(request, data)
        elif data["action"] == "sendVerificationEmail":
            return send_verification_email(request, data)

        return JsonResponse({"status":"fail"}, safe=False)

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        '''
        handle get requests
        '''
        parameters = Parameters.objects.first()

        #check for correct token
        return render(request, self.template_name, {'contact_email':parameters.contact_email,
                                                    'help_text' : self.get_help_text(request.path), })


#get user status
def get_user(request,data):
    logger = logging.getLogger(__name__)
    logger.info("Get user")
    logger.info(data)

    user=request.user
    logger.info(user)

    return JsonResponse({"emailVerified":False if user.profile.email_confirmed != "yes" else True}) 

#send verifiction email link to user
def send_verification_email(request, data):
    logger = logging.getLogger(__name__)

    user = request.user
    logger.info(f"Resend verification email: {data}, {user}")

    status = "success"

    try:
        result = profile_create_send_email(user)   
        status = "success"

        if result["mail_count"] == 0:
            status = "fail"
    except:
        status = "fail"

    return JsonResponse({"status":status}, safe=False)