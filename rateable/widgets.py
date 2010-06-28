from itertools import chain

from django import forms
from django.core.urlresolvers import reverse
from django.forms import Widget, util
from django.utils.encoding import force_unicode
from django.utils.html import escape, conditional_escape
from django.utils.safestring import mark_safe

class IsHelpfulWidget(Widget):
    CHOICES = ((1, "Helpful"), (0, "Not Helpful"))

    def render(self, name, value, attrs=None):
        return mark_safe(self.render_options())

    def render_options(self):
        def render_option(option_value, option_label):
            option_value = force_unicode(option_value)
            output = u'<button type="submit" title="Mark this comment as %s" class="button_tooltip" name="score" value="%s"><span class="icon_rate_%s"></span></button>' % \
                     (option_label, option_value, option_value)
            return output
        output = []
        for option_value, option_label in IsHelpfulWidget.CHOICES:
            output.append(render_option(option_value, option_label))
        return u'\n'.join(output)
        
class ThumbsRadio(forms.RadioSelect):
    CHOICES = ((1, "I like this"), (0, "I dislike this"))
    
    def __init__(self, *args, **kwargs):
        return super(ThumbsRadio, self).__init__(*args, choices=ThumbsRadio.CHOICES, **kwargs)