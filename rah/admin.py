from django.contrib import admin
from rah.models import *
from rah.forms import *

class SignupAdmin(admin.ModelAdmin):
    list_display = ('email', 'zipcode')
    search_fields = ('email', 'zipcode')

class ActionAdmin(admin.ModelAdmin):
    form = ActionAdminForm

class ActionCatAdmin(admin.ModelAdmin):
    form = ActionCatAdminForm
    
class LocationAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'county', 'recruit')
    list_filter = ('recruit',)
    search_fields = ('zipcode', 'county')
    actions = ['set_recruitable', 'unset_recruitable']
    
    def set_recruitable(self, request, queryset):
        rows_updated = queryset.update(recruit=1)
        message_bit = "%s locations were" % rows_updated
        self.message_user(request, "%s successfully marked as recruitable." % message_bit)
    set_recruitable.short_description = "Mark selected locations as recruitable"

    def unset_recruitable(self, request, queryset):
        rows_updated = queryset.update(recruit=0)
        message_bit = "%s locations were" % rows_updated
        self.message_user(request, "%s successfully marked as NOT recruitable." % message_bit)
    unset_recruitable.short_description = "Mark selected locations as NOT recruitable"

admin.site.register(Signup, SignupAdmin)
admin.site.register(ActionTask)
admin.site.register(Action, ActionAdmin)
admin.site.register(ActionCat, ActionCatAdmin)
admin.site.register(Profile)
admin.site.register(Location, LocationAdmin)
