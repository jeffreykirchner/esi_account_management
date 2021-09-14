'''
auth view
'''
import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

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
        
        status = "success"
        message = "access granted"
        profile = {}

        app_name = request.data['app_name']
        username = request.data['username']
        password = request.data['password']

        logger.info(f"Get Auth: {app_name}, {request.user}")

        experiments = Experiments.objects.filter(name=str(app_name))
        user = authenticate(request, username=username.lower(), password=password)

        logger.info(f"Get Auth experiments found: {experiments}")

        if experiments.count() != 1:
            status = "fail"
            message = "experiment not found"
        else:
            experiment = experiments.first()
        
        if status == "success":
            if not user:
                status = "fail"
                message = "user not found"
        
        if status == "success":
            if experiment in user.profile.experiments.all():
                profile = user.profile.json()
            else:
                status = "fail"
                message = "permission denied"

        return Response({"status" : status,
                         "message" : message,
                         "profile" : profile})