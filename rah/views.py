import json, logging
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.comments.views import comments
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.forms.formsets import formset_factory
from django.contrib import messages
from rah.models import *
from rah.forms import *
from settings import GA_TRACK_PAGEVIEW
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
    dict = {}
    dict['action'] = get_object_or_404(Action, slug=action_slug)
    dict['action_tasks'] = dict['action'].get_action_tasks_by_user(request.user)
    dict['num_users_in_progress'], dict['show_users_in_progress'], dict['num_users_completed'], dict['show_users_completed'] = dict['action'].users_with_completes(5)
    
    dict['num_noshow_users_in_progress'] = dict['num_users_in_progress'] - len(dict['show_users_in_progress'])
    dict['num_noshow_users_completed'] = dict['num_users_completed'] - len(dict['show_users_completed'])
    
    return render_to_response('rah/action_detail.html', dict, context_instance=RequestContext(request))
                              
def action_task(request, action_task_id):
    #  Handle the POST if a task is being completed
    # OPTIMIZE There are some extra queries going on here
    action_task = get_object_or_404(ActionTask, id=action_task_id)
    if request.method == 'POST' and request.user.is_authenticated():
        record = Record.objects.filter(user=request.user, activity=action_task)
        if request.POST.get('task_completed') and not record:
            request.user.record_activity(action_task)
            messages.success(request, 'Great work, we have updated our records to show you completed %s' % (action_task))
        else:
            request.user.unrecord_activity(action_task)
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
    chart_points = user.get_chart_data()
    point_data = [(chart_point.get_date_as_milli_from_epoch(), chart_point.points) for chart_point in chart_points]
    
    tooltips = [tooltip_template.render(Context({"records": chart_point.records})) for chart_point in chart_points]
    logging.debug("point data: %s" % point_data)
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
    }, context_instance=RequestContext(request))

@login_required
def profile_edit(request, user_id):
    if request.user.id <> int(user_id):
        return forbidden(request, "Sorry, but you do not have permissions to edit this profile.")
    if request.method == 'POST':
        # If the user just registered go to the home page
        post_reg = True if ("/register/" in str(request.META.get('HTTP_REFERER'))) else False
        profile_form = ProfileEditForm(request.POST, instance=request.user.get_profile())
        account_form = AccountForm(request.POST, instance=request.user)
        if profile_form.is_valid() and (account_form.is_valid() or post_reg):
            profile_form.save()
            account_form.save() if not post_reg else False
            if post_reg:
                return redirect('rah.views.index')
            messages.add_message(request, messages.SUCCESS, 'Your profile has been updated.')
            return redirect('rah.views.profile_edit', user_id=request.user.id)
    else:
        profile      = request.user.get_profile()
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
def feedback(request):
    """docstring for feedback"""
    success = False
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
            success = True
    else:
        form = FeedbackForm(initial={ 'url': request.META.get('HTTP_REFERER'), })
    
    
    if request.is_ajax():
        if request.method == 'POST':
            message_html = loader.render_to_string('_messages.html', {}, RequestContext(request))
            return HttpResponse(message_html)
        template = 'rah/_feedback.html'
    else:
        template = 'rah/feedback.html'
        
    return render_to_response(template, { 'feedback_form': form, 'success': success, }, context_instance=RequestContext(request))

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
            request.user.record_activity(Activity.objects.get(name="house-party"))
            messages.add_message(request, messages.SUCCESS, 'Thanks! We will be in touch soon.')
        else:
            pass
    return redirect('rah.views.index')

def invite_friend(request):
    if request.method == 'POST':
        form = InviteFriendForm(request.POST)
        if form.is_valid() and form.send(request.user):
            request.user.record_activity(Activity.objects.get(name="friend-invite"))
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
    
def forbidden(request, message="You do not have permissions."):
    from django.http import HttpResponseForbidden
    return HttpResponseForbidden(loader.render_to_string('403.html', { 'message':message, }, RequestContext(request)))