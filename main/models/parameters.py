'''
site wide parameters
'''
#import logging
#import traceback

from django.db import models

#gloabal parameters for site
class Parameters(models.Model):
    '''
    site wide parameters
    '''
    contact_email =  models.CharField(max_length=1000, default="JohnSmith@abc.edu")        #contact email 
    site_URL = models.CharField(max_length=200, default="https://www.google.com")          #site URL used for display in emails

    password_reset_text_subject = models.CharField(max_length=1000, default="")             #email subject text when password reset
    password_reset_text = models.CharField(max_length=10000, default="")                    #email text sent when password reset

    email_verification_text_subject = models.CharField(max_length=1000, default="")         #email subject sent to user to verify their email address
    email_verification_text = models.CharField(max_length=10000, default="")                #email text sent to user to verify their email address

    timestamp = models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Site Parameters"

    class Meta:
        verbose_name = 'Site Parameters'
        verbose_name_plural = 'Site Parameters'