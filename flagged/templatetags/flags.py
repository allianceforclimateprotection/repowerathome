from django import template
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.loader import render_to_string

from flagged.models import Flag
from flagged.forms import FlagForm

register = template.Library()

class FlagFormNode(template.Node):
    @classmethod
    def parse(cls, parser, token):
        tokens = token.contents.split()
        if tokens[1] != "for":
            raise template.TemplateSyntaxError("Second argument in %r tag must be 'for'" % tokens[0])
            
        return parser.compile_filter(tokens[2])
        
    def __init__(self, object_expr):
        self.object_expr = object_expr
        
    def get_target(self, context):
        obj = self.object_expr.resolve(context)
        return ContentType.objects.get_for_model(obj), obj.pk
        
    def render(self, context):
        content_type, object_pk = self.get_target(context)
        flag = Flag(content_type=content_type, object_pk=object_pk)
        form = FlagForm(instance=flag, auto_id=False)
        context.push() #move the context stack forward so our variable names don't conflict
        value = render_to_string("flagged/flag_form.html", {"form":form}, context)
        context.pop()
        return value
    
@register.tag
def get_flag_form(parser, token):
    """
    Get a form to flag an object
    
    Syntax::
    
        {% get_flag_form for [object] %}
    """
    object_expr = FlagFormNode.parse(parser, token)
    return FlagFormNode(object_expr)