from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    zipcode = models.CharField(max_length=5, db_index=True)
    county = models.CharField(max_length=100, db_index=True)
    st = models.CharField(max_length=2, db_index=True)
    state = models.CharField(max_length=50)
    lon = models.CharField(max_length=50)
    lat = models.CharField(max_length=50)
    recruit = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s, %s' % (self.name, self.st)