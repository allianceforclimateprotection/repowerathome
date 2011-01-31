import datetime
import json
import os

from django.db.models import Q
from django.http import HttpResponse
from django.views.generic.list_detail import object_list

def search_list(request, queryset, search_fields=None, template_name="search_widget/_search_listing.html",
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
    if not os.path.splitext(template_name)[1]:
        template_name = "%s.%s" % (template_name, format_)
    if format_ == "json":
        mimetype = "text/json"
    else:
        mimetype = "text/html"
    if request.GET.get("page", None) == "all":
        kwargs.pop("paginate_by")
    return object_list(request, queryset=queryset, template_name=template_name,
            mimetype=mimetype, **kwargs)

def __build_q_from_fields(fields, search):
    if fields:
        q = Q()
        for f in fields:
            q |= Q(**{"%s__icontains" % f: search})
    else:
        q = Q(name__icontains=search)
    return q
