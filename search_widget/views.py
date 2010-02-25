from django.views.generic.list_detail import object_list

def search_list(request, *args, **kwargs):
    if request:
        search = request.GET.get("search", None)
        if search:
            kwargs["queryset"] = kwargs["queryset"].filter(name__icontains=search.strip())
    if not "template_name" in kwargs:
        kwargs["template_name"] = "search_widget/_search_listing.html"
    return object_list(request, *args, **kwargs)