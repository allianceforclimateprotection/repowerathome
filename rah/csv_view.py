import csv
from django.http import HttpResponse, HttpResponseForbidden
from django.template.defaultfilters import slugify
from django.db.models.loading import get_model
from django.contrib import admin

def export(qs, fields=None):
    model = qs.model
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % slugify(model.__name__)
    writer = csv.writer(response)
    # Write headers to CSV file
    if fields:
        headers = fields
    else:
        headers = []
        for field in model._meta.fields:
            headers.append(field.name)
    writer.writerow(headers)
    # Write data to CSV file
    for obj in qs:
        row = []
        for field in headers:
            if field in headers:
                try:
                    val = getattr(obj, field)
                    if callable(val):
                        val = val()
                except AttributeError:
                    val = getattr(admin.site._registry[model], field)
                    if callable(val):
                        val = val(obj)
                row.append(val)
        writer.writerow(row)
    # Return CSV file to browser as download
    return response

def admin_list_export(request, model_name, app_label, queryset=None, fields=None, list_display=True):
    """
    Put the following line in your urls.py BEFORE your admin include
    (r'^admin/(?P<app_label>[\d\w]+)/(?P<model_name>[\d\w]+)/csv/', 'util.csv_view.admin_list_export'),
    """
    if not request.user.is_staff:
        return HttpResponseForbidden()
    
    if not queryset:
        model = get_model(app_label, model_name)
        model_admin = admin.site._registry[model]
        if hasattr(model_admin, "queryset"):
            queryset = model_admin.queryset(request)
        else:
            queryset = model.objects.all()
        filters = dict()
        for key, value in request.GET.items():
            if key not in ('ot', 'o'):
                filters[str(key)] = str(value)
    if len(filters):
        queryset = queryset.filter(**filters)
    if not fields and list_display:
        ld = admin.site._registry[queryset.model].list_display
        if ld and len(ld) > 0: fields = ld[1:]
    return export(queryset, fields)