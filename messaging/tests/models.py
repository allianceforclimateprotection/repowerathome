from django.db import models

class User(models.Model):
    email = models.EmailField()
    
    class Meta:
        app_label = "messaging"

class Event(models.Model):
    content = models.TextField(blank=True)
    creator = models.ForeignKey(User, related_name="creator")
    guests = models.ManyToManyField(User, related_name="guests")
    
    def host_email(self):
        return self.creator.email
        
    def emails(self):
        return [self.creator.email] + [g.email for g in self.guests.all()]
        
    def attendees(self):
        return [self.creator] + list(self.guests.all())
    
    class Meta:
        app_label = "messaging"
