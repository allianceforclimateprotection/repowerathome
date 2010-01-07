from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib import auth
from django.contrib.comments.views import comments
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.forms.formsets import formset_factory
from rah.models import *
from rah.forms import *
import json

@csrf_protect
def index(request):
    """
    Home Page
    """
    # If the user is logged in, show them the logged in homepage and bail
    if request.user.is_authenticated():
        recommended, in_progress = Action.objects.with_tasks_for_user(request.user)[1:3]
        points = request.user.get_latest_points(5)
        total_points = request.user.get_total_points()
        
        return render_to_response('rah/home_logged_in.html', {
            'points': points,
            'total_points': total_points,
            'in_progress': in_progress,
            'recommended': recommended,
            'house_party_form': HousePartyForm(),
        }, context_instance=RequestContext(request))
    
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
        
    return render_to_response('rah/home_logged_in.html', {}, context_instance=RequestContext(request))

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            # OPTIMIZE: authentication logic can be moved to the RegistrationForm
            user = auth.authenticate(username=form.cleaned_data["email"], password=form.cleaned_data["password1"])
            auth.login(request, user)
            # OPTIMIZE: profile create can be abstracted as a post_save signal [eg. models.signals.post_save.connect(some_profile_create_func, sender=User)]
            Profile.objects.create(user=user)
            
            # If this is an ajax request, then return the new user ID
            if request.is_ajax:
                return HttpResponse(json.dumps({'valid': True, 'userid': user.id }))
            
            return redirect('rah.views.profile_edit', user_id=user.id)
        elif request.is_ajax:
            # This should never happen if the client side validation is working properly
            return HttpResponse(json.dumps({'valid': False, 'errors': eval(repr(form.errors)) }))
    else:
        form = RegistrationForm()
        profileForm = ProfileEditForm()
    return render_to_response("registration/register.html", {
        'form': form,
        'profileForm': profileForm,
    }, context_instance=RequestContext(request))

def action_show(request):
    """Show all actions by Category"""
    actions = Action.objects.with_tasks_for_user(request.user)[0]
    categories = dict([(action.category, []) for action in actions]) #create a new map of categories to empty lists
    [categories[action.category].append(action) for action in actions] #append each action to the its assocaited categor list
    return render_to_response('rah/action_show.html', {'categories': categories}, context_instance=RequestContext(request))

def action_detail(request, action_slug):
    """Detail page for an action"""
    # Lookup the action
    action = get_object_or_404(Action, slug=action_slug)
    action_tasks = ActionTask.get_action_tasks_by_action_and_user(action, request.user)
    users_in_progress, users_completed = User.objects.with_completes_for_action(action)[1:3]
    
    return render_to_response('rah/action_detail.html', {
                                'action': action,
                                'action_tasks': action_tasks,
                                'users_in_progress': users_in_progress,
                                'users_completed': users_completed
                              }, context_instance=RequestContext(request))
                              
def action_task(request, action_task_id):
    #  Handle the POST if a task is being completed
    # OPTIMIZE There are some extra queries going on here
    action_task = get_object_or_404(ActionTask, id=action_task_id)
    if request.method == 'POST' and request.user.is_authenticated():
        user_action_task, created = UserActionTask.objects.get_or_create(user=request.user, action_task=action_task)
        if request.POST.get('task_completed'):
            Points.give(user=request.user, reason=action_task, points=action_task.points)
        else:
            user_action_task.delete()
            Points.take(user=request.user, reason=action_task)
    
    if request.is_ajax():
        return HttpResponse(action_task.action.completes_for_user(request.user))
    else:
        return redirect('rah.views.action_detail', action_slug=action_task.action.slug)

def profile(request, user_id):
    """docstring for profile"""
    user = get_object_or_404(User, id=user_id)
    is_profile_viewable = request.user <> user and user.get_profile().is_profile_private
    profile = user.get_profile()
    recommended, in_progress, completed = Action.objects.with_tasks_for_user(user)[1:4]
    points = user.get_latest_points()
    total_points = user.get_total_points()
    
    return render_to_response('rah/profile.html', {
        'profile': profile,
        'points': points,
        'total_points': total_points,
        'in_progress': in_progress,
        'recommended': recommended,
        'completed': completed,
        'is_others_profile': request.user <> user,
        'is_profile_viewable': is_profile_viewable,
    }, context_instance=RequestContext(request))

@login_required
def profile_edit(request, user_id):
    """docstring for inquiry"""
    if request.user.id <> int(user_id):
        return HttpResponseForbidden("Sorry, but you do not have permissions to edit this profile.")
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user.get_profile())
        if form.is_valid():
            form.save()
            # If the user just registered go to the home page
            if "/register/" in str(request.META.get('HTTP_REFERER')):
                return redirect('rah.views.index')
            # Else we go to the profile view page
            else:
                return redirect('rah.views.profile', user_id=request.user.id)
    else:
        profile = request.user.get_profile()
        initial = {'firstname': request.user.first_name,
            'lastname': request.user.last_name,
            'zipcode': profile.location.zipcode if profile.location else ''}
        form = ProfileEditForm(instance=profile, initial=initial)
    return render_to_response('rah/profile_edit.html', {'form': form,}, context_instance=RequestContext(request))
    
@login_required
def account(request):
    """
    The account view is used to generate and accept a form used by the user to update their registration specific details
    """
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('rah.views.index')
    else:
        profile = request.user.get_profile()
        form = AccountForm(instance=request.user, initial={ 'make_profile_private': profile.is_profile_private, })
    return render_to_response('rah/account.html', {'form': form,}, context_instance=RequestContext(request))

@csrf_protect
def feedback(request):
    """docstring for feedback"""
    success = False
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()
            
            # Add the logged in user to the record
            if request.user.is_authenticated():
                feedback.user = request.user
                feedback.save()
            
            # TODO Replace this success business with a message when messaging is ready
            success = True
    else:
        form = FeedbackForm(initial={ 'url': request.META.get('HTTP_REFERER'), })
    
    if request.is_ajax():
        template = 'rah/_feedback.html'
    else:
        template = 'rah/feedback.html'
        
    return render_to_response(template, {
        'feedback_form': form,
        'success': success,
    }, context_instance=RequestContext(request))

def validate_field(request):
    """The jQuery Validation plugin will post a single form field to this view and expects a json response."""
    # Must be called with an AJAX request
    if not request.is_ajax():
        return HttpResponseForbidden()
    
    valid = False

    # Valid if there are no other users using that email address
    if request.POST.get("email"):
        from django.forms.fields import email_re # OPTIMIZE Is it ok to have imports at the function level?
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
            # TODO set some sort of success message
            pass
        else:
            # TODO set some sort of failure message
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
    return comments.post_comment(request, next, using)
    
def forbidden(request, message="You do not have permissions."):
    return render_to_response('403.html', {'message':message}, context_instance=RequestContext(request))