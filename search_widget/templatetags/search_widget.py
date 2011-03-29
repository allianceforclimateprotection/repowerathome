import copy

from django import template
from django.conf import settings
from django.core.urlresolvers import NoReverseMatch, resolve, reverse
from django.template import loader, Node, RequestContext, TemplateSyntaxError
from django.utils.encoding import smart_str

register = template.Library()

class SearchWidgetNode(Node):
    def __init__(self, view_name, args, kwargs):
        self.view_name = view_name
        self.args = args
        self.kwargs = kwargs

    def render(self, context):
        args = [arg.resolve(context) for arg in self.args]
        kwargs = dict([(smart_str(k,'ascii'), v.resolve(context))
                       for k, v in self.kwargs.items()])
        try:
            path = reverse(self.view_name, args=args, kwargs=kwargs, current_app=context.current_app)
        except NoReverseMatch, e:
            if settings.SETTINGS_MODULE:
                project_name = settings.SETTINGS_MODULE.split('.')[0]
                try:
                    path = reverse(project_name + '.' + self.view_name,
                              args=args, kwargs=kwargs, current_app=context.current_app)
                except NoReverseMatch:
                    raise e
            else:
                raise e
        request = copy.copy(context["request"])
        request.path = path
        return loader.render_to_string("search_widget/_search_widget.html", {"request":request})

@register.tag
def search_widget(parser, token):
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument (url path to search)" % bits[0])
    viewname = bits[1]
    args = []
    kwargs = {}
    return SearchWidgetNode(viewname, args, kwargs)
