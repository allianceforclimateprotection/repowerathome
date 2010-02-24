import re

from django.contrib.auth.models import User
from django.db import models

from geo.models import Location
from records.models import Record
from rah.models import Action

def user_groups(user):
    groups = list(Group.objects.filter(users=user))
    return groups + GeoGroup.objects.get_users_geo_groups(user)

class BaseGroup(object):
    _must_redefine = Exception("Implementation of BaseGroup must redefine this method")
    
    def is_joinable(self):
        raise _must_redefine
        
    def is_member(self):
        raise _must_redefine
        
    def _group_users_filtered(self):
        raise _must_redefine
        
    def _group_actions_filtered(self):
        raise _must_redefine
        
    def _group_records_filtered(self):
        raise _must_redefine
        
    def is_public(self):
        return True
        
    def completed_actions_by_user(self):
        """
        what actions have been completed by users in this group and how many users have completed each action
        """
        actions = self._group_actions_filtered()
        actions = actions.order_by("-users_completed")
        actions = actions.filter(useractionprogress__is_completed=1)
        actions = actions.annotate(users_completed=models.Count("useractionprogress__is_completed"))
        return actions
        
    def members_ordered_by_points(self, limit=None):
        users = self._group_users_filtered()
        users = users.order_by("-profile__total_points")
        users = users.annotate(actions_completed=models.Sum("useractionprogress__is_completed"))
        users = users.annotate(actions_committed=models.Count("useractionprogress__date_committed"))
        return users[:limit] if limit else users
        
    def group_records(self, limit=None):
        records = self._group_records_filtered()
        records = records.select_related().order_by("-created")
        return records[:limit] if limit else records
        
    def has_pending_membership(self, user):
        return False
        
    def requesters_to_grant_or_deny(self, user):
        return []
        
    def is_user_manager(self, user):
        return False
        
class GroupManager(models.Manager):
    def new_groups_with_memberships(self, user, limit=None):
        groups = self.all().order_by("-created")
        groups = groups.extra(
                    select_params = (user.id,), 
                    select = { 'is_member': 'SELECT groups_groupusers.created \
                                                FROM groups_groupusers \
                                                WHERE groups_groupusers.user_id = %s AND \
                                                groups_groupusers.group_id = groups_group.id'})
        groups = groups.extra(
                    select_params = (user.id,), 
                    select = { 'membership_pending': 'SELECT groups_membershiprequests.created \
                                                        FROM groups_membershiprequests \
                                                        WHERE groups_membershiprequests.user_id = %s AND \
                                                        groups_membershiprequests.group_id = groups_group.id'})
        return groups[:limit] if limit else groups
        
class Group(BaseGroup, models.Model):
    MEMBERSHIP_CHOICES = (
        ('O', 'Open membership'),
        ('C', 'Closed membership'),
    )

    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField()
    membership_type = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default="O")
    image = models.ImageField(upload_to="group_images", null=True)
    is_featured = models.BooleanField(default=False)
    users = models.ManyToManyField(User, through="GroupUsers")
    requesters = models.ManyToManyField(User, through="MembershipRequests", related_name="requested_group_set")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    objects = GroupManager()
    
    def is_joinable(self):
        return True
    
    def is_public(self):
        return self.membership_type == "O"
        
    def is_member(self, user):
        if user.is_authenticated():
            return GroupUsers.objects.filter(group=self, user=user).exists()
        return False
        
    def _group_users_filtered(self):
        return User.objects.filter(group=self)

    def _group_actions_filtered(self):
        return Action.objects.filter(useractionprogress__user__group=self)

    def _group_records_filtered(self):
        return Record.objects.filter(user__group=self)
    
    def has_pending_membership(self, user):
        if user.is_authenticated():
            return MembershipRequests.objects.filter(group=self, user=user).exists()
        return False
        
    def requesters_to_grant_or_deny(self, user):
        if user.is_authenticated() and self.is_user_manager(user):
            return User.objects.filter(membershiprequests__group=self)
        return []
        
    def is_user_manger(self, user):
        return GroupUsers.objects.filter(user=self, group=group, is_manager=True).exists()
        
    @models.permalink
    def get_absolute_url(self):
        return ("group_detail", [str(self.slug)])
        
    def __unicode__(self):
        return u'%s' % self.name
        
class GeoGroupManager(models.Manager):    
    def geo_slugify(self, value):
        return re.sub("[\s]", "-", value).lower()

    def de_geo_slugify(self, value):
        return re.sub("[-]", " ", value).title()
    
    def get_geo_group(self, state, county_slug=None, place_slug=None):
        locations = Location.objects.filter(st=state)
        if place_slug:
            place = self.de_geo_slugify(place_slug)
            locations = locations.filter(name=place)
        elif county_slug:
            county = self.de_geo_slugify(county_slug)
            locations = locations.filter(county=county)
        
        if locations.count() == 0:
            return None
            
        return GeoGroup(locations=locations, state=state, county_slug=county_slug, place_slug=place_slug)
            
    def get_users_geo_groups(self, user):
        location = user.get_profile().location
        if location:
            state = location.st
            county_slug = self.geo_slugify(location.county)
            place_slug = self.geo_slugify(location.name)
            return [self.get_geo_group(state),
                        self.get_geo_group(state, county_slug),
                        self.get_geo_group(state, county_slug, place_slug),]
        return []
        
class GeoGroup(BaseGroup):
    objects = GeoGroupManager()
    
    class Meta:
        managed = False
        
    def __init__(self, locations, state, county_slug=None, place_slug=None, *args, **kwargs):
        self.locations = locations
        self.state = state
        self.county_slug = county_slug
        self.place_slug = place_slug
        self._set_attributes(locations[0], county_slug != None, place_slug != None)
        
    def _set_attributes(self, location, has_county, has_place):
        if has_place:
            self.name = "%s, %s" % (location.name, location.st)
        elif has_county:
            self.name = "%s in %s" % (location.county, location.state)
        else:
            self.name = location.state
        self.description = "A meeting place for all users belonging to %s" % self.name
        self.image = "geo_group_images/geo.jpg"
        
    def is_joinable(self):
        return False 
        
    def is_public(self):
        return True

    def is_member(self, user):
        if user.is_authenticated():
            return User.objects.filter(pk=user.id, profile__location__in=self.locations).exists()
        return False

    def _group_users_filtered(self):
        return User.objects.filter(profile__location__in=self.locations)

    def _group_actions_filtered(self):
        return Action.objects.filter(useractionprogress__user__profile__location__in=self.locations)

    def _group_records_filtered(self):
        return Record.objects.filter(user__profile__location__in=self.locations)
        
    @models.permalink
    def get_absolute_url(self):
        if self.place_slug:
            return ("geo_group_place", [self.state, self.county_slug, self.place_slug])
        elif self.county_slug:
            return ("geo_group_county", [self.state, self.county_slug])
        return ("geo_group_state", [self.state])

class GroupUsers(models.Model):
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    is_manager = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return u'%s belongs to group %s' % (self.user, self.group)
        
class MembershipRequests(models.Model):
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    created = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return u'%s request to join %s on %s' % (self.user, self.group, self.created)