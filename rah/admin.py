from django.contrib import admin
from django.contrib.auth.models import User, Group, Permission
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse

from models import Profile
from forms import ProfileEditForm
from rateable.models import Rating

class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "location", "date_joined",)
    ordering = ("id",)
    date_hierarchy = "date_joined"
    search_fields = ("email", "first_name", "last_name",)

    def location(self, obj):
        return obj.get_profile().location
    location.short_description = "Location"

class ProfileAdmin(admin.ModelAdmin):
    form = ProfileEditForm

admin.site.register(User, UserAdmin)
admin.site.register(Group)
admin.site.register(Permission)
admin.site.register(Profile, ProfileAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_name", "parent", "comment", "likes", "dislikes", "submit_date",)

    def __init__(self, *args, **kwargs):
        super(CommentAdmin, self).__init__(*args, **kwargs)
        self.content_type = ContentType.objects.get_for_model(Comment)

    def parent(self, obj):
        return str(obj.content_object)
    parent.short_description = "Parent"

    def likes(self, obj):
        return Rating.objects.filter(content_type=self.content_type, object_pk=obj.id,
            score=1).count()
    likes.short_description = "Likes"

    def dislikes(self, obj):
        return Rating.objects.filter(content_type=self.content_type, object_pk=obj.id,
            score=0).count()
    dislikes.short_description = "Dislikes"

admin.site.register(Comment, CommentAdmin)
