import json
import logging
import locale
import re
from datetime import datetime

from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.comments.views import comments
from django.contrib.sites.models import Site, RequestSite
from django.core.mail import send_mail, EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from django.db.models import Sum, Count
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext, loader, Context
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.cache import cache_page
from brabeion.models import BadgeAward

from basic.blog.models import Post
from tagging.models import Tag
from actions.models import Action, UserActionProgress
from rah.models import Profile, StickerRecipient
from records.models import Record
from rah.forms import RegistrationForm, RegistrationProfileForm, AuthenticationForm, \
    AccountForm, ProfileEditForm, GroupNotificationsForm, FeedbackForm, StickerRecipientForm
from settings import GA_TRACK_PAGEVIEW, GA_TRACK_CONVERSION, LOGIN_REDIRECT_URL, LOCALE
from geo.models import Location
from twitter_app.forms import StatusForm as TwitterStatusForm
from groups.models import Group
from commitments.models import Contributor, Commitment, Survey, ContributorSurvey
from commitments.forms import ContributorForm
from commitments.survey_forms import PledgeCard
from events.models import Event, Guest
from messaging.models import Stream
from messaging.forms import StreamNotificationsForm
from badges.models import user_badges

from decorators import save_queued_POST
from signals import logged_in

def _total_trendsetters():
    return (Profile.objects.all().count()) + \
        (Contributor.objects.filter(user__isnull=True).count() or 0)

def _total_points():
    return (Profile.objects.all().aggregate(Sum("total_points"))["total_points__sum"] or 0) + \
        (Action.objects.filter(commitment__answer="D", commitment__contributor__user__isnull=True).aggregate(
            Sum("points"))["points__sum"] or 0)

def _total_actions():
    return (Record.objects.filter(void=False, activity=1).count() or 0) + \
        (Commitment.objects.filter(answer="D", action__isnull=False, contributor__user__isnull=True).count() or 0)

def _total_commitment_cards():
    return (ContributorSurvey.objects.all().count())

def _total_communities():
    return (Group.objects.filter(is_geo_group=False).count() or 0)

def _total_events():
    return (Event.objects.filter(when__lte=datetime.now()).count() or 0)


def _progress_stats():
    progress_stats = cache.get('progress_stats')
    if progress_stats:
        return progress_stats
    else:
        progress_stats = {}
        progress_stats['total_trendsetters'] = _total_trendsetters()
        progress_stats['total_points'] = _total_points()
        progress_stats['total_actions'] = _total_actions()
        progress_stats['total_commitment_cards'] = _total_commitment_cards()
        progress_stats['total_communities'] = _total_communities()
        progress_stats['total_events'] = _total_events()
        cache.set('progress_stats', progress_stats, 60 * 5)
        return progress_stats

@csrf_protect
def index(request):
    """
    Home Page
    """
    # If the user is not logged in, show them the logged out homepage and bail
    if request.user.is_authenticated():
        return profile(request, request.user.id)

    section_class = "section_home"
    top_users = Profile.objects.filter(is_profile_private=False, location__isnull=False, facebook_connect_only=True).select_related("user").order_by("-total_points")[:6]
    top_communities = Group.objects.filter(is_featured=True).order_by("-member_count")[:2]
    locals().update(_progress_stats())

    return render_to_response("rah/home_page.html", locals(), context_instance=RequestContext(request))

@cache_page(60 * 60)
def user_list(request):
    """This page of links allows google CSE to find user profile pages"""
    users = User.objects.filter(profile__is_profile_private=False).only('first_name', 'last_name', 'id')
    return render_to_response("rah/user_list.html", {'users': users}, context_instance=RequestContext(request))

def logout(request):
    auth.logout(request)
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
def register(request, template_name="registration/register.html"):
    redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '')
    initial = {"email": request.GET["email"]} if "email" in request.GET else None
    user_form = RegistrationForm(initial=initial, data=(request.POST or None))
    profile_form = RegistrationProfileForm(request.POST or None)

    if user_form.is_valid() and profile_form.is_valid():
        new_user = user_form.save()
        if hasattr(profile_form, 'location'):
            profile = new_user.get_profile()
            profile.location = profile_form.location
            profile.save()
        user = auth.authenticate(username=new_user.email, password=user_form.cleaned_data["password1"])
        logged_in.send(sender=None, request=request, user=user, is_new_user=True)
        auth.login(request, user)
        save_queued_POST(request)
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
    return render_to_response(template_name, {
        'form': user_form,
        'profile_form': profile_form,
        REDIRECT_FIELD_NAME: redirect_to,
    }, context_instance=RequestContext(request))

