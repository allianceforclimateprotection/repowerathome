from django.contrib import admin

from models import Message, ABTest, Stream

class MessageAdmin(admin.ModelAdmin):
    list_display = ("__unicode__", "sends", "unique_opens")
    

admin.site.register(Message, MessageAdmin)
admin.site.register(ABTest)
admin.site.register(Stream)