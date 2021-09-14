'''
auth view
'''
import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status as response_status

from django.contrib.auth import authenticate

from main.models import Experiments

class GetAuthView(APIView):
    '''
    get authorization view
    '''
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        '''
        take get request
        '''
        logger = logging.getLogger(__name__)

        #check that user is authenticated
        if not request.user.is_authenticated:
            return Response({"status" : "fail",
                             "message" : "user not authenticated",
                             "profile" : {}}, status=response_status.HTTP_403_FORBIDDEN)
        
        status = "success"
        message = "access granted"
        profile = {}
        return_response_status = response_status.HTTP_200_OK

        app_name = request.data['app_name']
        username = request.data['username']
        password = request.data['password']

        logger.info(f"Get Auth: {app_name}, {request.user}")

        experiments = Experiments.objects.filter(name=str(app_name))
        user = authenticate(request, username=username.lower(), password=password)

        logger.info(f"Get Auth experiments found: {experiments}")

        #check experiment exists
        if experiments.count() != 1:
            status = "fail"
            message = "experiment not found"
        else:
            experiment = experiments.first()
        
        #check that user exists
        if status == "success":
            if not user:
                status = "fail"
                message = "user not found"
        
        #check that user email verified
        if status == "success":
            if user.profile.email_confirmed != 'yes':
                status = "fail"
                message = "email not verified"
        
        #check that user has permissions for experiment
        if status == "success":
            if experiment in user.profile.experiments.all():
                profile = user.profile.json()
            else:
                status = "fail"
                message = "permission denied"

        logger.info(f"Get Auth Result: status {status}, message {message}")

        return Response({"status" : status,
                         "message" : message,
                         "profile" : profile}
                         , status=return_response_status)