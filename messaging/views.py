from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import loader, Context

from utils import hex_to_byte

from models import RecipientMessage, MessageLink

ONE_PX_BY_ONE_PX_HEX_STRING = "47 49 46 38 37 61 01 00 01 00 80 00 00 ff ff ff 00 02 00 2c 00 \
    00 00 00 01 00 01 00 00 02 02 44 01 00 3b"
ONE_PX_BY_ONE_PX_BYTE_STRING = hex_to_byte(ONE_PX_BY_ONE_PX_HEX_STRING)

def open(request, token):
    try:
        recipient_message = RecipientMessage.objects.get(token=token)
        recipient_message.opens += 1
        recipient_message.save()
    except RecipientMessage.DoesNotExist:
        # TODO: an invalid token was passed back, we should track this in some log
        pass
    response = HttpResponse(mimetype="image/gif")
    response.write(ONE_PX_BY_ONE_PX_BYTE_STRING)
    return response
    
def click(request, token):
    message_link = get_object_or_404(MessageLink, token=token)
    message_link.clicks += 1
    message_link.save()
    return HttpResponseRedirect(message_link.link)
