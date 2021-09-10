'''
auth view
'''
import logging
from django.db.models.query import RawQuerySet

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from main.models import Experiments

class GetAuthView(APIView):
    '''
    get authorization view
    '''
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, app_name):
        '''
        take get request
        '''
        logger = logging.getLogger(__name__)
        logger.info(f"Get Auth: {app_name}, {request.user}")

        status = "success"
                        
        experiments = Experiments.objects.filter(name=str(app_name))

        logger.info(f"Get Auth experiments found: {experiments}")

        if experiments.count() != 1:
            status = "fail"

        return Response({"status" : status})