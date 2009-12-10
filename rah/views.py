from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.forms.formsets import formset_factory
from django.db.models import Sum
from rah.models import *
from rah.forms import *

def index(request):
    """
    Home Page
    """
    # If the user is logged in, show them the logged in homepage and bail
    if request.user.is_authenticated():
        # Get a list of relevant actions
        action_recs = Action.objects.select_related().all()[:5]

        # Get a list of actions in progress
        in_progress = UserActionTask.objects.select_related().filter(user=request.user)
        
        # Get a list of points earned by this user and their total points
        points = Points.objects.filter(user=request.user)[:10]
        total_points = Points.objects.filter(user=request.user).aggregate(Sum('points'))['points__sum']
        
        return render_to_response('rah/home_logged_in.html', {
            'points': points,
            'total_points': total_points,
            'in_progress': in_progress,
            'action_recs': action_recs,
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
            user = auth.authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password1"])
            auth.login(request, user)
            Profile.objects.create(user=user)
            return redirect('www.rah.views.index')
    else:
        form = RegistrationForm()
    return render_to_response("registration/register.html", {
        'form': form,
    }, context_instance=RequestContext(request))

def action_browse(request):
    """Browse all actions by category"""
    cats = ActionCat.objects.all()
    return render_to_response('rah/action_browse.html', {'cats':cats}, context_instance=RequestContext(request))

def action_cat(request, catSlug):
    """View an action category page with links to actions in that category"""
    cat     = get_object_or_404(ActionCat, slug=catSlug)
    actions = Action.objects.filter(category=cat.id)
        
    return render_to_response('rah/action_cat.html', {'cat': cat, 'actions': actions}, 
                                context_instance=RequestContext(request))

def action_detail(request, catSlug, actionSlug):
    """Detail page for an action"""
    # Lookup the action
    action = get_object_or_404(Action, slug=actionSlug)
    
    #  Handle the POST if a task is being completed and task_id is an integer
    if request.method == 'POST' and request.POST.get('task_id').isdigit():
        try:
            # Look for a row in UserActionTask table and delete it if task_completed is unchecked
            user_action_task = UserActionTask.objects.get(user=request.user, action_task=request.POST.get('task_id'))
            if request.POST.get('task_completed') == None:
                user_action_task.delete()
        except:
            # There was no row in UserActionTask, so create one if task_completed is checked
            if request.POST.get('task_completed') == 'on':
                UserActionTask(user=request.user, action_task=ActionTask(pk=request.POST.get('task_id'))).save()
    
    # Get action tasks conditionally depending on whether or not they're logged in
    if(request.user.is_authenticated()):
        # If they're logged in, grab the completed time for any completed tasks
        action_tasks = ActionTask.objects.filter(action=action.id).extra(
            select_params = (request.user.id,), 
            select = { 'completed': 'SELECT rah_useractiontask.completed \
                                     FROM rah_useractiontask \
                                     WHERE rah_useractiontask.user_id = %s AND \
                                     rah_useractiontask.action_task_id = rah_actiontask.id' }
        )
    else:
        action_tasks = ActionTask.objects.filter(action=action.id)
    
    return render_to_response('rah/action_detail.html', {
                                'action': action,
                                'action_tasks': action_tasks
                              }, context_instance=RequestContext(request))

def profile(request, username):
    """docstring for profile"""
    user = get_object_or_404(User, username=username)
    profile = user.get_profile()
    
    # Get a list of points earned by this user and their total points
    points = Points.objects.filter(user=user)[:10]
    total_points = Points.objects.filter(user=user).aggregate(Sum('points'))['points__sum']
    
    return render_to_response('rah/profile.html', {
        'profile': profile,
        'points': points,
        'total_points': total_points,
    }, context_instance=RequestContext(request))

@login_required
def profile_edit(request, username):
    """docstring for inquiry"""
    if request.user.username <> username:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user.get_profile())
        if form.is_valid():
            form.save()
            return redirect('www.rah.views.profile', username=request.user.username)
    else:
        profile = request.user.get_profile()
        form = ProfileEditForm(instance=profile, initial={'zipcode': profile.location.zipcode})
    return render_to_response('rah/profile_edit.html', {'form': form,}, context_instance=RequestContext(request))

