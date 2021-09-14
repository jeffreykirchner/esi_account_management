'''
unit tests for session model
'''
from decimal import Decimal

import logging
import json
import sys

from unittest import main

from django.contrib.auth.models import AnonymousUser, User
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.hashers import check_password

from django.test import TestCase
from django.test import RequestFactory

import main

from main.views import take_create_account
from main.views import GetAuthView

from main.models import Experiments

class TestAPI(TestCase):
    sys._called_from_test = True
    fixtures = ['Parameters.json']

    def setUp(self):
        logger = logging.getLogger(__name__)

        self.user = User.objects.create_user(username='E1', email='adam@smith.edu', password='go_panthers')

        self.experiment_1 = Experiments(name="E1", available_to_all=True)
        self.experiment_1.save()

        self.experiment_2 = Experiments(name="E2", available_to_all=False)
        self.experiment_2.save()

    def test_request_access(self):
        '''
        test create account
        '''
        logger = logging.getLogger(__name__)

        request = RequestFactory().get('/create-account/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.user = AnonymousUser()

        #check that user has access to experiment 1 and not 2
        data = {'action': 'create', 'formData': [{'name': 'first_name', 'value': 'John'}, {'name': 'last_name', 'value': 'smith'}, {'name': 'email', 'value': 'abc@123.edu'}, {'name': 'organization', 'value': 'College Tech'}, {'name': 'password1', 'value': 'qwerty112233'}, {'name': 'password2', 'value': 'qwerty112233'}]}

        result = json.loads(take_create_account(request, data).content.decode("UTF-8"))
        self.assertEqual(result['status'], 'success')

        user = User.objects.get(first_name="John")
        user.profile.email_confirmed='yes'
        user.profile.save()

        self.assertIn(self.experiment_1, user.profile.experiments.all())
        self.assertNotIn(self.experiment_2, user.profile.experiments.all())

        #check that user can get api access to experiment 1
        request = RequestFactory().get('/get-auth/')
        request.user = user
        view = GetAuthView()
        view.setup(request)

        request.data={'app_name' : 'E1', 'username' : str(user.email), 'password' : 'qwerty112233'}

        result = view.get(request).data
        #logger.info(result)
        self.assertEqual("success", result['status'])

        #check no access experiment 2
        request.data={'app_name' : 'E2', 'username' : str(user.email), 'password' : 'qwerty112233'}
        result = view.get(request).data
        #logger.info(result)
        self.assertEqual("fail", result['status'])
        self.assertEqual("permission denied", result['message'])

        #check wrong user name
        request.data={'app_name' : 'E1', 'username' : str(user.email)+"a", 'password' : 'qwerty112233'}
        result = view.get(request).data
        #logger.info(result)
        self.assertEqual("fail", result['status'])
        self.assertEqual("user not found", result['message'])

        #check wrong password
        request.data={'app_name' : 'E1', 'username' : str(user.email), 'password' : 'qwerty1122334'}
        result = view.get(request).data
        #logger.info(result)
        self.assertEqual("fail", result['status'])
        self.assertEqual("user not found", result['message'])

        #email not confirmed
        user.profile.email_confirmed = 'no'
        user.profile.save()

        request.data={'app_name' : 'E1', 'username' : str(user.email), 'password' : 'qwerty112233'}
        result = view.get(request).data
        self.assertEqual("fail", result['status'])
        self.assertEqual("email not verified", result['message'])

        #no api credentials
        user.profile.email_confirmed = 'yes'
        user.profile.save()
        request = RequestFactory().get('/get-auth/')
        request.user = AnonymousUser()

        request.data={'app_name' : 'E1', 'username' : str(user.email), 'password' : 'qwerty112233'}
        result = view.get(request)
        logger.info(result)
        self.assertNotEqual(200, result.status_code)


        






        








        

        
    
    