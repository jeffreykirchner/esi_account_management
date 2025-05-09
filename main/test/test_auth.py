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
from django.test import Client

import main

from main.views import take_create_account
from main.views import update_profile

class TestAuth(TestCase):
    sys._called_from_test = True
    fixtures = ['Parameters.json']

    def setUp(self):
        logger = logging.getLogger(__name__)

    def test_create_account(self):
        '''
        test create account
        '''
        logger = logging.getLogger(__name__)

        request = RequestFactory().get('/create-account/')
        middleware = SessionMiddleware(get_response=request)
        middleware.process_request(request)
        request.session.save()
        request.user = AnonymousUser()

        #password
        data = {'action': 'create', 'form_data': {'first_name': 'John', 'last_name': 'smith', 'email': 'abc@123.edu', 'organization': 'College Tech', 'password1': 'qwerty123', 'password2': 'qwerty123'}}

        result = json.loads(take_create_account(request, data).content.decode("UTF-8"))
        self.assertEqual(result['errors']['password1'][0], 'This password is too common.')

        #name and org not present
        data = {'action': 'create', 'form_data': {'first_name': '', 'last_name': '', 'email': '', 'organization': '', 'password1': '', 'password2': ''}}

        result =  json.loads(take_create_account(request, data).content.decode("UTF-8"))
        logger.info(result)
        self.assertEqual(result['errors']['first_name'][0], 'This field is required.')
        self.assertEqual(result['errors']['last_name'][0], 'This field is required.')
        self.assertEqual(result['errors']['email'][0], 'This field is required.')
        self.assertEqual(result['errors']['organization'][0], 'This field is required.')
        self.assertEqual(result['errors']['password1'][0], 'This field is required.')
        self.assertEqual(result['errors']['password2'][0], 'This field is required.')

        #success
        data = {'action': 'create', 'form_data': {'first_name': 'John', 'last_name': 'smith', 'email': 'abc@123.edu', 'organization': 'College Tech', 'password1': 'qwerty112233', 'password2': 'qwerty112233'}}

        result =  json.loads(take_create_account(request, data).content.decode("UTF-8"))
        #logger.info(result)
        self.assertEqual(result['status'], 'success')

        #double email fail
        data = {'action': 'create', 'form_data': {'first_name': 'John', 'last_name': 'smith', 'email': 'abc@123.edu', 'organization': 'College Tech', 'password1': 'qwerty112233', 'password2': 'qwerty112233'}}

        result =  json.loads(take_create_account(request, data).content.decode("UTF-8"))
        logger.info(result)
        self.assertEqual(result['errors']['email'][0], 'Email "abc@123.edu" is already in use.')

    def test_edit_account(self):
        '''
        test editing account information
        '''
        logger = logging.getLogger(__name__)

        self.factory = RequestFactory()
        request = self.factory.get('/create-account/')
        middleware = SessionMiddleware(get_response=request)
        middleware.process_request(request)
        request.session.save()
        request.user = AnonymousUser()

        data = {'action': 'create', 'form_data': {'first_name': 'John', 'last_name': 'Smith', 'email': 'abc@123.edu', 'organization': 'College Tech', 'password1': 'qwerty112233', 'password2': 'qwerty112233'}}
        # c = Client()
        # response = c.post('/create-account/', data)

        result = json.loads(take_create_account(request, data).content.decode("UTF-8"))
        #logger.info(result)
        self.assertEqual(result['status'], 'success')

        user = User.objects.all().first()

        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Smith')
        self.assertEqual(user.email, 'abc@123.edu')
        self.assertEqual(user.profile.organization, 'College Tech')
        self.assertNotEqual(user.profile.email_confirmed, 'yes')

        user.profile.email_confirmed = 'yes'
        user.save()

        #check update, no email change
        data = {'action': 'update', 'form_data': {'first_name': 'Adam', 'last_name': 'Joe', 'email': 'abc@123.edu', 'organization': 'Chapman University', 'password1': '', 'password2': ''}}
        result = json.loads(update_profile(user, data).content.decode("UTF-8"))
        self.assertEqual(result['status'], 'success')

        user = User.objects.all().first()
        self.assertEqual(user.first_name, 'Adam')
        self.assertEqual(user.last_name, 'Joe')
        self.assertEqual(user.email, 'abc@123.edu')
        self.assertEqual(user.profile.organization, 'Chapman University')
        self.assertEqual(user.profile.email_confirmed, 'yes')

        #check update, with email change
        data = {'action': 'update', 'form_data': {'first_name': 'Adam', 'last_name': 'Joe', 'email': 'abc@chapman.edu', 'organization': 'Chapman University', 'password1': '', 'password2': ''}}
        result = json.loads(update_profile(user, data).content.decode("UTF-8"))
        self.assertEqual(result['status'], 'success')

        user = User.objects.all().first()
        self.assertEqual(user.first_name, 'Adam')
        self.assertEqual(user.last_name, 'Joe')
        self.assertEqual(user.email, 'abc@chapman.edu')
        self.assertEqual(user.profile.organization, 'Chapman University')
        self.assertNotEqual(user.profile.email_confirmed, 'yes')

        #check password change
        data = {'action': 'update', 'form_data': {'first_name': 'Adam', 'last_name': 'Joe', 'email': 'abc@chapman.edu', 'organization': 'Chapman University', 'password1': 'qwerty11223344', 'password2': 'qwerty11223344'}}
        result = json.loads(update_profile(user, data).content.decode("UTF-8"))
        self.assertEqual(result['status'], 'success')

        user = User.objects.all().first()
        self.assertEqual(user.first_name, 'Adam')
        self.assertEqual(user.last_name, 'Joe')
        self.assertEqual(user.email, 'abc@chapman.edu')
        self.assertEqual(user.profile.organization, 'Chapman University')
        self.assertNotEqual(user.profile.email_confirmed, 'yes')
        self.assertTrue(check_password('qwerty11223344', user.password))

        #check valid email address
        data = {'action': 'update', 'form_data': {'first_name': 'Adam', 'last_name': 'Joe', 'email': 'abc@chapman', 'organization': 'Chapman University', 'password1': '', 'password2': ''}}
        result = json.loads(update_profile(user, data).content.decode("UTF-8"))
        #logger.info(result)
        self.assertEqual(result['errors']['email'][0], 'Enter a valid email address.')

        #check valid password
        data = {'action': 'update', 'form_data': {'first_name': 'Adam', 'last_name': 'Joe', 'email': 'abc@chapman.edu', 'organization': 'Chapman University', 'password1': 'asdfqwert123', 'password2': 'asdfqwert1234'}}
        result = json.loads(update_profile(user, data).content.decode("UTF-8"))
        logger.info(result)
        self.assertEqual(result['errors']['password1'][0], 'Passwords are not the same')


        








        

        
    
    