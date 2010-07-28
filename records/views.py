import json

from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext, loader, Context
from django.views.decorators.csrf import csrf_protect

from models import Record
from forms import AskToShareForm

def chart(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if not request.is_ajax():
        return redirect("index")
    tooltip_template = loader.get_template("records/_chart_tooltip.html")
    chart_points = Record.objects.get_chart_data(user)
    point_data = [(cp.get_date_as_milli_from_epoch(), cp.points) for cp in chart_points]
    tooltips = [tooltip_template.render(Context({"records": cp.records, "request": request})) for cp in chart_points]
    context = {'chart_data': json.dumps({"point_data": point_data, "tooltips": tooltips})}
    return render_to_response("records/_chart.js", context, RequestContext(request), mimetype="text/javascript")
    
@csrf_protect
def ask_to_share(request):
    form = AskToShareForm(request.POST or None)
    if form.is_valid():
        is_shared = form.save(request=request)
        messages.success(request, "Your activity is now being shared")
        if request.is_ajax():
            response = loader.render_to_string("records/sharing_response.js", locals(), 
                RequestContext(request))
            return HttpResponse(response, mimetype="text/javascript")
        return redirect("profile_edit", user_id=request.user.id)
    template = "records/_ask_to_share.html" if request.is_ajax() else "records/ask_to_share.html"
    return render_to_response(template, locals(), RequestContext(request))
    