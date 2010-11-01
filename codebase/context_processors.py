from django.conf import settings

from models import Ticket
from forms import TestingFeedbackForm

def testing_feedback_form(request):
    context = {}
    if settings.DEBUG:
        context["testing_feedback_form"] = TestingFeedbackForm()
        context["tickets"] = Ticket.objects.qa_tickets()
    return context