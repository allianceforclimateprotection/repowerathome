from django.contrib import admin
from models import StickerImage

class StickerImageAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    ordering = ("name",)

admin.site.register(StickerImage, StickerImageAdmin)
