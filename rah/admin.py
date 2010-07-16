from django.contrib import admin
from django.contrib.auth.models import User, Group, Permission
from django.contrib.comments.models import Comment

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

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_name", "parent", "comment", "submit_date",)
    
    def parent(self, obj):
        return str(obj.content_object)
    parent.short_description = "Parent"

admin.site.register(Comment, CommentAdmin)