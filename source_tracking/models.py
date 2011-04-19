from django.db import models

class UserSource(models.Model):
     user = models.ForeignKey("auth.User", unique=True, db_index=True)
     source = models.CharField(max_length=100, blank=True, db_index=True)
     subsource = models.CharField(max_length=100, blank=True, db_index=True)
     referrer = models.CharField(max_length=255, blank=True)
     created = models.DateTimeField(auto_now_add=True)
     updated = models.DateTimeField(auto_now=True)