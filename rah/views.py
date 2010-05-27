import json, logging

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import auth
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.comments.views import comments
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext, loader, Context
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.forms.formsets import formset_factory
from django.contrib import messages
from django.contrib.sites.models import Site

from tagging.models import Tag
from actions.models import Action
from rah.models import User, Profile
from records.models import Record
from rah.forms import RegistrationForm, AuthenticationForm, HousePartyForm, AccountForm, ProfileEditForm, GroupNotificationsForm, FeedbackForm
from settings import GA_TRACK_PAGEVIEW, LOGIN_REDIRECT_URL
from geo.models import Location
from twitter_app.forms import StatusForm as TwitterStatusForm
from groups.models import Group
from decorators import save_queued_POST

@csrf_protect
def index(request):
    """
    Home Page
    """
    # If the user is not logged in, show them the logged out homepage and bail
    if not request.user.is_authenticated():
        context = {'house_party_form': HousePartyForm(request.user)}
        return render_to_response("rah/home_logged_out.html", context, context_instance=RequestContext(request))
    
    recommended, committed, completed = Action.objects.actions_by_status(request.user)[1:4]
    twitter_form = TwitterStatusForm(initial={
        "status":"I'm saving money and having fun with @repowerathome. Check out http://repowerathome.com"
    })
    return render_to_response('rah/home_logged_in.html', {
        'total_points': request.user.get_profile().total_points,
        'committed': committed,
        'completed': completed,
        'recommended': recommended[:6], # Hack to only show 6 "recommended" actions
        'house_party_form': HousePartyForm(request.user),
        'twitter_status_form': twitter_form,
        'commitment_list': request.user.get_commit_list(),
        'my_groups': Group.objects.filter(users=request.user, is_geo_group=False),
        'records': Record.objects.user_records(request.user, 10),
    }, context_instance=RequestContext(request))

def privacy_policy(request):
    return render_to_response("rah/privacy_policy.html", {}, context_instance=RequestContext(request))

def terms_of_use(request):
    return render_to_response("rah/terms_of_use.html", {}, context_instance=RequestContext(request))
 
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
    
    redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            user = auth.authenticate(username=form.cleaned_data["email"], password=form.cleaned_data["password1"])
            auth.login(request, user)
            save_queued_POST(request)

            # Add the location to profile if the user registered with one
            if "location" in form.cleaned_data:
                profile = user.get_profile()
                profile.location = form.cleaned_data["location"]
                profile.save()
            
            messages.success(request, 'Thanks for registering.')
            messages.add_message(request, GA_TRACK_PAGEVIEW, '/register/complete')
            
            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
            
            # Heavier security check -- redirects to http://example.com should 
            # not be allowed, but things like /view/?param=http://example.com 
            # should be allowed. This regex checks if there is a '//' *before* a
            # question mark.
            elif '//' in redirect_to and re.match(r'[^\?]*//', redirect_to):
                redirect_to = settings.LOGIN_REDIRECT_URL
                    
            return HttpResponseRedirect(redirect_to)
    else:
        if "email" in request.GET:
            form = RegistrationForm(initial={"email": request.GET["email"]})
        else:
            form = RegistrationForm()
    return render_to_response("registration/register.html", {
        'register_form': form,
        REDIRECT_FIELD_NAME: redirect_to,
        'login_form': AuthenticationForm()
    }, context_instance=RequestContext(request))

@csrf_protect
def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm):
    """Displays the login form and handles the login action."""

    redirect_to = request.REQUEST.get(redirect_field_name, '')
    
    if request.method == "POST":
        form = authentication_form(data=request.POST)
        if form.is_valid():
            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
            
            # Heavier security check -- redirects to http://example.com should 
            # not be allowed, but things like /view/?param=http://example.com 
            # should be allowed. This regex checks if there is a '//' *before* a
            # question mark.
            elif '//' in redirect_to and re.match(r'[^\?]*//', redirect_to):
                    redirect_to = settings.LOGIN_REDIRECT_URL
            
            # Okay, security checks complete. Log the user in.
            auth.login(request, form.get_user())
            save_queued_POST(request)

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return HttpResponseRedirect(redirect_to)

    else:
        form = authentication_form(request)
    
    request.session.set_test_cookie()
    
    if Site._meta.installed:
        current_site = Site.objects.get_current()
    else:
        current_site = RequestSite(request)
    
    return render_to_response(template_name, {
        'login_form': form,
        'register_form': RegistrationForm(),
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }, context_instance=RequestContext(request))

