'''
experiment model
'''

from django.db import models
import main

#gloabal parameters for site
class Experiments(models.Model):
    manager = models.OneToOneField("main.profile", on_delete=models.SET_NULL, null=True, blank=True, related_name='experiments_a')  #user who manages the experiment

    name =  models.CharField(max_length = 1000, default = "*** New Experiment **", unique=True)            #name of the experiment
    url =  models.URLField(max_length = 200, default = "https://www.google.com")              #URL of the experiment
    available_to_all = models.BooleanField(default=False)                                     #allow all users access 
    disabled = models.BooleanField(default=False)                                             #disable the experiment
    
    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Experiment'
        verbose_name_plural = 'Experiments'
        ordering = ['name']

    def json(self):
        '''
        return json representation of the experiment
        '''

        profiles = self.profiles_a.values('pk','user__first_name', 'user__last_name', 'user__email')

        return {
            "id": self.id,
            "manager": self.manager.pk if self.manager else None,
            "manager_json": self.manager.json() if self.manager else None,
            "name": self.name,
            "url": self.url,
            "available_to_all": 1 if self.available_to_all else 0,
            "disabled": 1 if self.disabled else 0,     
            "profiles": list(profiles),      
        }