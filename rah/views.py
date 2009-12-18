from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib import auth
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.forms.formsets import formset_factory
from rah.models import *
from rah.forms import *

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
            Profile.objects.create(user=user)
            return redirect('www.rah.views.profile_edit', user_id=user.id)
    else:
        form = RegistrationForm()
    return render_to_response("registration/register.html", {
        'form': form,
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
    
    return render_to_response('rah/action_detail.html', {
                                'action': action,
                                'action_tasks': action_tasks
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
        return redirect('www.rah.views.action_detail', action_slug=action_task.action.slug)

def profile(request, user_id):
    """docstring for profile"""
    user = get_object_or_404(User, id=user_id)
    if request.user <> user and user.get_profile().is_profile_private:
        return HttpResponseForbidden()
    profile = user.get_profile()
    recommended, in_progress, completed = Action.objects.with_tasks_for_user(request.user)[1:4]
    points = request.user.get_latest_points()
    total_points = request.user.get_total_points()
    
    return render_to_response('rah/profile.html', {
        'profile': profile,
        'points': points,
        'total_points': total_points,
        'in_progress': in_progress,
        'recommended': recommended,
        'completed': completed,
    }, context_instance=RequestContext(request))

@login_required
def profile_edit(request, user_id):
    """docstring for inquiry"""
    if request.user.id <> int(user_id):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user.get_profile())
        if form.is_valid():
            form.save()
            return redirect('www.rah.views.profile', user_id=request.user.id)
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
            return redirect('www.rah.views.index')
    else:
        profile = request.user.get_profile()
        form = AccountForm(instance=request.user, initial={ 'make_profile_private': profile.is_profile_private, })
    return render_to_response('rah/account.html', {'form': form,}, context_instance=RequestContext(request))

