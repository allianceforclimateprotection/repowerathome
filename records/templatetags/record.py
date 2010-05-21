from django import template

register = template.Library()

class RecordNode(template.Node):
    @classmethod
    def parse(cls, parser, token):
        tokens = token.contents.split()        
        if len(tokens) != 2:
            raise template.TemplateSyntaxError("Only 2 arguments needed for %s, the second should be a record" % tokens[0])
        return parser.compile_filter(tokens[1])
    
    def __init__(self, record_expr):
        self.record_expr = record_expr

    def render(self, context):
        record = self.record_expr.resolve(context)
        request = context["request"]
        return record.render(request)

@register.tag
def render_record(parser, token):
    """
    Render the record within the given context

    Syntax::

        {% render_record [record] %}
    """
    record_expr = RecordNode.parse(parser, token)
    return RecordNode(record_expr)