from django.db import models

class Post(models.Model):
    name = models.CharField(blank=True, max_length=100)
    content = models.TextField(blank=True)
    
    class Meta:
        app_label = "search_widget"