from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_protect

from tagging.models import Tag
from records.models import Record

from models import Action, UserActionProgress
from forms import ActionForm

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
    action_form = ActionForm(user=request.user, action=action, 
        data=(request.POST or None))
    if request.method == 'POST':
        if action_form.is_valid():
            action_form.save()
            redirect("action_detail", action_slug=action.slug)
    users_completed = User.objects.filter(useractionprogress__action=action, 
        useractionprogress__is_completed=1)[:5]
    noshow_users_completed = action.users_completed - users_completed.count()
    users_committed = User.objects.filter(useractionprogress__action=action, 
        useractionprogress__date_committed__isnull=False)[:5]
    noshow_users_committed = action.users_committed - users_committed.count()
    progress = request.user.get_action_progress(action) if \
        request.user.is_authenticated() else None
    return render_to_response("actions/action_detail.html", locals(), 
        context_instance=RequestContext(request))

@csrf_protect
@login_required
def action_commit(request, action_slug):
    action = get_object_or_404(Action, slug=action_slug)
    action_form = ActionForm(user=request.user, action=action, 
        data=(request.POST or None))
    if request.method == 'POST':
        if action_form.is_valid():
            action_form.save()
            redirect("action_detail", action_slug=action.slug)
    progress = request.user.get_action_progress(action)
    return render_to_response('actions/action_commit.html', locals(), 
        context_instance=RequestContext(request))