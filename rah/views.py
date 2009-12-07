from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404

from rah.models import Action, ActionCat, ActionStatus, Profile
from rah.forms import RegistrationForm, SignupForm, InquiryForm, ActionStatusForm

def index(request):
    """
    Home Page
    """
    # If the user is logged in, show them the logged in homepage and bail
    if request.user.is_authenticated():
        # Get a list of relevant actions

        # Get a list of completed actions

        # Get a list of the user's earned points
        
        return render_to_response('rah/home_logged_in.html', {}, context_instance=RequestContext(request))
    
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
            return HttpResponseRedirect("/")
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
    
    # If there is a logged in user, grab their status for each action, else, just grab the actions
    if(request.user.is_authenticated()):
        actions = Action.objects.filter(category=cat.id).extra(
                    select_params = (request.user.id,),
                    select = { 'user_status': ' SELECT rah_actionstatus.status \
                                                FROM rah_actionstatus \
                                                WHERE rah_actionstatus.user_id = %s AND \
                                                rah_actionstatus.action_id = rah_action.id' }
                  )
    else:
        actions = Action.objects.filter(category=cat.id)
        
    return render_to_response('rah/action_cat.html', {'cat': cat, 'actions': actions}, context_instance=RequestContext(request))

def action_detail(request, catSlug, actionSlug):
    """Detail page for an action"""
    # Lookup the action
    action = get_object_or_404(Action, slug=actionSlug)

    # Process the status update is form is POSTed
    if request.method == 'POST':
        form = ActionStatusForm(request.POST)
        if form.is_valid():
            # If the form is valid, look for an existing ActionStatus object before creating a new one
            try:
                st = ActionStatus.objects.get(user=request.user, action=action)
            except Exception, e:
                ActionStatus.objects.create(user=request.user, action=action, status=form.cleaned_data["status"])
            else:
                st.status = form.cleaned_data["status"]
                st.save()
    else:
        form = ActionStatusForm()
    
    # Lookup the user's status for this action
    try:
        status = ActionStatus.objects.get(user=request.user.id, action=action.id)
    except:
        status = False
    
    return render_to_response('rah/action_detail.html', {
                                'action': action, 
                                'status': status,
                                'form'  : form
                              }, context_instance=RequestContext(request))

def profile(request, username):
    """docstring for profile"""
    user = User.objects.get(username=username)
    profile = user.get_profile()
    return render_to_response('rah/profile.html', {'profile': profile,}, context_instance=RequestContext(request))
    
def inquiry(request):
    """docstring for inquiry"""
    if request.method == 'POST':
        form = InquiryForm(request.POST, instance=request.user.get_profile())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/%s/" % (request.user.username))
    else:
        form = InquiryForm(instance=request.user.get_profile())
    return render_to_response('rah/inquiry.html', {'form': form,}, context_instance=RequestContext(request))

