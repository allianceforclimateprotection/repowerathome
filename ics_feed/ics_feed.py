import vobject

from django.utils.encoding import smart_unicode
from django.http import HttpResponse

EVENT_ITEMS = (
    ('uid', 'uid'),
    ('dtstart', 'start'),
    ('dtend', 'end'),
    ('summary', 'summary'),
    ('location', 'location'),
    ('last_modified', 'last_modified'),
    ('created', 'created'),
)

class IcsEvent(object):
    """Used to map any object to an ICS Event for ICalendarFeed to process.

    Notes:
    * Start and end timestamps can be datetime.datetime objects (django.db.models.DateTimeField) as well as datetime.date objects
        * (django.db.models.DateField). If they are datetime.date objects, the event will be exposed as an all-day event.
       """
    def __init__(self, uid, summary, start, end=None, location=None, last_modified=None, created=None):
        self.uid = uid
        self.summary = smart_unicode(summary)
        self.start = start

        if end != None:
            self.end = end
        if location != None:
            self.location = location
        if last_modified != None:
            self.last_modified = last_modified
        if created != None:
            self.created = created
        

class ICalendarFeed(object):
    """Provides a base class for creating iCal feeds.

    To create a feed, simply subclas ICalendarFeed and implement the items method, which
    should return a list of IcsEvents.

    Original code by Christian Joergensen:
        http://www.technobabble.dk/2008/mar/06/exposing-calendar-events-using-icalendar-django/
       """

    def __call__(self, *args, **kwargs):
        """This tests to see if the standard attributes have been implemented via the subclass.
        If they have, it adds them to the calendar item in question and moves on.
           """
        cal = vobject.iCalendar()

        for item in self.items():
            event = cal.add('vevent')
            for vkey, key in EVENT_ITEMS:
                try:
                    value = getattr(item, key)
                    event.add(vkey).value = value
                except AttributeError:
                    continue

        response = HttpResponse(cal.serialize())
        response['Content-Type'] = 'text/calendar'
        response['Content-Disposition'] = 'attachment; filename=ical_feed.ics'
        return response

    def items(self):
        """Returns a list of IcsEvents to be added to the calendar. 
        You _must_ override this method!
           """
        return []


