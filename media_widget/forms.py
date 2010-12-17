from django import forms

from PIL.Image import open as pil_open
from models import StickerImage

class StickerImageUpload(forms.ModelForm):
    IMAGE_FORMATS = {"PNG": "png", "JPEG": "jpeg", "GIF": "gif"}
    name = forms.CharField(label="Your Name")
    email = forms.CharField(label="Your Email")

    class Meta:
        model = StickerImage
        exclude = ('updated', 'created', 'approved')

    def clean_image(self):
        data = self.cleaned_data["image"]
        if data:
            if data.size > 41943040:
                raise forms.ValidationError("Image must be smaller than 5MB")
            self.image_format = pil_open(data.file).format
            if not self.image_format in self.IMAGE_FORMATS:
                raise forms.ValidationError("Images cannot be of type %s" % data.content_type)
        return data

