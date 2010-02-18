import pdb

from django.contrib.auth.decorators import login_required
from django.contrib import contenttypes, messages
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

from django.contrib.auth.models import User

from models import Rating
from widgets import IsHelpfulWidget

@require_POST
@csrf_protect
def rate(request, rating_widget=IsHelpfulWidget, next=None, using=None, success_message=None, error_message=None):
    content_type_pk = request.POST.get("content_type")
    object_pk = request.POST.get("object_pk")
    try:
        content_type = ContentType.objects.get(pk=content_type_pk)
        target = content_type.get_object_for_this_type(pk=object_pk)
    except AttributeError:
        # TODO: handle error if content type is invalid
        pass
    except ObjectDoesNotExist:
        # TODO: handle error if object can not be found
        pass
    # if the score is defined in the post data override that provided
    score = rating_widget.determine_score(request.POST)
    rating, created = Rating.objects.create_or_update(content_type=content_type, object_pk=object_pk, 
        user=request.user, score=score)
    
    if success_message and rating:
        messages.success(request, success_message)
    elif error_message and not rating:
        messages.error(request, error_message)
    # pdb.set_trace()
    next = request.POST.get("next", next)
    if next:
        return redirect(next)
        
    template_list = [
        "rateable/%s/rated.html" % content_type.model_class()._meta.app_label,
        "rateable/rated.html",
    ]
    if request.is_ajax():
        template_list = [ 
            "rateable/%s/ajax/rated.html" % content_type.model_class()._meta.app_label,
            "rateable/ajax/rated.html",
        ] + template_list 
    return render_to_response(template_list, {"rating":rating}, context_instance=RequestContext(request))    