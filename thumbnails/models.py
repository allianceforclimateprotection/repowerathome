from django.db import models

class ThumbnailManager(models.Manager):
    def thumbnails_for(self, raw):
        return self.filter(raw=raw).values_list("thumbnail", flat=True)

class Thumbnail(models.Model):
    raw = models.CharField(max_length=255, db_index=True)
    thumbnail = models.CharField(max_length=255)
    objects = ThumbnailManager()

    class Meta:
        unique_together = ("raw", "thumbnail",)
