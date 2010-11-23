from django.conf import settings

from models import Ticket
from forms import TestingFeedbackForm

def testing_feedback_form(request):
    context = {}
    if (hasattr(settings, 'USE_TESTING_WIDGET') and settings.USE_TESTING_WIDGET) or \
    request.META['SERVER_NAME'] == "staging.repowerathome.com":
        tickets = Ticket.objects.qa_tickets()
        context["tickets"] = tickets
        context["ticket_count"] = len(tickets)
        initial = {}
        if request.user.is_authenticated():
            initial["name"] = request.user.get_full_name()
        context["testing_feedback_form"] = TestingFeedbackForm(initial=initial)
    return context