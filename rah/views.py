import json, logging

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import auth
from django.contrib.comments.views import comments
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.forms.formsets import formset_factory
from django.contrib import messages
from django.contrib.sites.models import Site

from rah.models import *
from records.models import *
from rah.forms import *
from settings import GA_TRACK_PAGEVIEW
from geo.models import Location
from twitter_app.forms import StatusForm as TwitterStatusForm

@csrf_protect
def index(request):
    """
    Home Page
    """
    # If the user is logged in, show them the logged in homepage and bail
    if request.user.is_authenticated():
        return profile(request, request.user.id)
    
    # Setup and handle email form on logged out home page
    success = False
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            success = True
    else:
        form = SignupForm()
    return render_to_response("rah/home_logged_out.html", {
        'form': form,
        'success': success
    }, context_instance=RequestContext(request))
    
def logout(request):
    response = auth.logout(request)
    messages.success(request, "You have successfully logged out.", extra_tags="sticky")
    return redirect("index")
    
def password_change_done(request):
    messages.success(request, "Your password was changed successfully.", extra_tags="sticky")
    return redirect("profile_edit", user_id=request.user.id)
    
def password_reset_done(request):
    messages.success(request, "We just sent you an email with instructions for resetting your password.", extra_tags="sticky")
    return redirect("index")
    
def password_reset_complete(request):
    messages.success(request, "Password reset successfully!", extra_tags="sticky")
    return redirect("index")

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            user = auth.authenticate(username=form.cleaned_data["email"], password=form.cleaned_data["password1"])
            auth.login(request, user)
            
            # Add the location to profile if the user registered with one
            if "location" in form.cleaned_data:
                profile = user.get_profile()
                profile.location = form.cleaned_data["location"]
                profile.save()
            
            messages.success(request, 'Thanks for registering.')
            messages.add_message(request, GA_TRACK_PAGEVIEW, '/register/complete')
            
            return redirect("index")
    else:
        form = RegistrationForm()
    return render_to_response("registration/register.html", {
        'form': form,
    }, context_instance=RequestContext(request))

def action_show(request):
    """Show all actions by Category"""
    actions = Action.objects.actions_by_completion_status(request.user)[0]
    categories = dict([(action.category, []) for action in actions]) #create a new map of categories to empty lists
    [categories[action.category].append(action) for action in actions] #append each action to the its assocaited categor list
    return render_to_response('rah/action_show.html', {'categories': categories}, context_instance=RequestContext(request))

def action_detail(request, action_slug):
    """Detail page for an action"""
    # Lookup the action
    action = get_object_or_404(Action, slug=action_slug)
    action_tasks = action.get_action_tasks_by_user(request.user)
    
    num_users_in_progress, show_users_in_progress, num_users_completed, show_users_completed = action.users_with_completes(5)
    
    num_noshow_users_in_progress = num_users_in_progress - len(show_users_in_progress)
    num_noshow_users_completed = num_users_completed - len(show_users_completed)
    
    progress = request.user.get_action_progress(action) if request.user.is_authenticated() else None
    commit_form = ActionCommitForm()
    
    return render_to_response('rah/action_detail.html', locals(), context_instance=RequestContext(request))

@login_required
def action_task(request, action_task_id):
    #  Handle the POST if a task is being completed
    action_task = get_object_or_404(ActionTask, id=action_task_id)
    if request.method == 'POST':
        record = ActionTaskUser.objects.filter(user=request.user, actiontask=action_task)

        if request.POST.get('task_completed') and not record:
            action_task.complete_task(request.user)
            Record.objects.create_record(request.user, 'action_task_complete', action_task)
            messages.success(request, 'Great work, we have updated our records to show you completed %s' % (action_task))
        else:
            action_task.complete_task(request.user, undo=True)
            Record.objects.void_record(request.user, 'action_task_complete', action_task)
            messages.success(request, 'We have updated our records to show you have not completed %s' % (action_task))
    
    if request.is_ajax():
        message_html = loader.render_to_string('_messages.html', {}, RequestContext(request))
        dict = { 'completed_tasks': action_task.action.completes_for_user(request.user), 'message_html': message_html }
        return HttpResponse(json.dumps(dict))
    else:
        return redirect('rah.views.action_detail', action_slug=action_task.action.slug)

