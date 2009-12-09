from django.contrib import admin
from www.rah.models import *
from www.rah.forms import *

class SignupAdmin(admin.ModelAdmin):
    list_display = ('email', 'zipcode')
    search_fields = ('email', 'zipcode')

class ActionAdmin(admin.ModelAdmin):
    form = ActionAdminForm

class ActionCatAdmin(admin.ModelAdmin):
    form = ActionCatAdminForm

admin.site.register(Signup, SignupAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(ActionCat, ActionCatAdmin)
admin.site.register(Profile)
