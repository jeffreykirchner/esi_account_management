'''
people model
'''
import uuid

from django.db import models
from django.conf import settings

from django.dispatch import receiver
from django.db.models.signals import post_delete

from main.models.experiments import Experiments

#gloabal parameters for site
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    experiments = models.ManyToManyField(Experiments, related_name='profiles_a')

    organization = models.CharField(max_length = 1000, default = "Chapman University")   #organization
    global_id = models.UUIDField(default=uuid.uuid4, unique=True)                        #id used across all experiments
    email_confirmed =  models.CharField(verbose_name="Email Confirmed", max_length = 100, default="no")                #yes/code/no

    password_reset_key = models.UUIDField(verbose_name='Password Reset Key', null=True, blank=True)                     #log in key used to reset subject password

    mfa_hash = models.CharField(verbose_name="Multi-factor Hash", max_length = 50, null=True, blank=True)             #hash for multi-factor authentication
    mfa_required = models.BooleanField(verbose_name="Multi-factor Required", default=False)                           #true if multi-factor authentication is required
    mfa_setup_complete = models.BooleanField(verbose_name="Multi-factor Setup Complete", default=False)               #true if multi-factor authentication is setup

    disabled = models.BooleanField(verbose_name="Disabled", default=False)                                            #if true, user is disabled and cannot login

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return f"{self.user.last_name}, {self.user.first_name} "

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        ordering = ['user__last_name', 'user__first_name']
    
    def json(self):
        '''
        return json object of model
        '''

        return {'first_name' : self.user.first_name,
                'last_name' : self.user.last_name,
                'email' : self.user.email,
                'organization' : self.organization,
                'global_id' : self.global_id,
                }

#delete associated user model when profile is deleted
@receiver(post_delete, sender=Profile)
def post_delete_user(sender, instance, *args, **kwargs):
    if instance.user: # just in case user is not specified
        instance.user.delete()