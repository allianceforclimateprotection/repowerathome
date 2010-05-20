from django.contrib.auth.decorators import login_required
from django.contrib import contenttypes, messages
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.template import loader, RequestContext
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

from django.contrib.auth.models import User

from models import Rating

@login_required
@require_POST
@csrf_protect
def rate(request, next=None, using=None, success_message=None, error_message=None):
    content_type_pk = request.POST.get("content_type", "-1")
    object_pk = request.POST.get("object_pk", "-1")
    try:
        content_type = ContentType.objects.get(pk=content_type_pk)
        target = content_type.get_object_for_this_type(pk=object_pk)
    except AttributeError:
        raise Http404("No type found matching %s" % content_type_pk)
    except ObjectDoesNotExist:
        raise Http404("No object found matching %s" % object_pk)
    except ValueError:
        raise Http404("Invalid parameters %s, %s" % (content_type_pk, object_pk))
    score = request.POST.get("score", None)
    if score == None:
        raise Http404("Missing score value")
    score = int(score)
    rating, created = Rating.objects.create_or_update(content_type=content_type, object_pk=object_pk, 
        user=request.user, score=score)
    
    if success_message and rating:
        messages.success(request, success_message)
    elif error_message and not rating:
        messages.error(request, error_message)
    next = request.POST.get("next", next)
    if next:
        return redirect(next)
        
    template_list = [
        "rateable/%s/%s/rated.html" % (content_type.model_class()._meta.app_label, content_type.model_class()._meta.module_name),
        "rateable/%s/rated.html" % content_type.model_class()._meta.app_label,
        "rateable/rated.html",
    ]
    if request.is_ajax():
        template_list = [ 
        "rateable/%s/%s/ajax/rated.html" % (content_type.model_class()._meta.app_label, content_type.model_class()._meta.module_name),
        "rateable/%s/ajax/rated.html" % content_type.model_class()._meta.app_label,
        "rateable/ajax/rated.html",
        ] + template_list
    response = loader.render_to_string(template_list, {"rating": rating}, context_instance=RequestContext(request))
    for message in request._messages: pass #if messages weren't used in the response, clear them out
    return HttpResponse(response)   