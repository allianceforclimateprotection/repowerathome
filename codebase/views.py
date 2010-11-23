import json

from django.contrib import messages
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from utils import ajax_required

from forms import TestingFeedbackForm

@require_POST
@ajax_required
def feedback(request):
    testing_feedback_form = TestingFeedbackForm(request.POST)
    form_valid = testing_feedback_form.is_valid()    
    if form_valid:
        testing_feedback_form.save(request)
    
    return HttpResponse(json.dumps({
            "errors": testing_feedback_form.errors, 
            "valid": form_valid
        }), 
        mimetype="text/json")

@require_POST
@ajax_required
def set_wiget_state(request, opened=False):
    request.session["testing_widget_opened"] = opened
    return HttpResponse(json.dumps({"valid": True}), mimetype="text/json")