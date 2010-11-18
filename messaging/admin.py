import csv

from django.contrib import admin
from django.template import RequestContext
from django.shortcuts import render_to_response

from models import Message, ABTest, Stream

def preview_messages(modeladmin, request, queryset):
    previews = []
    for obj in queryset:
        for preview in obj.clean():
            previews.append((obj.name, preview.email.body))
    return render_to_response("messaging/previews.html", {"previews": previews}, RequestContext(request))
preview_messages.short_description = "Preview Messages"

class MessageAdmin(admin.ModelAdmin):
    list_display = ("__unicode__", "sends", "unique_opens", "click_thrus")
    readonly_fields = ("sends", "recipient_function")
    fieldsets = (
        (None, {"fields": ("name", "subject", "body", "sends", "recipient_function",)}),
        ("Send Time", {"fields": ("message_timing", "x_value",)}),
        ("Advanced Options", {"fields": ("send_as_batch", "batch_window", "time_snap", 
            "minimum_duration", "content_types", "generic_relation_content_type"),
            "classes": ("collapse",)}),
    )
    actions = [preview_messages]
    
class ABTestAdmin(admin.ModelAdmin):
    list_display = ("__unicode__", "control_sends", "control_opens", "test_sends", "test_opens")

admin.site.register(Message, MessageAdmin)
admin.site.register(ABTest, ABTestAdmin)
admin.site.register(Stream)