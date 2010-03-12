from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

from geo.models import Location
from records.models import Record
from rah.models import Action, Profile
        
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
        
    def user_geo_group_tuple(self, user):
        location = user.get_profile().location
        geo_groups = []
        for location_type_tuple in Group.LOCATION_TYPE:
            location_type = location_type_tuple[0]
            slug = Group.LOCATION_SLUG[location_type](location)
            query = self.filter(slug=slug)
            geo_groups.append((location_type, query[0] if query else None))
        return geo_groups

    def create_geo_group(self, location_type, location):
        name = Group.LOCATION_NAME[location_type](location)
        slug = Group.LOCATION_SLUG[location_type](location)
        parent_key = Group.LOCATION_PARENT[location_type]
        parent = None
        if parent_key:
            parent_slug = Group.LOCATION_SLUG[parent_key](location)
            parent_query = self.filter(slug=parent_slug)
            parent = parent_query[0] if parent_query else self.create_geo_group(parent_key, location)
        geo_group = Group(name=name, slug=slug, is_geo_group=True, location_type=location_type, sample_location=location, parent=parent)
        geo_group.save()
        return geo_group
        
class Group(models.Model):
    MEMBERSHIP_CHOICES = (
        ('O', 'Open membership'),
        ('C', 'Closed membership'),
    )
    LOCATION_TYPE = (
        ('S', 'State'),
        ('C', 'County'),
        ('P', 'Place'),
    )
    LOCATION_PARENT = {
        'S': None,
        'C': 'S',
        'P': 'C',
    }
    LOCATION_NAME = {
        'S': lambda l: l.state,
        'C': lambda l: l.county,
        'P': lambda l: "%s, %s" % (l.name, l.state),
    }
    LOCATION_SLUG = {
        'S': lambda l: slugify(l.st),
        'C': lambda l: "%s-%s" % (slugify(l.st), slugify(l.county)),
        'P': lambda l: "%s-%s-%s" % (slugify(l.st), slugify(l.county), slugify(l.name)),    
    }
    LOCATION_URL = {
        'S': lambda l: ("geo_group_state", [l.st]),
        'C': lambda l: ("geo_group_county", [l.st, slugify(l.county)]),
        'P': lambda l: ("geo_group_place", [l.st, slugify(l.county), slugify(l.name)]),
    }

    name = models.CharField(max_length=255, blank=True)
    slug = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="group_images", null=True)
    is_featured = models.BooleanField(default=False)
    membership_type = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default="O", null=True)
    is_geo_group = models.BooleanField(default=False)
    location_type = models.CharField(max_length=1, choices=LOCATION_TYPE, blank=True)
    sample_location = models.ForeignKey(Location, null=True, blank=True)
    parent = models.ForeignKey("self", null=True, blank=True, related_name="children")
    users = models.ManyToManyField(User, through="GroupUsers")
    requesters = models.ManyToManyField(User, through="MembershipRequests", related_name="requested_group_set")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = GroupManager()
    
    def is_joinable(self):
        return not self.is_geo_group
    
    def is_public(self):
        return self.is_geo_group or self.membership_type == "O"
        
    def is_member(self, user):
        return user.is_authenticated() and \
            GroupUsers.objects.filter(group=self, user=user).exists()
        
    def safe_image(self):
        if self.is_geo_group:
            return self.image if self.image else "images/theme/geo_group.jpg"
        return self.image if self.image else "images/theme/default_group.png"
        
    def completed_actions_by_user(self):
        """
        what actions have been completed by users in this group and how many users have completed each action
        """
        actions = Action.objects.distinct().filter(useractionprogress__user__group=self, users_completed__gte=1)
        actions = actions.order_by("-users_completed")
        return actions

    def members_ordered_by_points(self):
        return User.objects.raw("""
        SELECT auth_user.id, auth_user.username, auth_user.first_name, auth_user.last_name, auth_user.email, auth_user.password, 
        	auth_user.is_staff, auth_user.is_active, auth_user.is_superuser, auth_user.last_login, auth_user.date_joined, rah_profile.total_points,
        	SUM(rah_useractionprogress.is_completed) AS actions_completed, 
        	COUNT(rah_useractionprogress.date_committed) AS actions_committed,
        	(SELECT MAX(created) FROM records_record WHERE user_id = auth_user.id) AS last_active
        FROM auth_user 
        INNER JOIN groups_groupusers ON (auth_user.id = groups_groupusers.user_id)
        LEFT OUTER JOIN rah_useractionprogress ON (auth_user.id = rah_useractionprogress.user_id)
        LEFT OUTER JOIN rah_profile ON (auth_user.id = rah_profile.user_id)
        WHERE groups_groupusers.group_id = %s
        GROUP BY auth_user.id, auth_user.username, auth_user.first_name, auth_user.last_name, auth_user.email, auth_user.password,
        	auth_user.is_staff, auth_user.is_active, auth_user.is_superuser, auth_user.last_login, auth_user.date_joined, rah_profile.total_points
        ORDER BY rah_profile.total_points DESC
        """ % self.id)

    def group_records(self, limit=None):
        records = Record.objects.filter(user__group=self)
        records = records.select_related().order_by("-created")
        return records[:limit] if limit else records
        
    def has_pending_membership(self, user):
        return user.is_authenticated() and \
            self.is_joinable() and \
            MembershipRequests.objects.filter(group=self, user=user).exists()
        
    def requesters_to_grant_or_deny(self, user):
        if self.is_joinable() and user.is_authenticated() and self.is_user_manager(user):
            return User.objects.filter(membershiprequests__group=self)
        return []
        
    def is_user_manager(self, user):
        return user.is_authenticated() and \
            self.is_joinable() and \
            GroupUsers.objects.filter(user=user, group=self, is_manager=True).exists()
        
    def parents(self):
        parents = []
        if self.parent:
            parents.extend(self.parent.parents())
            parents.append(self.parent)
        return parents
        
    def has_other_managers(self, user):
        managers = GroupUsers.objects.filter(group=self, is_manager=True)
        if user.is_authenticated():
            managers = managers.exclude(user=user)
        return managers.exists()
        
    def number_of_managers(self):
        return GroupUsers.objects.filter(group=self, is_manager=True).count()
        
    @models.permalink
    def get_absolute_url(self):
        if self.is_geo_group:
            return Group.LOCATION_URL[self.location_type](self.sample_location)
        return ("group_detail", [str(self.slug)])
        
    def __unicode__(self):
        return u'%s' % self.name
        
class GroupUsers(models.Model):
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    is_manager = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ("user", "group",)
    
    def __unicode__(self):
        return u'%s belongs to group %s' % (self.user, self.group)
        
class MembershipRequests(models.Model):
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ("user", "group",)
    
    def __unicode__(self):
        return u'%s request to join %s on %s' % (self.user, self.group, self.created)
        
def associate_with_geo_groups(sender, instance, **kwargs):
    user = instance.user
    GroupUsers.objects.filter(user=user, group__is_geo_group=True).delete()
    if instance.location:
        geo_groups = Group.objects.user_geo_group_tuple(user)
        for location_type, geo_group in geo_groups:
            if not geo_group:
                geo_group = Group.objects.create_geo_group(location_type, instance.location)
            GroupUsers(user=user, group=geo_group).save()
        
models.signals.post_save.connect(associate_with_geo_groups, sender=Profile)