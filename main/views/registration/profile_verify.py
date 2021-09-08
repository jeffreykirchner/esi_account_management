
import logging
import json

from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.utils.decorators import method_decorator

#user account info
class ProfileVerify(TemplateView):
    '''
    verify profile class view
    '''
    template_name = 'registration/profile_verify.html'

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        '''
        handle post requests
        '''
        data = json.loads(request.body.decode('utf-8'))

        if data["action"] == "verifyEmail":
            return verifyEmail(request,data)        

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
def verifyEmail(request, data):
    logger = logging.getLogger(__name__)
    logger.info("Verify email")
    logger.info(data)

    emailVerified = True
    failed=False
    try:

        u=request.user                
        u.is_active=True
        u.profile.email_confirmed="yes"
        u.profile.paused=False
        u.profile.save()
        u.save()    

        status="done"            
    except ObjectDoesNotExist:
        print("Failed to validate email")
        emailVerified = False
        failed = False

    return JsonResponse({'emailVerified':emailVerified,
                         'failed':failed,}, safe=False)