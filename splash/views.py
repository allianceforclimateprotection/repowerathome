from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django import forms
from www.splash.forms import SignupForm
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def index(request):
    """
    Home Page
    """
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/?signup=success")
    else:
        form = SignupForm()
    return render_to_response("splash/index.html", {
        'form': form,
    }, context_instance=RequestContext(request))