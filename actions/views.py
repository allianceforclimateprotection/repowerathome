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
    return render_to_response("actions/action_show.html", locals(), context_instance=RequestContext(request))

def action_detail(request, action_slug):
    """Detail page for an action"""
    action = get_object_or_404(Action, slug=action_slug)
    users_completed = User.objects.filter(useractionprogress__action=action, useractionprogress__is_completed=1)[:5]
    noshow_users_completed = action.users_completed - users_completed.count()
    users_committed = User.objects.filter(useractionprogress__action=action, useractionprogress__date_committed__isnull=False)[:5]
    noshow_users_committed = action.users_committed - users_committed.count()
    progress = request.user.get_action_progress(action) if request.user.is_authenticated() else None
    commit_form = ActionCommitForm()
    return render_to_response("actions/action_detail.html", locals(), context_instance=RequestContext(request))

@csrf_protect
@login_required
def action_commit(request, action_slug):
    action = get_object_or_404(Action, slug=action_slug)
    progress = request.user.get_action_progress(action)
    if request.method == 'POST':
        commit_form = ActionCommitForm(request.POST)
        if commit_form.is_valid():
            commit_form.save(action, request.user)
            data = {'date_committed': commit_form.cleaned_data['date_committed']}
            Record.objects.create_record(request.user, 'action_commitment', action, data=data)
            messages.add_message(request, messages.SUCCESS, 'We updated your commitment successfully')
            return redirect("action_detail", action_slug=action.slug)
    else:
        initial = {'date_committed': progress.date_committed} if progress else None
        commit_form = ActionCommitForm(initial=initial)

    return render_to_response('actions/action_commit.html', {
        'action': action,
        'commit_form': commit_form,
    }, context_instance=RequestContext(request))

