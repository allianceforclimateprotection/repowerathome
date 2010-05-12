from django.db import models

class Post(models.Model):
    content = models.TextField(blank=True)
    
    class Meta:
        app_label = "invite"