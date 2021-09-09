
import logging
import json

from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.utils.decorators import method_decorator

class VerifyAccount(TemplateView):
    '''
    verify account class view
    '''
    template_name = 'registration/verify_account.html'

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        '''
        handle post requests
        '''
        data = json.loads(request.body.decode('utf-8'))

        if data["action"] == "verifyEmail":
            return verify_email(request,data)        

        return JsonResponse({"status":"fail"}, safe=False)

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        '''
        handle get requests
        '''
        #check for correct token
        user = request.user
        failed = False
        token = kwargs['token']

        if token != user.profile.email_confirmed or user.profile.email_confirmed == 'no':
            failed=True

        #check that user is not already verified
        email_verified = True
        if user.profile.email_confirmed != 'yes':
            email_verified = False

        return render(request, self.template_name,{'emailVerified':email_verified,
                                                                  'failed':failed,    
                                                                  'token':token}) 

#verify user email address
def verify_email(request, data):
    logger = logging.getLogger(__name__)
    logger.info("Verify email")
    logger.info(data)

    email_verified = True
    failed = False

    try:
        u = request.user                
        u.is_active = True
        u.profile.email_confirmed = "yes"
        u.profile.save()
        u.save()    
         
    except ObjectDoesNotExist:
        print("Failed to validate email")
        email_verified = False
        failed = False

    return JsonResponse({'emailVerified':email_verified,
                         'failed':failed,}, safe=False)