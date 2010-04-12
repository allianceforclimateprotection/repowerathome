from django.contrib import admin
from models import Group, GroupUsers

class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "is_geo_group",)
    list_filter = ("is_geo_group",)
    readonly_fields = ("is_geo_group", "location_type", "sample_location", "parent",)

admin.site.register(Group, GroupAdmin)
admin.site.register(GroupUsers)