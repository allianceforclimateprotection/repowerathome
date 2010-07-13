from django.contrib import admin

from models import Message, ABTest, Stream

class MessageAdmin(admin.ModelAdmin):
    list_display = ("__unicode__", "sends", "unique_opens")
    readonly_fields = ("sends", "recipient_function")
    
class ABTestAdmin(admin.ModelAdmin):
    list_display = ("__unicode__", "control_sends", "control_opens", "test_sends", "test_opens")

admin.site.register(Message, MessageAdmin)
admin.site.register(ABTest, ABTestAdmin)
admin.site.register(Stream)