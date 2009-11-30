from django import forms
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect


def index(request):
    """
    Home Page
    """
    # If the user is not logged in, show them the logged out homepage and bail
    if not request.user.is_authenticated():
        return render_to_response('rah/home_logged_out.html')
    
    # Get a list of relevant actions
    
    # Get a list of completed actions
    
    # Get a list of the user's earned points
    
    
    
    return render_to_response('rah/home_logged_in.html', {}, context_instance=RequestContext(request))

@csrf_protect
def register(request):
    from www.rah.forms import RegistrationForm
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            user = auth.authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password1"])
            auth.login(request, user)
            return HttpResponseRedirect("/")
    else:
        form = RegistrationForm()
    return render_to_response("registration/register.html", {
        'form': form,
    }, context_instance=RequestContext(request))

def actionBrowse(request):
    """docstring for action"""
    return render_to_response('rah/actionBrowse.html')

def actionCat(request, catSlug):
    """docstring for actionCat"""
    return render_to_response('rah/actionCat.html')

def actionDetail(request, catSlug, actionSlug):
    """docstring for actionDetail"""
    return render_to_response('rah/actionDetail.html')