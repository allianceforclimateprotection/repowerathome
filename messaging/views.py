from django.http import HttpResponse
from django.template import loader, Context

from models import RecipientMessage

def open(request, token):
    try:
        recipient_message = RecipientMessage.objects.get(token=token)
        recipient_message.opens += 1
        recipient_message.save()
    except RecipientMessage.DoesNotExist:
        # TODO: an invalid token was passed back, we should track this in some log
        pass
    response = HttpResponse(mimetype="image/gif")
    t = loader.get_template("messaging/open_tracker.gif")
    response.write(t.render(Context({})))
    return response
