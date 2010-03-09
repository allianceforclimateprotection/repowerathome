from django.contrib import admin
from rah.models import Signup, ActionTask, Action, Profile
from rah.forms import ActionAdminForm

class SignupAdmin(admin.ModelAdmin):
    list_display = ('email', 'zipcode')
    search_fields = ('email', 'zipcode')

class ActionAdmin(admin.ModelAdmin):
    form = ActionAdminForm

admin.site.register(Signup, SignupAdmin)
admin.site.register(ActionTask)
admin.site.register(Action, ActionAdmin)
admin.site.register(Profile)