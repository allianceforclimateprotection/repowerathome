from django.contrib import admin

from models import Message, ABTest, Stream

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
    
class ABTestAdmin(admin.ModelAdmin):
    list_display = ("__unicode__", "control_sends", "control_opens", "test_sends", "test_opens")

admin.site.register(Message, MessageAdmin)
admin.site.register(ABTest, ABTestAdmin)
admin.site.register(Stream)