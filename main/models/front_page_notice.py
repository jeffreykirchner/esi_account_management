from django.db import models
from tinymce.models import HTMLField

class FrontPageNotice(models.Model):
    '''
    notices shown on long in screen
    '''
    subject_text = models.CharField(verbose_name="Subject Text", max_length=1000, default="")   #text displayed in the header portion of the notification card
    body_text =  HTMLField(verbose_name = 'Body Text', max_length = 100000, default="")

    enabled = models.BooleanField(default=True)

    timestamp = models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.subject_text}'

    class Meta:
        
        verbose_name = 'Login Page Notice'
        verbose_name_plural = 'Login Page Notices'
    
    def json(self):
        return {
            "id" : self.id,
            "subject_text" : self.subject_text,
            "body_text" : self.body_text,
            "enabled" : self.enabled,
        }
        

