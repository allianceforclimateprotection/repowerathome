from datetime import datetime

from django.contrib.syndication.feeds import FeedDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.utils.feedgenerator import Atom1Feed

from events.models import Event

class EventsFeed(Feed):
    feed_type = Atom1Feed
    
    _site = Site.objects.get_current()
    title = '%s feed' % _site.name
    subtitle = '%s events feed.' % _site.name

    def link(self):
        # TODO: Double check that this is where we want to drop them 
        return reverse('event-show') 

    def items(self):
        # TODO: Create a better sort/order
        return Event.objects.filter(when__gte=datetime.now())[:10]

    def item_creation_date(self, obj):
        return obj.created

    def item_description(self, event):
        return event

    def item_link(self, event):
        return event.get_absolute_url()
