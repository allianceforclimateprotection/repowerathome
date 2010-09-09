from django.db import models
from django.contrib.admin.filterspecs import FilterSpec, ChoicesFilterSpec
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext as _

class StateFilterSpec(ChoicesFilterSpec):
    def __init__(self, f, request, params, model, model_admin):
        super(StateFilterSpec, self).__init__(f, request, params, model,
                                                   model_admin)
        self.lookup_kwarg = '%s__st' % f.name
        self.lookup_val = request.GET.get(self.lookup_kwarg, None)
        self.lookup_choices = list(model.objects.distinct().values_list("%s__st" % f.name, flat=True))
        self.lookup_choices.sort()

    def choices(self, cl):
        yield {'selected': self.lookup_val is None,
                'query_string': cl.get_query_string({}, [self.lookup_kwarg]),
                'display': _('All')}
        for val in self.lookup_choices:
            yield {'selected': smart_unicode(val) == self.lookup_val,
                    'query_string': cl.get_query_string({self.lookup_kwarg: val}),
                    'display': val.upper()}
    def title(self):
        return _('%(field_name)s') % \
            {'field_name': "state"}

# registering the filter
FilterSpec.filter_specs.insert(0, (lambda f: getattr(f, 'state_filter', False),
                                   StateFilterSpec))