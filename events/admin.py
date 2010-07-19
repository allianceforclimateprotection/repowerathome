from django.contrib import admin

from models import EventType, Event

class EventAdmin(admin.ModelAdmin):
    list_display = ("__unicode__", "place_name", "start_datetime", "is_private")
    readonly_fields = ("limit",)

admin.site.register(EventType)
admin.site.register(Event, EventAdmin)