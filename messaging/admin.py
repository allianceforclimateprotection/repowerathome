from django.contrib import admin

from models import Message, ABTest, Stream

admin.site.register(Message)
admin.site.register(ABTest)
admin.site.register(Stream)