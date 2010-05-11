from django import template
from django.template.loader import render_to_string

from invite.models import Invitation
from invite.forms import InviteForm

register = template.Library()

class InviteFormNode(template.Node):      
    def __init__(self, object_expr=None):
        self.object_expr = object_expr
        
    def get_target(self, context):
        return self.object_expr.resolve(context) if self.object_expr else None
        
    def render(self, context):
        content_object = self.get_target(context)
        if content_object:
            invite = Invitation(user=context["request"].user, content_object=content_object, 
                token=Invitation.objects.make_token())
        else:
            invite = Invitation(user=context["request"].user, token=Invitation.objects.make_token())
        form = InviteForm(instance=invite)
        context.push() #move the context stack forward so our variable names don't conflict
        value = render_to_string("invite/invite_form.html", {"form":form}, context)
        context.pop()
        return value
    
@register.tag
def get_invite_form(parser, token):
    """
    Get a form to send an invite to that is optionally related to an object
    
    Syntax::
        {% get_invite_form %}
                or
        {% get_invite_form for [object] %}
    """
    tokens = token.split_contents()
    if len(tokens) > 3:
        raise template.TemplateSyntaxError("Invalid Syntax")
    if len(tokens) == 1:
        return InviteFormNode()
    if tokens[1] != "for":
        raise template.TemplateSyntaxError("Second argument in %r tag must be 'for'" % tokens[0])
    return InviteFormNode(parser.compile_filter(tokens[2]))