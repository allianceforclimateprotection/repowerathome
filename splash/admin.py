from django.contrib import admin
from www.splash.models import *

class SignupAdmin(admin.ModelAdmin):
    list_display = ('email', 'zipcode')
    search_fields = ('email', 'zipcode')

admin.site.register(Signup, SignupAdmin)