@csrf_exempt
# TODO: Use an ajax request to login from the tongue because CSRF is not being used for this view
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
            user = form.get_user()
            logged_in.send(sender=None, request=request, user=user, is_new_user=False)
            auth.login(request, user)
            save_queued_POST(request)
            messages.add_message(request, GA_TRACK_PAGEVIEW, '/login/success')

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

    actions = Action.objects.actions_by_status(user)
    commitment_list = UserActionProgress.objects.commitments_for_user(user)
    groups = Group.objects.filter(users=user, is_geo_group=False)
    events = Event.objects.filter(guest__contributor__user=user)
    records = Record.objects.user_records(user, 10)
    badges = user_badges(user)
    #pledge_card_count = ContributorSurvey.objects.filter(entered_by=user).count()

    #locals().update(_progress_stats())

    #try:
        #contributor = Contributor.objects.get(user=request.user)
    #except Contributor.DoesNotExist:
        #contributor = None
    #profile = request.user.get_profile()
    #zipcode = profile.location.zipcode if profile.location else ""
    #contributor_form = ContributorForm(instance=contributor, initial={"zipcode": zipcode})
    #pledge_card_form = PledgeCard(contributor, None)

    return render_to_response('rah/profile.html', {
        'user': user,
        #'total_points': user.get_profile().total_points,
        #'completed': completed,
        #'profile': user.get_profile(),
        'is_others_profile': request.user <> user,
        'commitment_list': UserActionProgress.objects.commitments_for_user(user),
        'events': events,
        'badges': badges,
        'communities': Group.objects.filter(users=user, is_geo_group=False),
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
    stream_notifications_form = StreamNotificationsForm(user=request.user)

    if request.method == 'POST':
        if "edit_account" in request.POST:
            profile_form = ProfileEditForm(request.POST, instance=profile)
            account_form = AccountForm(request.POST, instance=request.user)
            if profile_form.is_valid() and account_form.is_valid():
                profile_form.save()
                account_form.save()
                messages.add_message(request, messages.SUCCESS, 'Your profile has been updated.')
                return redirect("profile_edit", user_id=request.user.id)
        elif "edit_notifications" in request.POST:
            group_notifications_form = GroupNotificationsForm(user=request.user, data=request.POST)
            stream_notifications_form = StreamNotificationsForm(user=request.user, data=request.POST)
            if group_notifications_form.is_valid() and stream_notifications_form.is_valid():
                group_notifications_form.save()
                stream_notifications_form.save()
                messages.add_message(request, messages.SUCCESS, 'Your notifications have been updated.')
                return redirect("profile_edit", user_id=request.user.id)
        else:
            messages.error(request, 'No action specified.')

    return render_to_response('rah/profile_edit.html', {
        'profile_form': profile_form,
        'account_form': account_form,
        'group_notification_form': group_notifications_form,
        'stream_notification_form': stream_notifications_form,
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

    return render_to_response('rah/feedback.html', { 'form': form, }, context_instance=RequestContext(request))

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

def search(request):
    return render_to_response('rah/search.html', {}, context_instance=RequestContext(request))

def ga_opt_out(request):
    return render_to_response('rah/ga_opt_out.html', {}, context_instance=RequestContext(request))

def comment_message(sender, comment, request, **kwargs):
    messages.add_message(request, messages.SUCCESS, 'Thanks for the comment.')
comments.signals.comment_was_posted.connect(comment_message)

def forbidden(request, message="You do not have permissions."):
    from django.http import HttpResponseForbidden
    return HttpResponseForbidden(loader.render_to_string('403.html', { 'message':message, }, RequestContext(request)))

def track_registration(sender, request, user, is_new_user, **kwargs):
    if is_new_user:
        messages.success(request, 'Thanks for registering.')
        messages.add_message(request, GA_TRACK_PAGEVIEW, '/register/complete')
        messages.add_message(request, GA_TRACK_CONVERSION, True)
logged_in.connect(track_registration)

def send_registration_emails(sender, request, user, is_new_user, **kwargs):
    if is_new_user:
        Stream.objects.get(slug="registration").enqueue(content_object=user, start=user.date_joined)
logged_in.connect(send_registration_emails)

def take_the_pledge(sender, request, user, is_new_user, **kwargs):
    if is_new_user:
        contributor, created = Contributor.objects.get_or_create_from_user(user=user)
        Commitment.objects.get_or_create(contributor=contributor, question="pledge", defaults={"answer":True})
        ContributorSurvey.objects.get_or_create(contributor=contributor, survey=Survey.objects.get(form_name="PledgeCard"), entered_by=None)
logged_in.connect(take_the_pledge)
