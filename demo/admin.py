from django.contrib import admin
from models import *

admin.site.register(Group)
admin.site.register(User)
admin.site.register(Action)
admin.site.register(Activity)
admin.site.register(Record)
admin.site.register(ActionTask)