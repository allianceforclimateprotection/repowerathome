from django import template
from django.core.urlresolvers import reverse

register = template.Library()

class UserNode(template.Node):
    @classmethod
    def parse(cls, parser, token):
        tokens = token.contents.split()        
        if len(tokens) != 2:
            raise template.TemplateSyntaxError("Only 2 arguments needed for %s, the second should be a user" % tokens[0])
        return parser.compile_filter(tokens[1])
    
    def __init__(self, user_expr):
        self.user_expr = user_expr

    def render(self, context):
        user = self.user_expr.resolve(context)
        current_user = context["request"].user
        if user != current_user and user.get_profile().is_profile_private:
            return str(user.get_full_name())
        else:
            return "<a href='%s'>%s</a>" % (reverse("profile", args=[user.id]), user.get_full_name())

@register.tag
def safe_user_link(parser, token):
    """
    Return a safe user link that is only wrap the user's name in a hyperlink
    to their profile if either their profile is not private or the user
    making the request is trying to view their own link.

    Syntax::

        {% safe_user_link [user] %}

    Example usage::

        {% safe_user_link request.user %}
    """
    user_expr = UserNode.parse(parser, token)
    return UserNode(user_expr)