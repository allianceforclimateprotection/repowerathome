from django.contrib import admin
from models import StickerImage

class StickerImageAdmin(admin.ModelAdmin):
    search_fields = ("name", "description", "email",)
    ordering = ("-created",)
    list_display = ("name", "email", "description", "created", "approved",)

admin.site.register(StickerImage, StickerImageAdmin)
