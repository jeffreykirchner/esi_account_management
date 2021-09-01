'''
people model
'''

from django.db import models
import uuid

#gloabal parameters for site
class People(models.Model):

    first_name =  models.CharField(max_length = 1000, default = "Adam")                  #first name
    last_name =  models.CharField(max_length = 1000, default = "Smith")                  #last name
    email = models.EmailField(max_length = 254, default = "Adam_Smith@chapman.edu", unique=True)      #email address
    organization = models.CharField(max_length = 1000, default = "Chapman University")   #organization

    user_name = models.UUIDField(default=uuid.uuid4, unique=True)
    password = models.CharField(max_length = 1000, default = "Super Secret")             #password

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name} "

    class Meta:
        verbose_name = 'People'
        verbose_name_plural = 'People'