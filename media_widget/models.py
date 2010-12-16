from django.db import models
from thumbnails.fields import ImageAndThumbsField

class StickerImage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    description =models.CharField(max_length=255, blank=True)
    image = ImageAndThumbsField(upload_to="sticker_images" )
    approved = models.BooleanField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sticker image"
        verbose_name_plural = "Sticker images"

