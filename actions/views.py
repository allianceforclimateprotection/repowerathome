import datetime
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_protect

from tagging.models import Tag
from records.models import Record

from models import Action, UserActionProgress, ActionForm, ActionFormData
from forms import ActionCommitForm
import action_forms

def action_show(request, tag_slug=None):
    """Show all actions by Category"""
    actions = Action.objects.all()
    if tag_slug:
        tag_filter = get_object_or_404(Tag, name=tag_slug)
        actions = Action.tagged.with_any(tag_filter)
    tags = Action.tags.cloud()
    return render_to_response("actions/action_show.html", locals(), 
        context_instance=RequestContext(request))

@csrf_protect
def action_detail(request, action_slug):
    """Detail page for an action"""
    action = get_object_or_404(Action, slug=action_slug)
    default_vars = _default_action_vars(action, request.user)
    default_vars.update(_build_action_form_vars(action, request.user))
    action_commit_form = ActionCommitForm(user=request.user, action=action)
    default_vars.update(locals())
    return render_to_response("actions/action_detail.html", default_vars, RequestContext(request))
        
@login_required
@csrf_protect
def action_complete(request, action_slug):
    """invoked when a user marks an action as completed"""
    action = get_object_or_404(Action, slug=action_slug)
    if request.method == "GET":
        return redirect("action_detail", action_slug=action.slug)
    if action.complete_for_user(request.user):
        messages.success(request, "Thanks for completing this action.")
    return redirect("action_detail", action_slug=action.slug)
    
@login_required
@csrf_protect
def action_undo(request, action_slug):
    action = get_object_or_404(Action, slug=action_slug)
    if request.method == "GET":
        return redirect("action_detail", action_slug=action.slug)
    if action.undo_for_user(request.user):
        messages.success(request, "We have corrected the mistake.")
    return redirect("action_detail", action_slug=action.slug)
    
@login_required
@csrf_protect
def action_commit(request, action_slug):
    action = get_object_or_404(Action, slug=action_slug)
    if request.method == "GET":
        return redirect("action_detail", action_slug=action.slug)
    action_commit_form = ActionCommitForm(user=request.user, action=action, data=request.POST)
    if action_commit_form.is_valid():
        action_commit_form.save()
        messages.success(request, "Thanks for making a commitment.")
        return redirect("action_detail", action_slug=action.slug)
    default_vars = _default_action_vars(action, request.user)
    default_vars.update(locals())
    return render_to_response("actions/action_detail.html", default_vars, RequestContext(request))
    
@login_required
@csrf_protect
def action_cancel(request, action_slug):
    action = get_object_or_404(Action, slug=action_slug)
    if request.method == "POST":    
        if action.cancel_for_user(request.user):
            messages.success(request, "Sorry to see you can not make the commitment.")
        return redirect("action_detail", action_slug=action.slug)
    return render_to_response("actions/action_cancel.html", locals(), RequestContext(request))

@login_required
@csrf_protect
def save_action_from(request, action_slug, form_name):
    action = get_object_or_404(Action, slug=action_slug)
    action_form = get_object_or_404(ActionForm, action=action, form_name=form_name)
    if request.method == "GET":
        return redirect("action_detail", action_slug=action.slug)
    afd, c = ActionFormData.objects.get_or_create(action_form=action_form, user=request.user)
    data = request.POST.copy()
    if "csrfmiddlewaretoken" in data:
        del data["csrfmiddlewaretoken"]
    if afd.data:
        existing = json.loads(afd.data)
        existing.update(data.items())
        data = existing
        afd.data = json.dumps(data)
    else:
        afd.data = json.dumps(data)
    afd.save()
    if request.is_ajax():
        form = getattr(action_forms, form_name)(data=data)
        ajax_data_func = getattr(form, "ajax_data", None)
        return HttpResponse(json.dumps(ajax_data_func() if ajax_data_func else None))
    return redirect("action_detail", action_slug=action.slug)
    
def _default_action_vars(action, user):
    users_completed = User.objects.filter(useractionprogress__action=action, 
        useractionprogress__is_completed=1)[:5]
    noshow_users_completed = action.users_completed - users_completed.count()
    users_committed = User.objects.filter(useractionprogress__action=action, 
        useractionprogress__date_committed__isnull=False)[:5]
    noshow_users_committed = action.users_committed - users_committed.count()
    progress = None
    if user.is_authenticated():
        try:
            progress = UserActionProgress.objects.get(action=action, user=user)
            if progress.date_committed:
                days_till_commitment = progress.date_committed - datetime.date.today()
                days_till_commitment = days_till_commitment.days if days_till_commitment.days > 0 else 0
        except UserActionProgress.DoesNotExist: pass
    default_vars = dict(locals())
    del default_vars["action"]
    del default_vars["user"]
    return default_vars
    
def _build_action_form_vars(action, user):
    forms = {}
    for form in action.action_forms_with_data(user):
        data = json.loads(form.data) if form.data else None
        forms[form.var_name] = getattr(action_forms, form.form_name)(data=data)
    return forms