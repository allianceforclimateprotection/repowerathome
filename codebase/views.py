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
    if testing_feedback_form.is_valid():
        testing_feedback_form.save(request)
        messages.success(request, "Thanks for the feedback")
        testing_feedback_form = TestingFeedbackForm()
    message_html = render_to_string("_messages.html", {}, RequestContext(request))
    form_html= render_to_string("codebase/_testing_feedback_form.html", locals(), RequestContext(request))
    return HttpResponse(json.dumps({"message_html": message_html, "form_html": form_html}), 
        mimetype="text/json")

@require_POST
@ajax_required
def set_wiget_state(request, opened=False):
    request.session["testing_widget_opened"] = opened
    return HttpResponse(json.dumps({"valid": True}), mimetype="text/json")