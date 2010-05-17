from itertools import chain

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
            output = u'<button type="submit" title="Mark this comment as %s" class="button_tooltip" name="%s" value="%s"><span class="icon_rate_%s"></span></button>' % \
                     (option_label, option_label, conditional_escape(force_unicode(option_label)), option_value)
            return output
        output = []
        for option_value, option_label in IsHelpfulWidget.CHOICES:
            output.append(render_option(option_value, option_label))
        return u'\n'.join(output)
    
    @classmethod   
    def determine_score(cls, POST):
        for option_value, option_label in IsHelpfulWidget.CHOICES:
            if POST.has_key(option_label):
                return option_value
        return None