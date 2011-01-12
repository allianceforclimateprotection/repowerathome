import datetime
import json

from django.db.models import Q
from django.http import HttpResponse
from django.views.generic.list_detail import object_list

def search_list(request, queryset, search_fields=None, 
    template_name="search_widget/_search_listing.html", 
    object_rendering_template=None, **kwargs):
    if not search_fields:
        search_fields = []
    if request:
        search = request.GET.get("search", None)
        if search:
            queryset = queryset.filter(__build_q_from_fields(search_fields, search.strip()))
        else:
            queryset = queryset.none()
    if object_rendering_template:
        ec = kwargs.get("extra_context", {})
        ec["object_rendering_template"] = object_rendering_template
        kwargs["extra_context"] = ec
    format_ = request.GET.get("format", "html")
    if format_ == "json":
        fields = request.GET.get("fields", None).split(",")
        data = queryset.values(*fields) if fields else queryset.values()
        dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
        return HttpResponse(json.dumps(list(data), default=dthandler), mimetype="text/json")
    return object_list(request, queryset=queryset, template_name=template_name, **kwargs)
    
def __build_q_from_fields(fields, search):
    if fields:
        q = Q()
        for f in fields:
            q |= Q(**{"%s__icontains" % f: search})
    else:
        q = Q(name__icontains=search)
    return q
