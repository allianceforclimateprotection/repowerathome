from django.contrib import admin
from www.rah.models import *

class SignupAdmin(admin.ModelAdmin):
    list_display = ('email', 'zipcode')
    search_fields = ('email', 'zipcode')

admin.site.register(Signup, SignupAdmin)
admin.site.register(Action)
admin.site.register(ActionCat)
admin.site.register(ActionStatus)
