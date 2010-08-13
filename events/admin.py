from django.contrib import admin

from models import EventType, Event
from forms import EventForm

class EventAdminForm(EventForm):
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        if self.instance.location:
            self.fields["city"].initial = self.instance.location.name
            self.fields["state"].initial = self.instance.location.st
            self.fields["zipcode"].initial = self.instance.location.zipcode
            
    def save(self, *args, **kwargs):
        self.instance.location = self.cleaned_data["location"]
        return super(EventForm, self).save(*args, **kwargs)

class EventAdmin(admin.ModelAdmin):
    list_display = ("__unicode__", "place_name", "start_datetime", "is_private")
    readonly_fields = ("limit",)
    form = EventAdminForm

admin.site.register(EventType)
admin.site.register(Event, EventAdmin)