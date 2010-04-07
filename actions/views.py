from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_protect

from tagging.models import Tag
from records.models import Record

from models import Action, UserActionProgress
from forms import ActionCommitForm

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
    vars = _default_action_vars(action, request.user)
    action_commit_form = ActionCommitForm(user=request.user, action=action)
    vars.update(locals())
    return render_to_response("actions/action_detail.html", vars, RequestContext(request))
        
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
    vars = _default_action_vars(action, request.user)
    vars.update(locals())
    return render_to_response("actions/action_detail.html", vars, RequestContext(request))
    
@login_required
@csrf_protect
def action_cancel(request, action_slug):
    action = get_object_or_404(Action, slug=action_slug)
    if request.method == "POST":    
        if action.cancel_for_user(request.user):
            messages.success(request, "Sorry to see you can not make the commitment.")
        return redirect("action_detail", action_slug=action.slug)
    return render_to_response("actions/action_cancel.html", locals(), RequestContext(request))
    
def _default_action_vars(action, user):
    users_completed = User.objects.filter(useractionprogress__action=action, 
        useractionprogress__is_completed=1)[:5]
    noshow_users_completed = action.users_completed - users_completed.count()
    users_committed = User.objects.filter(useractionprogress__action=action, 
        useractionprogress__date_committed__isnull=False)[:5]
    noshow_users_committed = action.users_committed - users_committed.count()
    try:
        progress = UserActionProgress.objects.get(action=action, user=user)
    except UserActionProgress.DoesNotExist:
        progress = None
    # TODO: Don't use vars as a variable name. It's a python built-in
    vars = dict(locals())
    del vars["action"]
    del vars["user"]
    return vars 