def profile(request, user_id):
    user = request.user if request.user.id is user_id else get_object_or_404(User, id=user_id)
    profile = user.get_profile()
    if request.user <> user and user.get_profile().is_profile_private:
        return forbidden(request, "Sorry, but you do not have permissions to view this profile.")
        
    recommended, committed, completed = Action.objects.actions_by_status(user)[1:4]
    return render_to_response('rah/profile.html', {
        'profile_user': user,
        'total_points': user.get_profile().total_points,
        'completed': completed,
        'profile': user.get_profile(),
        'is_others_profile': request.user <> user,
        'commitment_list': user.get_commit_list(),
        'teams': Group.objects.filter(users=user, is_geo_group=False),
        'records': Record.objects.user_records(user, 10),
    }, context_instance=RequestContext(request))

@login_required
@csrf_protect
def profile_edit(request, user_id):
    if request.user.id <> int(user_id):
        return forbidden(request, "Sorry, but you do not have permissions to edit this profile.")
    
    profile = request.user.get_profile()
    account_form = AccountForm(instance=request.user)
    profile_form = ProfileEditForm(instance=profile)
    group_notifications_form = GroupNotificationsForm(user=request.user)
    
    if request.method == 'POST':
        if "edit_account" in request.POST:
            profile_form = ProfileEditForm(request.POST, instance=profile)
            account_form = AccountForm(request.POST, instance=request.user)
            if profile_form.is_valid() and account_form.is_valid():
                profile_form.save()
                account_form.save()
                messages.add_message(request, messages.SUCCESS, 'Your profile has been updated.')
                return redirect("profile_edit", user_id=request.user.id)
        elif "edit_group_notifications" in request.POST:
            group_notifications_form = GroupNotificationsForm(user=request.user, data=request.POST)
            if group_notifications_form.is_valid():
                group_notifications_form.save()
                messages.add_message(request, messages.SUCCESS, 'Your group notifications have been updated.')
                return redirect("profile_edit", user_id=request.user.id)
        else:
            messages.error(request, 'No action specified.')

    return render_to_response('rah/profile_edit.html', {
        'profile_form': profile_form,
        'account_form': account_form,
        'group_notification_form': group_notifications_form,
        'profile': profile,
    }, context_instance=RequestContext(request))

@csrf_protect
def feedback(request):
    """docstring for feedback"""
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()
            form.send(request)
            
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
        email = request.POST.get("email")
        if email_re.search(email) and not User.objects.filter(email__exact = email):
            valid = True
        if request.user.is_authenticated() and request.user.email == email:
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
        form = HousePartyForm(user=request.user, data=request.POST)
        if form.is_valid() and form.send(request.user):
            if request.user.is_authenticated():
                Record.objects.create_record(request.user, 'mag_request_party_host_info')
            messages.add_message(request, messages.SUCCESS, 'Thanks! We will be in touch soon.')
    return redirect('rah.views.index')

def search(request):
    return render_to_response('rah/search.html', {}, context_instance=RequestContext(request))

def comment_message(sender, comment, request, **kwargs):
    messages.add_message(request, messages.SUCCESS, 'Thanks for the comment.')
comments.signals.comment_was_posted.connect(comment_message)
    
def forbidden(request, message="You do not have permissions."):
    from django.http import HttpResponseForbidden
    return HttpResponseForbidden(loader.render_to_string('403.html', { 'message':message, }, RequestContext(request)))