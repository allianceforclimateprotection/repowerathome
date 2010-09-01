import csv

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import loader, Context, RequestContext

from rah.models import Profile

from forms import UserExportForm

# writer.writerow(['="%s"' % s if s and excel_friendly else s for s in row])

@staff_member_required
def user_export(request):
    form = UserExportForm(request.POST or None)
    if form.is_valid():
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=user_activity.csv'
        writer = csv.writer(response, dialect='excel')
        form.save_to_writer(writer)
        return response
    return render_to_response("export/user_export.html", locals(), context_instance=RequestContext(request))
