
'''
send email via ESI mass email service
'''
from smtplib import SMTPException

import logging
import requests
import sys

from django.utils.crypto import get_random_string
from django.conf import settings

from main.models import profile, parameters

def send_mass_email_verify(profile_list, request):
    '''
    send mass deactivation email to current active subjects
    '''
    logger = logging.getLogger(__name__)
    logger.info(f"Send mass verification email to list: {profile_list}")

    params = parameters.objects.first()

    if len(profile_list) == 0:
        return {"mailCount":0, "errorMessage":"No valid users"}

    for prfl in profile_list:
        prfl.email_confirmed = get_random_string(length=32)
    
    profile.objects.bulk_update(profile_list, ['email_confirmed'])

    user_list = []

    for prfl in profile_list:     
        user_list.append({"email" : prfl.user.email,
                          "variables": [{"name" : "activation link", "text" : f'{params.siteURL}/profileVerify/{prfl.email_confirmed}'},
                                        {"name" : "first name", "text" : prfl.user.first_name},
                                        {"name" : "contact email", "text" : params.labManager.email}]})
            
    memo = 'Bulk account deactivation'

    try:
        return send_mass_email_service(user_list, params.deactivationTextSubject, params.deactivationText, memo)             
    except SMTPException as exc:
        logger.info(f'There was an error sending email: {exc}') 
        return {"mail_count":0, "error_message":str(exc)}

#send email when profile is created or changed
def profile_create_send_email(user):
    logger = logging.getLogger(__name__) 
    logger.info(f"Verify Email: {user.profile}")

    params = parameters.objects.first()

    user.profile.email_confirmed = get_random_string(length=32)   
    user.profile.save()

    user_list = []
    user_list.append({"email" : user.email,
                      "variables": [{"name" : "activation link", "text" : f'{params.siteURL}/profileVerify/{user.profile.email_confirmed}'},
                                    {"name" : "first name", "text" : user.first_name},
                                    {"name" : "contact email", "text" : params.labManager.email}]})

    memo = f'Verfiy email address for user {user.id}'

    try:
        return send_mass_email_service(user_list, params.emailVerificationTextSubject, params.emailVerificationResetText, memo)             
    except SMTPException as exc:
        logger.info(f'There was an error sending email: {exc}') 
        return {"mail_count":0, "error_message":str(exc)}

def send_mass_email_service(user_list, message_subject, message_text, memo):
    '''
    send mass email through ESI mass pay service
    returns : {mail_count:int, error_message:str}

    :param user_list: List of users to email [{email:email, variables:[{name:""},{text:""}}, ]
    :type user_list: List

    :param message_subject : string subject header of message
    :type message_subject

    :param message_text : message template, variables : [first name]
    :type message_text: string 
    
    :param memo : note about message's purpose
    :type memo: string 

    :param unit_testing : if true do not send email, return expected result
    :type unit_testing: bool

    '''
    logger = logging.getLogger(__name__)

    if hasattr(sys, '_called_from_test'):
        logger.info(f"ESI mass email API: Unit Test")
        return {"mail_count":len(user_list), "error_message":""}

    data = {"user_list" : user_list,
            "message_subject" : message_subject,
            "message_text" : message_text,
            "memo" : memo}
    
    logger.info(f"ESI mass email API: users: {user_list}, message_subject : {message_subject}, message_text : {message_text}")

    headers = {'Content-Type' : 'application/json', 'Accept' : 'application/json'}

    request_result = requests.post(f'{settings.EMAIL_MS_HOST}/send-email/',
                                   json=data,
                                   auth=(str(settings.EMAIL_MS_USER_NAME), str(settings.EMAIL_MS_PASSWORD)),
                                   headers=headers)
    
    if request_result.status_code == 500:        
        logger.warning(f'send_mass_email_service error: {request_result}')
        return {"mail_count":0, "error_message":"Mail service error"}
   
    logger.info(f"ESI mass email API response: {request_result.json()}")
    return request_result.json()
