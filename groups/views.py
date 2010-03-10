from smtplib import SMTPException

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import Context, loader, RequestContext
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

from records.models import Record

from models import Group, GroupUsers, MembershipRequests
from forms import GroupForm, MembershipForm

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
            return redirect("group_detail", group_slug=group.slug)
    else:
        form = GroupForm()
    return render_to_response("groups/group_create.html", {"form": form, "site": Site.objects.get_current()}, context_instance=RequestContext(request))
    
@login_required
def group_leave(request, group_id):
    group = get_object_or_404(Group, id=group_id, is_geo_group=False)
    if request.user.id in group.users.all().values_list("id", flat=True):
        if group.has_other_managers(request.user):
            GroupUsers.objects.filter(group=group, user=request.user).delete()
            messages.success(request, "You have been removed from group %s" % group)
        else:
            messages.error(request, "You can not leave the group, until you've assigned someone else to be manager.", extra_tags="sticky")
    else:
        messages.error(request, "You can not leave a group your not a member of")
    return redirect("group_detail", group_slug=group.slug)
    
@login_required
def group_join(request, group_id):
    group = get_object_or_404(Group, id=group_id, is_geo_group=False)
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
        template = loader.get_template("groups/group_join_request.html")
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
def group_membership_request(request, group_id, user_id, action):
    group = get_object_or_404(Group, id=group_id, is_geo_group=False)
    user = get_object_or_404(User, id=user_id)
    if not group.is_user_manager(request.user):
        messages.error(request, "You do not have permissions")
        return redirect("group_detail", group_slug=group.slug)
    membership_request = MembershipRequests.objects.filter(group=group, user=user)
    if membership_request:
        if action == "approve":
            GroupUsers.objects.create(group=group, user=user, is_manager=False)
            membership_request.delete()
            messages.success(request, "%s has been added to the group" % user)
        elif action == "deny":
            membership_request.delete()
            messages.success(request, "%s has been denied access to the group" % user)
    else:
        messages.error(request, "%s has not requested to join this group" % user)
    return redirect("group_detail", group_slug=group.slug)

def group_detail(request, group_slug):
    """
    display all of the information about a particular group
    """
    group = get_object_or_404(Group, slug=group_slug, is_geo_group=False)
    return _group_detail(request, group)
    
def geo_group(request, state, county_slug=None, place_slug=None):
    slug = state.lower()
    if county_slug:
        slug += "-%s" % county_slug
    if place_slug:
        slug += "-%s" % place_slug
    group = get_object_or_404(Group, slug=slug)
    return _group_detail(request, group)
    
def group_list(request):
    """
    display a listing of the groups
    """
    new_groups = Group.objects.new_groups_with_memberships(request.user, 5)
    return render_to_response("groups/group_list.html", locals(), context_instance=RequestContext(request))

@login_required
@csrf_protect    
def group_edit(request, group_slug):
    group = get_object_or_404(Group, slug=group_slug, is_geo_group=False)
    if not group.is_user_manager(request.user):
        return _forbidden(request)
    if request.method == "POST":
        if "change_group" in request.POST:
            group_form = GroupForm(request.POST, request.FILES, instance=group)
            if group_form.is_valid():
                group = group_form.save()
                messages.success(request, "%s has been updated." % group)
                return redirect("group_edit", group_slug=group.slug)
            else:
                membership_form = MembershipForm(group=group)
        elif "delete_group" in request.POST:
            group.delete()
            messages.success(request, "%s has been deleted." % group)
            return redirect("group_list")
        elif "change_membership" in request.POST:
            membership_form = MembershipForm(group=group, data=request.POST)
            if membership_form.is_valid():
                membership_form.save()
                if group.is_user_manager(request.user):
                    messages.success(request, "%s's memberships have been updated." % group)
                    return render_to_response("groups/group_edit.html", locals(), context_instance=RequestContext(request))
                else:
                    messages.success(request, "You no longer have permissions to edit %s" % group)
                    return redirect("group_detail", group_slug=group.slug)
            else:
                group_form = GroupForm(instance=group)
    else:
        group_form = GroupForm(instance=group)
        membership_form = MembershipForm(group=group)
    site = Site.objects.get_current()
    requesters = group.requesters_to_grant_or_deny(request.user)
    return render_to_response("groups/group_edit.html", locals(), context_instance=RequestContext(request))

def _group_detail(request, group):
    popular_actions = group.completed_actions_by_user()
    top_members = group.members_ordered_by_points()
    group_records = group.group_records(10)
    is_member = group.is_member(request.user)
    is_manager = group.is_user_manager(request.user)
    membership_pending = group.has_pending_membership(request.user)
    requesters = group.requesters_to_grant_or_deny(request.user)
    has_other_managers = group.has_other_managers(request.user)
    return render_to_response("groups/group_detail.html", locals(), context_instance=RequestContext(request))
    
def _forbidden(request, message="You do not have permissions."):
    from django.http import HttpResponseForbidden
    return HttpResponseForbidden(loader.render_to_string('403.html', { 'message':message, }, RequestContext(request)))