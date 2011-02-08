from datetime import date, timedelta, datetime
from itertools import chain

from events.models import Event
from actions.models import UserActionProgress 
from ics_feed import ICalendarFeed, IcsEvent

class CombinedICSFeed(ICalendarFeed):
    """Provides a simple iCal feed of the next week's events and commitments.
       """
    
    def items(self):
        """Returns a combined list of all the events we wish to include to include in our feed.
           """
        # Get the events
        today = date.today()
        one_week_later = today + timedelta(days=7)
        events = Event.objects.filter(when__gte=today, when__lte=one_week_later)
        actions = UserActionProgress.objects.filter(date_committed__gte=today, date_committed__lte=one_week_later)

        # Map the models to IcsEvent
        mapped_events = [IcsEvent("Event"+str(i.id), i.title, i.start_datetime(),end=i.start_datetime()+timedelta(hours=i.duration) ) for i in events]
        mapped_actions= [IcsEvent("Actions"+str(i.id), i.action, i.date_committed) for i in actions]

        # Combine the lists.  FIXME: This is inefficient... 
        combined_items = list(chain(mapped_events, mapped_actions))
        return combined_items 
