from django.db import models
from tinymce.models import HTMLField

#Help Documentation
class HelpDocs(models.Model):
    title = models.CharField(verbose_name = 'Title',max_length = 300,default="")
    path = models.CharField(verbose_name = 'URL Path',max_length = 300,default="/")
    text = HTMLField(verbose_name = 'Help Doc Text', max_length = 100000, default="")

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    class Meta:
        verbose_name = 'Help Doc'
        verbose_name_plural = 'Help Docs'

    def __str__(self):
        return self.title + " " + self.path
    
    def json(self) -> dict:
        return{
            "id":self.id,
            "title":self.title,
            "path":self.path,
            "text":self.text,
        }