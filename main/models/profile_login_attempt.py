
from django.db import models

from main.models import Profile

#profile login attempts
class ProfileLoginAttempt(models.Model):
    my_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile_login_attempts")    #profile that note is attached to
    
    success = models.BooleanField(verbose_name="Login Success", default=False)                                  #was the login successful
    note = models.TextField(verbose_name="Note", blank=True, null=True)                                         #note about the login attempt

    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.timestamp}'

    class Meta:
        
        verbose_name = 'Profile Login Attempt'
        verbose_name_plural = 'Profile Login Attempts'
        ordering = ['-timestamp']
    
    def json(self):
        return {
            "id" : self.id,
            "success" : self.trait.success,
            "note" : self.note,
            "timestamp" : self.timestamp,
            "updated" : self.updated,
        }
        