def profile(request, user_id):
    """docstring for profile"""
    user = request.user if request.user.id is user_id else get_object_or_404(User, id=user_id)
    if request.user <> user and user.get_profile().is_profile_private:
        return forbidden(request, "Sorry, but you do not have permissions to view this profile.")
        
    recommended, in_progress, completed = Action.objects.actions_by_completion_status(user)[1:4]
    twitter_form = TwitterStatusForm(initial={
        "status":"I'm saving money and having fun with @repowerathome. Check out http://repowerathome.com"
    })
    tooltip_template = loader.get_template("rah/_chart_tooltip.html")
    chart_points = Record.objects.get_chart_data(user)
    point_data = [(chart_point.get_date_as_milli_from_epoch(), chart_point.points) for chart_point in chart_points]
    tooltips = [tooltip_template.render(Context({"records": chart_point.records})) for chart_point in chart_points]
    return render_to_response('rah/profile.html', {
        'total_points': user.get_profile().total_points,
        'in_progress': in_progress,
        'completed': completed,
        'recommended': recommended[:6], # Hack to only show 6 "recommended" actions
        'house_party_form': HousePartyForm(),
        'invite_friend_form': InviteFriendForm(),
        'twitter_status_form': twitter_form,
        'chart_data': json.dumps({"point_data": point_data, "tooltips": tooltips}),
        'profile': user.get_profile(),
        'is_others_profile': request.user <> user,
        'commitment_list': user.get_commit_list(),
        'my_groups': user.my_groups(),
        'records': Record.objects.user_records(user, 10),
    }, context_instance=RequestContext(request))

@login_required
def profile_edit(request, user_id):
    if request.user.id <> int(user_id):
        return forbidden(request, "Sorry, but you do not have permissions to edit this profile.")
    
    profile = request.user.get_profile()
    if request.method == 'POST':
        profile_form = ProfileEditForm(request.POST, instance=profile)
        account_form = AccountForm(request.POST, instance=request.user)
        if profile_form.is_valid() and account_form.is_valid():
            profile_form.save()
            account_form.save()
            messages.add_message(request, messages.SUCCESS, 'Your profile has been updated.')
    else:
        account_form = AccountForm(instance=request.user)
        profile_form = ProfileEditForm(instance=profile, initial={
            'zipcode': profile.location.zipcode if profile.location else '',
        })

    return render_to_response('rah/profile_edit.html', {
        'profile_form': profile_form,
        'account_form': account_form,
        'profile': profile,
    }, context_instance=RequestContext(request))

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
            messages.add_message(request, messages.SUCCESS, 'We recorded your commitment.')
            return redirect("action_detail", action_slug=action.slug)
    else:
        initial = {'date_committed': progress.date_committed} if progress else None
        commit_form = ActionCommitForm(initial=initial)
    
    return render_to_response('rah/action_commit.html', {
        'action': action,
        'commit_form': commit_form,
    }, context_instance=RequestContext(request))

@csrf_protect
def feedback(request):
    """docstring for feedback"""
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()
            form.send(request.user)
            
            # Add the logged in user to the record
            if request.user.is_authenticated():
                feedback.user = request.user
                feedback.save()
                
            messages.success(request, 'Thank you for the feedback.')
    else:
        form = FeedbackForm(initial={ 'url': request.META.get('HTTP_REFERER'), })
    
    if request.is_ajax():
        if request.method == 'POST':
            message_html = loader.render_to_string('_messages.html', {}, RequestContext(request))
            return HttpResponse(message_html)
        template = 'rah/_feedback.html'
    else:
        template = 'rah/feedback.html'
        
    return render_to_response(template, { 'feedback_form': form, }, context_instance=RequestContext(request))

def validate_field(request):
    """The jQuery Validation plugin will post a single form field to this view and expects a json response."""
    # Must be called with an AJAX request
    if not request.is_ajax():
        return forbidden(request)
    
    valid = False

    # Valid if there are no other users using that email address
    if request.POST.get("email"):
        from django.core.validators import email_re # OPTIMIZE Is it ok to have imports at the function level?
        if email_re.search(request.POST.get("email")) and not User.objects.filter(email__exact = request.POST.get("email")):
            valid = True
        if request.user.is_authenticated() and request.user.email == request.POST.get("email"):
            valid = True
    
    # Valid if zipcode is in our location table
    elif request.POST.get("zipcode"):
        if request.POST.get("zipcode").isdigit() and len(request.POST.get("zipcode")) == 5:
            location = Location.objects.filter(zipcode__exact = request.POST.get("zipcode"))
            if location:
                valid = True
    
    return HttpResponse(json.dumps(valid))
    
def house_party(request):
    if request.method == 'POST':
        form = HousePartyForm(request.POST)
        if form.is_valid() and form.send(request.user):
            Record.objects.create_record(request.user, 'mag_request_party_host_info')
            messages.add_message(request, messages.SUCCESS, 'Thanks! We will be in touch soon.')
        else:
            pass
    return redirect('rah.views.index')

def invite_friend(request):
    if request.method == 'POST':
        form = InviteFriendForm(request.POST)
        if form.is_valid() and form.send(request.user):
            Record.objects.create_record(request.user, 'mag_invite_friend')
            messages.add_message(request, messages.SUCCESS, 'Invitation sent. Thanks!')
        else:
            pass
    return redirect('rah.views.index')


def search(request):
    return render_to_response('rah/search.html', {}, context_instance=RequestContext(request))

