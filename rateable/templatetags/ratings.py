from django import template
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.loader import render_to_string

from rateable.models import Rating
from rateable.forms import RatingForm

from django.contrib.auth.models import User

register = template.Library()

class RatingNode(template.Node):
    @classmethod
    def parse(cls, parser, token):
        tokens = token.contents.split()
        if tokens[1] != "for":
            raise template.TemplateSyntaxError("Second argument in %r tag must be 'for'" % tokens[0])

        if tokens[3] != "as":
            raise template.TemplateSyntaxError("Third argument in %r must be 'as'" % token[0])
        return parser.compile_filter(tokens[2]), tokens[4]
    
    def __init__(self, object_expr, varname=None, query_eval=None):
        self.object_expr = object_expr
        self.varname = varname
        self.query_eval = query_eval
        
    def get_target(self, context):
        obj = self.object_expr.resolve(context)
        return ContentType.objects.get_for_model(obj), obj.pk
        
    def get_query(self, context):
        content_type, object_pk = self.get_target(context)
        return Rating.objects.filter(content_type=content_type, object_pk=object_pk)
        
    def render(self, context):
        query = self.get_query(context)
        context[self.varname] = self.query_eval(query)
        return ""
        
class RatingFormNode(RatingNode):
    @classmethod
    def parse(cls, parser, token):
        tokens = token.contents.split()
        if tokens[1] != "for":
            raise template.TemplateSyntaxError("Second argument in %r tag must be 'for'" % tokens[0])
            
        return parser.compile_filter(tokens[2])
        
    def render(self, context):
        content_type, object_pk = self.get_target(context)
        rating = Rating(content_type=content_type, object_pk=object_pk, 
            score=Rating.objects.get_users_current_score(content_type, object_pk, context.get("request").user))
        form = RatingForm(instance=rating, auto_id=False)
        context.push() #move the context stack forward so our variable names don't conflict
        value = render_to_string("rateable/form.html", {"form":form}, context)
        context.pop()
        return value

@register.tag
def get_rating_count(parser, token):
    """
    Gets the ratings count, that is the number of users that have rated this object.
    And populates the template with a variable contained that value, whose name is
    is defined by the 'as' clause

    Syntax::
    
        {% get_rating_count for [object] as [varname] %}
        
    Example usage::
    
        {% get_rating_count for post as rating_count %}
    """
    object_expr, varname = RatingNode.parse(parser, token)
    return RatingNode(object_expr, varname, lambda q: q.count())
    
@register.tag
def get_rating_sum(parser, token):
    """
    Gets the ratings sum, that is the sum rating for this object.
    And populates the template with a variable contained that value, whose name is
    is defined by the 'as' clause

    Syntax::

        {% get_rating_sum for [object] as [varname] %}

    Example usage::

        {% get_rating_sum for post as rating_count %}
    """
    object_expr, varname = RatingNode.parse(parser, token)
    return RatingNode(object_expr, varname, lambda q: q.aggregate(sum=models.Sum("score"))["sum"])
    
@register.tag
def get_rating_avg(parser, token):
    """
    Gets the ratings avg, that is the avg rating for this object.
    And populates the template with a variable contained that value, whose name is
    is defined by the 'as' clause

    Syntax::

        {% get_rating_avg for [object] as [varname] %}

    Example usage::

        {% get_rating_avg for post as rating_count %}
    """
    object_expr, varname = RatingNode.parse(parser, token)
    return RatingNode(object_expr, varname, lambda q: q.aggregate(avg=models.Avg("score"))["avg"])
    
@register.tag
def get_rating_form(parser, token):
    """
    Get a form to rate an object
    
    Syntax::
    
        {% get_rating_form for [object] %}
    """
    object_expr = RatingFormNode.parse(parser, token)
    return RatingFormNode(object_expr)