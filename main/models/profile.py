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
    experiments = models.ManyToManyField(Experiments)

    organization = models.CharField(max_length = 1000, default = "Chapman University")   #organization
    global_id = models.UUIDField(default=uuid.uuid4, unique=True)                        #id used across all experiments
    email_confirmed =  models.CharField(verbose_name="Email Confirmed", max_length = 100, default="no")                #yes/code/no

    password_reset_key = models.UUIDField(verbose_name='Password Reset Key', null=True, blank=True)                     #log in key used to reset subject password

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return f"{self.user.last_name}, {self.user.first_name} "

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

#delete associated user model when profile is deleted
@receiver(post_delete, sender=Profile)
def post_delete_user(sender, instance, *args, **kwargs):
    if instance.user: # just in case user is not specified
        instance.user.delete()