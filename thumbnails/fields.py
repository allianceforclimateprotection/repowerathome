import os
import re
import StringIO
import tempfile

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import models
from django.db.models.fields.files import ImageFieldFile

from PIL import Image

from processors import Resize, Detail, Sharpen

class ImageAndThumbsFile(ImageFieldFile):
    PROCESSORS = [Resize, Detail, Sharpen]
    
    def __init__(self, *args, **kwargs):
        super(ImageAndThumbsFile, self).__init__(*args, **kwargs)
        
    def __getattribute__(self, name):
        try:
            return super(ImageAndThumbsFile, self).__getattribute__(name)
        except AttributeError:
            if name.startswith("thumbnail"):
                thumbnail_name = self._generate_thumbnail_name(name)
                if default_storage.exists(thumbnail_name):
                    return thumbnail_name
                options = [opt for opt in name.split("_")[1:] if opt]
                thumbnail = self._process_options(options)
                thumbnail_name = default_storage.save(thumbnail_name, thumbnail)
                return thumbnail_name
            raise
        
    def _open_file(self, name):
        return ImageFieldFile(default_storage.open(name, ImageAndThumbsField(), name))
        
    def _generate_thumbnail_name(self, attribute_name):
        directory = os.path.dirname(self.name)
        basename = os.path.basename(self.name)
        filename, extension = os.path.splitext(basename)
        return "%s/%s__%s%s" % (directory, filename, attribute_name, extension)
        
    def _process_options(self, options):
        copy = ContentFile(default_storage.open(self.name).read())
        thumbnail = Image.open(copy)
        for option in options:
            for proc in ImageAndThumbsFile.PROCESSORS:
                matcher = proc.key_expression().match(option)
                if matcher:
                    proc.process(thumbnail, matcher)
                    break
        codec = os.path.splitext(self.name)[1][1:].lower()
        if codec == "png":
            imgstr = StringIO.StringIO()
            thumbnail.save(imgstr, "png")
            return ContentFile(imgstr.getvalue())
        return ContentFile(thumbnail.tostring(codec, thumbnail.mode))
        
class ImageAndThumbsField(models.ImageField):
    attr_class = ImageAndThumbsFile