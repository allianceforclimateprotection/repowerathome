from django.conf import settings

from models import Ticket
from forms import TestingFeedbackForm

def testing_feedback_form(request):
    context = {}
    if settings.DEBUG:
        tickets = Ticket.objects.qa_tickets()
        context["tickets"] = tickets
        context["testing_feedback_form"] = TestingFeedbackForm(
            initial={"ticket_id": tickets[0].ticket_id if tickets else 0})
    return context