from django.contrib import admin

from models import Action
from forms import ActionAdminForm

class ActionAdmin(admin.ModelAdmin):
    list_display = ("name", "tag_list", "points", "updated",)
    search_fields = ("name",)
    ordering = ("name",)
    readonly_fields = ("users_completed", "users_committed",)
    form = ActionAdminForm

admin.site.register(Action, ActionAdmin)