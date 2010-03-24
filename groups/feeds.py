from django.contrib.syndication.views import Feed, FeedDoesNotExist
from django.shortcuts import get_object_or_404
from django.utils.feedgenerator import Atom1Feed

from models import Group

from records.models import Record

class GroupActivityFeed(Feed):
    feed_type = Atom1Feed
    
    def get_object(self, request, group_slug):
        self.request = request
        return get_object_or_404(Group, slug=group_slug)

    def title(self, group):
        return "%s Activity Stream" % group.name

    def link(self, group):
        return group.get_absolute_url()
        
    def feed_guid(self, group):
        return self.link(group)

    def subtitle(self, group):
        return "All of the activity going on for %s" % group.name

    def items(self, group):
        return group.group_records(30)
        
    def item_description(self, record):
        return record.render(self.request)
        
    def item_link(self, record):
        return record.get_absolute_url()
        
    def item_pudate(self, item):
        return record.created