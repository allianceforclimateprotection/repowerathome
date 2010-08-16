import math
import re

from PIL import Image, ImageFilter

class Processor(object):
    @classmethod
    def key_expression(cls):
        """return a pattern that will be used to identify usage of this processor"""
        raise NotImplementedError
    
    @classmethod
    def process(cls, image, matcher):
        """take the provided thumbnail and process accordingly"""
        raise NotImplementedError
        
class Resize(Processor):
    @classmethod
    def key_expression(cls):
        return re.compile("^(\d+)x(\d+)$", re.IGNORECASE)
        
    @classmethod
    def process(cls, image, matcher):
        width = int(matcher.group(1))
        height = int(matcher.group(2))
        image.thumbnail((width,height), Image.ANTIALIAS)
        return image
        
class Detail(Processor):
    @classmethod
    def key_expression(cls):
        return re.compile("^detail$", re.IGNORECASE)
        
    @classmethod
    def process(cls, image, matcher):
        try:
            return image.filter(ImageFilter.DETAIL)
        except ValueError:
            pass
        return image
        
class Sharpen(Processor):
    @classmethod
    def key_expression(cls):
        return re.compile("^sharpen$", re.IGNORECASE)

    @classmethod
    def process(cls, image, matcher):
        try:
            return image.filter(ImageFilter.SHARPEN)
        except ValueError:
            pass
        return image
            
class SmartCrop(Processor):
    """
    Note this processor has a dependancy on the easy-thumbnails library
    """
    @classmethod
    def key_expression(cls):
        return re.compile("^(\d+)x(\d+)smartcrop$", re.IGNORECASE)
        
    @classmethod
    def process(cls, image, matcher):
        from easy_thumbnails.processors import scale_and_crop
        width = int(matcher.group(1))
        height = int(matcher.group(2))
        return scale_and_crop(im=image, size=(width,height), crop="smart")
            