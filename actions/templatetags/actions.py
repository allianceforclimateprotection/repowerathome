import re

from django import template
from django.template import Context, Template
from django.template.loader import render_to_string

from utils import strip_quotes

register = template.Library()

class ActionFormNode(template.Node):
    def __init__(self, complete_title, commitment_title):
        self.complete_title = complete_title
        self.commitment_title = commitment_title

    def render(self, context):
        values = {"complete_title": self.complete_title, 
            "commitment_title": self.commitment_title}
        context.push()
        value = render_to_string("actions/_action_form.html", values, context)
        context.pop()
        return value

@register.tag
def action_form(parser, token):
    try:
        tag_name, complete_title, commitment_title = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, \
            "%(tag_name)s tag requires 2 arguments {%% %(tag_name)s \
            [complete_title] [commitment_title] %%}" % \
            {"tag_name": token.contents.split()[0]}
    complete_title = strip_quotes(complete_title)
    commitment_title = strip_quotes(commitment_title)
    return ActionFormNode(complete_title, commitment_title)
    
class TemplateSnippetNode(template.Node):
    def __init__(self, filter_expr):
        self.filter_expr = filter_expr
        
    def render(self, context):
        template = Template(self.filter_expr.resolve(context))
        return template.render(context)
    
@register.tag
def render_template_snippet(parser, token):
    try:
        tag_name, snippet = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, \
            "%(tag_name)s tag requires 1 arguments {%% %(tag_name)s \
            [template_snippet] %%}" % {"tag_name": token.contents.split()[0]}
    return TemplateSnippetNode(parser.compile_filter(snippet))