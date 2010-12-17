from django.db import models
from thumbnails.fields import ImageAndThumbsField

class StickerImage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    description =models.CharField(max_length=255, blank=True, null=True,
        help_text="Tell us about where you stuck your sticker.")
    image = ImageAndThumbsField(upload_to="sticker_images",
        help_text="Image must be smaller than 1MB")
    approved = models.BooleanField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sticker image"
        verbose_name_plural = "Sticker images"

    def __unicode__(self):
        return u"%s" % (self.name)
