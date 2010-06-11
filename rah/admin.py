from django.contrib import admin
from django.contrib.auth.models import User, Group, Permission

from models import Profile
from forms import ProfileEditForm

class UserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email",)
    ordering = ("id",)

class ProfileAdmin(admin.ModelAdmin):
    form = ProfileEditForm

admin.site.register(User, UserAdmin)
admin.site.register(Group)
admin.site.register(Permission)
admin.site.register(Profile, ProfileAdmin)