@login_required
@require_POST
def post_comment(request, next=None, using=None):
    """
    wrapper view around the django.contrib.comments post_comment view, this way if a user specifies their name in a comment,
    we can capture it and use it to update their profile
    """
    name = request.POST.get('name')
    if name and request.user.get_full_name() == '':
        request.user.first_name = name
        request.user.save()
    response = comments.post_comment(request, next, using)
    messages.add_message(request, messages.SUCCESS, 'Thanks for the comment.')
    return response
    
@login_required
@csrf_protect
def group_create(request):
    """
    create a form a user can use to create a custom group, on POST save this group to the database
    and automatically add the creator to the said group as a manager.
    """
    if request.method == "POST":
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save()
            GroupUsers.objects.create(group=group, user=request.user, is_manager=True)
            Record.objects.create_record(request.user, 'group_create', group)
            messages.success(request, "%s has been created." % group)
            return redirect("group_detail", group_slug=group.slug) # TODO: after creating the group we should redirect the user to the group detail page
    else:
        form = GroupForm()
    return render_to_response("rah/group_create.html", {"form": form, "site": Site.objects.get_current()}, context_instance=RequestContext(request))
    
@login_required
def group_leave(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.user in group.users.all():
        GroupUsers.objects.filter(group=group, user=request.user).delete()
        messages.success(request, "You have been removed from group %s" % group)
    else:
        messages.error(request, "You can not leave a group your not a member of")
    return redirect("group_detail", group_slug=group.slug)
    
@login_required
def group_join(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if GroupUsers.objects.filter(group=group, user=request.user).exists():
        messages.error(request, "You are already a member")
        return redirect("group_detail", group_slug=group.slug)
    if MembershipRequests.objects.filter(group=group, user=request.user).exists():
        messages.error(request, "Your membership is currently pending")
        return redirect("group_detail", group_slug=group.slug)
    if group.is_public():
        GroupUsers.objects.create(group=group, user=request.user, is_manager=False)
        messages.success(request, "You have successfully joined group %s" % group, extra_tags="sticky")
    else:
        template = loader.get_template("rah/group_join_request.html")
        context = { "user": request.user, "group": group, "domain": Site.objects.get_current().domain, }
        manager_emails = [user_dict["email"] for user_dict in User.objects.filter(group=group, groupusers__is_manager=True).values("email")]
        try:
            send_mail("Group Join Request", template.render(Context(context)), None, manager_emails, fail_silently=False)
            MembershipRequests.objects.create(group=group, user=request.user)
            messages.success(request, "You have made a request to join %s, a manager should grant or deny your membership shortly." % group, extra_tags="sticky")
        except SMTPException, e:
            messages.error(request, "A problem occured, if this persits please contact feedback@repowerathome.com", extra_tags="sticky")
    return redirect("group_detail", group_slug=group.slug)

@login_required    
def group_membership(request, group_id, user_id, action):
    group = get_object_or_404(Group, id=group_id)
    user = get_object_or_404(User, id=user_id)
    if not request.user.is_group_manager(group):
        messages.errors(request, "You do not have permissions")
        return redirect("group_detail", group_slug=group.slug)
    membership_request = MembershipRequests.objects.filter(group=group, user=user)
    if membership_request:
        if action == "approve":
            GroupUsers.objects.create(group=group, user=user, is_manager=False)
            membership_request.delete()
            messages.success(request, "%s has been added to the group" % user)
            # TODO: also create a message for the approved user
        elif action == "deny":
            membership_request.delete()
            messages.success(request, "%s has been denied access to the group" % user)
            # TODO: also create a message for the denied user
    else:
        messages.errors(request, "%s has not requested to join this group" % user)
    return redirect("group_detail", group_slug=group.slug)

def group_detail(request, group_slug):
    """
    display all of the information about a particular group
    """
    group = get_object_or_404(Group, slug=group_slug)
    return _group_detail(request, group)
    
def geo_group(request, state, county_slug=None, place_slug=None):
    geo_group = GeoGroup.objects.get_geo_group(state, county_slug, place_slug)
    if not geo_group:
        raise Http404
    return _group_detail(request, geo_group)
    
def group_list(request):
    """
    display a listing of the groups
    """
    new_groups = Group.objects.new_groups_with_memberships(request.user)
    return render_to_response("rah/group_list.html", locals(), context_instance=RequestContext(request))
        
def _group_detail(request, group):
    popular_actions = group.completed_actions_by_user()
    top_members = group.members_ordered_by_points()
    group_records = group.group_records(10)
    is_member = group.is_member(request.user)
    membership_pending = group.has_pending_membership(request.user)
    requesters = group.requesters_to_grant_or_deny(request.user)
    return render_to_response("rah/group_detail.html", locals(), context_instance=RequestContext(request))
    
def forbidden(request, message="You do not have permissions."):
    from django.http import HttpResponseForbidden
    return HttpResponseForbidden(loader.render_to_string('403.html', { 'message':message, }, RequestContext(request)))