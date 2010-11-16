import base64
import re
import urllib2

from xml.dom import minidom

from django.conf import settings
from django.core.cache import cache
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
    INSTRUCTIONS_PATTERN = re.compile("^instructions.?\n\n")
    FEEDBACK_PATTERN = re.compile("Initials.*Works.*Feedback.*", re.S)
    
    @classmethod
    def _parse_ticket_node(cls, node):
        ticket_id = _get_text(node.getElementsByTagName("ticket-id"))
        summary = _get_text(node.getElementsByTagName("summary"))
        notes_dom = minidom.parseString(_send_codebase("tickets/%s/notes" % ticket_id))
        notes = notes_dom.getElementsByTagName("ticketing-note")
        notes.reverse()
        feedback_count = 0
        for idx, note in enumerate(notes):
            content = _get_text(note.getElementsByTagName("content"))
            if TicketManager.FEEDBACK_PATTERN.search(content):
                feedback_count += 1
            if TicketManager.INSTRUCTIONS_PATTERN.search(content):
                # Remove the instruction pattern
                content = TicketManager.INSTRUCTIONS_PATTERN.sub("", content)
                break
            if idx == len(notes)-1:
                break
                
        return Ticket(ticket_id=ticket_id, summary=summary, instructions=content, 
            feedback_count=feedback_count)
    
    def qa_tickets(self):
        cache_hit = cache.get("codebase_qa_tickets")
        if cache_hit:
            return cache_hit
        dom = minidom.parseString(_send_codebase("tickets?query=status:QA"))
        tickets = map(TicketManager._parse_ticket_node, dom.getElementsByTagName("ticket"))
        cache.set("codebase_qa_tickets", tickets, 60 * 5)
        return tickets
        
    def add_feedback(self, ticket_id, message):
        data = "<ticket-note><content>%s</content></ticket-note>" % message
        return _send_codebase("tickets/%s/notes" % ticket_id, data)
        
class Ticket(models.Model):
    ticket_id = models.IntegerField(blank=True, null=True)
    summary = models.CharField(blank=True, max_length=100)
    instructions = models.TextField(blank=True)
    feedback_count = models.IntegerField(blank=True, null=True)
    objects = TicketManager()
    
    class Meta:
        managed = False
        
    def add_feedback(self, message):
        return self.objects.add_feedback(self.ticket_id, message)

    def __unicode__(self):
        return "%s [%s...]" % (self.summary, self.instructions[0:20]) 
    