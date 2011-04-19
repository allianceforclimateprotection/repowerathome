from django.contrib import admin

from models import Location
from filterspecs import StateFilterSpec

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

admin.site.register(Location, LocationAdmin)
