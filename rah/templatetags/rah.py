from django import template
from django.core.urlresolvers import reverse

from records.models import Activity

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
        if user.id != current_user.id and user.get_profile().is_profile_private:
            return str(user.get_full_name())
        else:
            name = "You" if user.id == current_user.id else user.get_full_name()
            return "<a href='%s'>%s</a>" % (reverse("profile", args=[user.id]), name)

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
    
@register.filter
@template.defaultfilters.stringfilter
def deslug(value):
    return value.title().replace('_', ' ').replace('-', ' ')

class ActivityNode(template.Node):
    def __init__(self, activity, var_name):
        self.activity = activity
        self.var_name = var_name
        
    def render(self, context):
        context[self.var_name] = self.activity
        return ""

@register.tag
def activity_by_slug(parser, token):
    """
    Assign an activity object to a variable based on the slug provided.
    
    Syntax::
        {% activity_by_slug [slug] as [variable_name] %}
        
    Example usage::
        {% activity_by_slug group_create as group_create_activity %}
    """
    try:
        tag_name, slug, as_token, var_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, \
            "%(tag_name)s tag requires 4 arguments {%% %(tag_name)s [slug] as [var_name] %%}" % {"tag_name": token.contents.split()[0]}
            
    if slug[0] == slug[-1] and slug[0] in ('"', "'"):
        slug = slug[1:-1] #slug came through in quotes, strip them away
    
    activity = Activity.objects.get(slug=slug)
    return ActivityNode(activity, var_name)