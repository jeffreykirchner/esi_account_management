'''
auth view
'''
import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status as response_status
from rest_framework import generics
from rest_framework import serializers
from django.contrib.auth.models import User


from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

from django.contrib.auth import authenticate

from main.models import Experiments

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', "first_name", "last_name")

class UserList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer

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

        request_data = getattr(request, 'data', {}) or {}
        query_params = getattr(request, 'query_params', request.GET)

        try:
            app_name = query_params.get('app_name') if 'app_name' in query_params else request_data['app_name']
            username = query_params.get('username') if 'username' in query_params else request_data['username']
            password = query_params.get('password') if 'password' in query_params else request_data['password']
        except KeyError as e:
            logger.error(f"Get Auth KeyError: {e}")
            return Response({"status" : "fail",
                             "message" : "missing required parameters",
                             "profile" : {}}, status=response_status.HTTP_400_BAD_REQUEST)

        logger.info(f"Get Auth: {app_name}, {request.user}")

        # single-row lookup avoids separate count() and first() queries
        try:
            experiment = Experiments.objects.only('id', 'available_to_all', 'manager_id').get(name=str(app_name), disabled=False)
        except (Experiments.DoesNotExist, Experiments.MultipleObjectsReturned):
            status = "fail"
            message = "experiment not found"
        
        #check that user exists
        if status == "success":
            user = authenticate(request, username=username.lower(), password=password)
            if not user:
                status = "fail"
                message = "user not found"
        
        #check that user email verified
        if status == "success":
            user_profile = user.profile
            if user_profile.email_confirmed != 'yes':
                status = "fail"
                message = "email not verified"
        
        #check that user has permissions for experiment
        if status == "success":
            if experiment.available_to_all or \
               experiment.manager_id == user_profile.pk or \
               user_profile.experiments.filter(pk=experiment.pk).exists():
                
                profile = user_profile.json()
            else:
                status = "fail"
                message = "permission denied"

        logger.info(f"Get Auth Result: status - {status}, message - {message}")

        return Response({"status" : status,
                         "message" : message,
                         "profile" : profile}
                         , status=return_response_status)