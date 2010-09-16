from django.contrib import admin
from django.utils.dateformat import DateFormat

from models import EventType, Event, Guest
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
    list_display = ("name", "_when", "city", "state", "hosts", "commitment_cards_entered", "is_private",)
    list_filter = ("event_type", "location",)
    date_hierarchy = "when"
    readonly_fields = ("limit",)
    form = EventAdminForm
    
    def name(self, obj):
        return obj.place_name or obj.__unicode__()
    
    def _when(self, obj):
        return DateFormat(obj.start_datetime()).format("M j Y @ g:ia")
    _when.short_description = "When"
    
    def city(self, obj):
        return obj.location.name
        
    def state(self, obj):
        return obj.location.st
        
    def commitment_cards_entered(self, obj):
        return Guest.objects.distinct().filter(event=obj, commitment__isnull=False).count()
    
    def hosts(self, obj):
        return ", ".join([u.get_full_name() for u in obj.hosts()])
    hosts.short_description = "Hosts"

admin.site.register(EventType)
admin.site.register(Event, EventAdmin)