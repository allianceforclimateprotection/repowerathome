from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from models import User, Profile
from forms import ProfileEditForm

class ProfileAdmin(admin.ModelAdmin):
    form = ProfileEditForm

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)