from datetime import date, timedelta
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
        one_week = timedelta(days=7)
        events = Event.objects.filter(when__gte=today, when__lte=today+one_week)
        actions = UserActionProgress.objects.filter(date_committed__gte=today, date_committed__lte=today+one_week)

        # Map the models to IcsEvent
        mapped_events = [IcsEvent("Event"+str(i.id), i.title, i.when) for i in events] # TODO: Change when to specific time
        mapped_actions= [IcsEvent("Actions"+str(i.id), i.action, i.date_committed) for i in actions]

        # Combine the lists.  FIXME: This is inefficient... 
        combined_items = list(chain(mapped_events, mapped_actions))
        return combined_items 
