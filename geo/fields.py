from django.forms import ValidationError
from django.contrib.localflavor.us.forms import USZipCodeField

from models import Location

class ZipCodeField(USZipCodeField):
    def clean(self, value):
        if value:
            if not Location.objects.filter(zipcode=value).exists():
                raise ValidationError("Invalid zipcode %s" % value)
        return value