from django.contrib.auth.decorators import login_required
from django.contrib import contenttypes, messages
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render_to_response
from django.template import loader, RequestContext
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

from django.contrib.auth.models import User

from models import Flag

@login_required
@require_POST
@csrf_protect
def flag(request, next=None, using=None):
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
    success = Flag.objects.flag_content(content_type=content_type, object_pk=object_pk, user=request.user)
    
    if success:
        messages.success(request, "You have added a flag. A moderator will review your submission shortly.")
    else:
        messages.success(request, "You have already added a flag.")
    next = request.POST.get("next", next)
    if next:
        return redirect(next)
        
    template_list = [
        "flagged/%s/%s/flagged.html" % (content_type.model_class()._meta.app_label, content_type.model_class()._meta.module_name),
        "flagged/%s/flagged.html" % content_type.model_class()._meta.app_label,
        "flagged/flagged.html",
    ]
    if request.is_ajax():
        template_list = [
            "flagged/%s/%s/ajax/flagged.html" % (content_type.model_class()._meta.app_label, content_type.model_class()._meta.module_name),
            "flagged/%s/ajax/flagged.html" % content_type.model_class()._meta.app_label,
            "flagged/ajax/flagged.html",
        ] + template_list
    response = loader.render_to_string(template_list, {"success": success}, context_instance=RequestContext(request))
    for message in request._messages: pass #if messages weren't used in the response, clear them out
    return HttpResponse(response)

@login_required
@require_POST
@csrf_protect
def unflag(request, next=None, using=None):
    content_type_pk = request.POST.get("content_type")
    object_pk = request.POST.get("object_pk")
    try:
        content_type = ContentType.objects.get(pk=content_type_pk)
        target = content_type.get_object_for_this_type(pk=object_pk)
    except AttributeError:
        raise Http404("No type found matching %s" % content_type_pk)
    except ObjectDoesNotExist:
        raise Http404("No object found matching %s" % object_pk)
    success = Flag.objects.unflag_content(content_type=content_type, object_pk=object_pk, user=request.user)

    if success:
        messages.success(request, "Your flag has been removed.")
    else:
        messages.success(request, "You have not yet flagged this.")
    next = request.POST.get("next", next)
    if next:
        return redirect(next)

    template_list = [
        "flagged/%s/unflagged.html" % content_type.model_class()._meta.app_label,
        "flagged/unflagged.html",
    ]
    if request.is_ajax():
        template_list = [ 
            "flagged/%s/ajax/unflagged.html" % content_type.model_class()._meta.app_label,
            "flagged/ajax/unflagged.html",
        ] + template_list
    response = loader.render_to_string(template_list, {"success": success}, context_instance=RequestContext(request))
    for message in request._messages: pass #if messages weren't used in the response, clear them out
    return HttpResponse(response)
