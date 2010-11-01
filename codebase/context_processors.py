from django.conf import settings

from models import Ticket
from forms import TestingFeedbackForm

def testing_feedback_form(request):
    context = {}
    if (hasattr(settings, 'USE_TESTING_WIDGET') and settings.USE_TESTING_WIDGET) or \
    request.META['SERVER_NAME'] == "staging.repowerathome.com":
        tickets = Ticket.objects.qa_tickets()
        context["tickets"] = tickets
        context["testing_feedback_form"] = TestingFeedbackForm(
            initial={"ticket_id": tickets[0].ticket_id if tickets else 0})
    return context