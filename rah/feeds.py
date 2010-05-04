from django.contrib.syndication.views import Feed, FeedDoesNotExist
from django.shortcuts import get_object_or_404
from django.utils.feedgenerator import Atom1Feed

from django.contrib.auth.models import User

from records.models import Record

class UserActivityFeed(Feed):
    feed_type = Atom1Feed
    
    def get_object(self, request, user_id):
        self.request = request
        return get_object_or_404(User, id=user_id)

    def title(self, user):
        return "%s Activity Stream" % user.get_full_name()

    def link(self, user):
        return user.get_absolute_url()

    def feed_guid(self, user):
        return self.link(user)

    def subtitle(self, user):
        return "%s's recent activity" % user.get_full_name()

    def items(self, user):
        records = Record.objects.filter(user=user)
        records = records.exclude(user__profile__is_profile_private=True)
        records = records.select_related().order_by("-created")
        return records[:30]

    def item_description(self, record):
        return record.render(self.request)

    def item_link(self, record):
        return record.get_absolute_url()

    def item_pudate(self, item):
        return record.created