'''
people model
'''
import uuid

from django.db import models
from django.conf import settings

from django.dispatch import receiver
from django.db.models.signals import post_delete

#gloabal parameters for site
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    # first_name =  models.CharField(max_length = 1000, default = "Adam")                  #first name
    # last_name =  models.CharField(max_length = 1000, default = "Smith")                  #last name
    # email = models.EmailField(max_length = 254, default = "Adam_Smith@chapman.edu", unique=True)      #email address
    organization = models.CharField(max_length = 1000, default = "Chapman University")   #organization

    profile_id = models.UUIDField(default=uuid.uuid4, unique=True)
    #password = models.CharField(max_length = 1000, default = "Super Secret")             #password

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