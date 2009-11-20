from django.db import models

# Create your models here.
class Signup(models.Model):
    email = models.EmailField(max_length=255)
    zipcode = models.CharField(max_length=5)
        
    def __unicode__(self):
        return u'%s' % (self.email)

