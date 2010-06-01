from django.contrib import admin

from models import Profile
from forms import ProfileEditForm

class ProfileAdmin(admin.ModelAdmin):
    form = ProfileEditForm

admin.site.register(Profile, ProfileAdmin)