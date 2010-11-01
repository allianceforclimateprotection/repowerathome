from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.views.decorators.http import require_POST

from utils import ajax_required

from forms import TestingFeedbackForm

@require_POST
@ajax_required
def feedback(request):
    testing_feedback_form = TestingFeedbackForm(request.POST)
    if testing_feedback_form.is_valid():
        testing_feedback_form.save()
    return render_to_response("codebase/_testing_widget.html", locals(), 
        context_instance=RequestContext(request))
    