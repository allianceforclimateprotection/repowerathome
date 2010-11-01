import base64
import re
import urllib2

from xml.dom import minidom

from django.conf import settings
from django.db import models

def _send_codebase(path, data=None):
    "POST the given data message to the codebase API, if no data is provided GET"    
    url = "%s/%s" % (settings.CODEBASE_PROJECT_URL, path)
    headers = {"Content-type": "application/xml", "Accept": "application/xml", 
        "Authorization": "Basic %s" % base64.b64encode("%s:%s" % 
        (settings.CODEBASE_USERNAME, settings.CODEBASE_APIKEY))}
    request = urllib2.Request(url, data, headers)
    return urllib2.urlopen(request).read()
    
def _get_text(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
        elif node.childNodes:
            rc.append(_get_text(node.childNodes))
    return ''.join(rc)
    
class TicketManager(models.Manager):
    INSTRUCTIONS_PATTERN = re.compile("^instructions:")
    
    def qa_tickets(self):
        tickets_dom = minidom.parseString(_send_codebase("tickets?query=status:QA"))
        tickets = []
        for node in tickets_dom.getElementsByTagName("ticket"):
            ticket_id = _get_text(node.getElementsByTagName("ticket-id"))
            summary = _get_text(node.getElementsByTagName("summary"))
            notes_dom = minidom.parseString(_send_codebase("tickets/%s/notes" % ticket_id))
            notes = notes_dom.getElementsByTagName("ticketing-note")
            notes.reverse()
            for idx, note in enumerate(notes):
                content = _get_text(note.getElementsByTagName("content"))
                if idx == len(notes)-1 or re.search(TicketManager.INSTRUCTIONS_PATTERN, content):
                    break
            tickets.append(Ticket(ticket_id=ticket_id, summary=summary, instructions=content))
        return tickets
        
    def add_feedback(self, ticket_id, message):
        data = "<ticket-note><content>%s</content></ticket-note>" % message
        _send_codebase("tickets/%s/notes" % ticket_id, data)
        
class Ticket(models.Model):
    ticket_id = models.IntegerField(blank=True, null=True)
    summary = models.CharField(blank=True, max_length=100)
    instructions = models.TextField(blank=True)
    objects = TicketManager()
    
    class Meta:
        managed = False
        
    def add_feedback(self, message):
        return self.objects.add_feedback(self.ticket_id, message)

    def __unicode__(self):
        return "%s [%s...]" % (self.summary, self.instructions[0:20]) 
    