'''
experiment model
'''

from django.db import models

#gloabal parameters for site
class Experiments(models.Model):

    name =  models.CharField(max_length = 1000, default = "*** New Experiment **", unique=True)            #name of the experiment
    url =  models.URLField(max_length = 200, default = "https://www.google.com")              #URL of the experiment
    available_to_all = models.BooleanField(default=False)                                     #allow all users access 
    
    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Experiment'
        verbose_name_plural = 'Experiments'
        ordering = ['name']