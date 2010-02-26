from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import loader, RequestContext
from django.views.decorators.csrf import csrf_protect

from records.models import Record

from models import Group, GeoGroup, GroupUsers, MembershipRequests
from forms import GroupForm

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
            return redirect("group_detail", group_slug=group.slug) # TODO: after creating the group we should redirect the user to the group detail page
    else:
        form = GroupForm()
    return render_to_response("groups/group_create.html", {"form": form, "site": Site.objects.get_current()}, context_instance=RequestContext(request))
    
@login_required
def group_leave(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.user in group.users.all():
        GroupUsers.objects.filter(group=group, user=request.user).delete()
        messages.success(request, "You have been removed from group %s" % group)
    else:
        messages.error(request, "You can not leave a group your not a member of")
    return redirect("group_detail", group_slug=group.slug)
    
@login_required
def group_join(request, group_id):
    group = get_object_or_404(Group, id=group_id)
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
        template = loader.get_template("rah/group_join_request.html")
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
def group_membership(request, group_id, user_id, action):
    group = get_object_or_404(Group, id=group_id)
    user = get_object_or_404(User, id=user_id)
    if not group.is_user_manager(request.user):
        messages.errors(request, "You do not have permissions")
        return redirect("group_detail", group_slug=group.slug)
    membership_request = MembershipRequests.objects.filter(group=group, user=user)
    if membership_request:
        if action == "approve":
            GroupUsers.objects.create(group=group, user=user, is_manager=False)
            membership_request.delete()
            messages.success(request, "%s has been added to the group" % user)
            # TODO: also create a message for the approved user
        elif action == "deny":
            membership_request.delete()
            messages.success(request, "%s has been denied access to the group" % user)
            # TODO: also create a message for the denied user
    else:
        messages.errors(request, "%s has not requested to join this group" % user)
    return redirect("group_detail", group_slug=group.slug)

def group_detail(request, group_slug):
    """
    display all of the information about a particular group
    """
    group = get_object_or_404(Group, slug=group_slug)
    return _group_detail(request, group)
    
def geo_group(request, state, county_slug=None, place_slug=None):
    geo_group = GeoGroup.objects.get_geo_group(state, county_slug, place_slug)
    if not geo_group:
        raise Http404
    return _group_detail(request, geo_group)
    
def group_list(request):
    """
    display a listing of the groups
    """
    new_groups = Group.objects.new_groups_with_memberships(request.user, 5)
    return render_to_response("groups/group_list.html", locals(), context_instance=RequestContext(request))

def _group_detail(request, group):
    popular_actions = group.completed_actions_by_user()
    top_members = group.members_ordered_by_points()
    group_records = group.group_records(10)
    is_member = group.is_member(request.user)
    membership_pending = group.has_pending_membership(request.user)
    requesters = group.requesters_to_grant_or_deny(request.user)
    return render_to_response("groups/group_detail.html", locals(), context_instance=RequestContext(request))