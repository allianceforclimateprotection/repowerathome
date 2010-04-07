from django.contrib import admin
from models import Signup, Profile

class SignupAdmin(admin.ModelAdmin):
    list_display = ('email', 'zipcode')
    search_fields = ('email', 'zipcode')

admin.site.register(Signup, SignupAdmin)
admin.site.register(Profile)