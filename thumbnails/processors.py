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
        return re.compile("(\d+)x(\d+)", re.IGNORECASE)
        
    @classmethod
    def process(cls, image, matcher):
        width = int(matcher.group(1))
        height = int(matcher.group(2))
        image.thumbnail((width,height), Image.ANTIALIAS)
        
class Detail(Processor):
    @classmethod
    def key_expression(cls):
        return re.compile("detail", re.IGNORECASE)
        
    @classmethod
    def process(cls, image, matcher):
        try:
            image = image.filter(ImageFilter.DETAIL)
        except ValueError:
            pass
        
class Sharpen(Processor):
    @classmethod
    def key_expression(cls):
        return re.compile("sharpen", re.IGNORECASE)

    @classmethod
    def process(cls, image, matcher):
        try:
            image = image.filter(ImageFilter.SHARPEN)
        except ValueError:
            pass