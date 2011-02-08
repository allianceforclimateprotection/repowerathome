from django.db import models

from actions.models import Action, UserActionProgress

from brabeion import badges as badge_cache
from brabeion.base import Badge, BadgeAwarded

def event_name(action):
    return '%s-action-completed' % action.slug

class ActionBadge(Badge):
    events = ['action_completed']
    multiple = False
    action = None
    levels = ['gold']
    slug = None

    def award(self, **state):
        if not self.action:
            raise NotImplementedError('%s can not be used as a badge' % self.__class__)
        user = state['user']
        if UserActionProgress.objects.filter(user=user, action=self.action, 
                is_completed=True).exists():
            return BadgeAwarded()

    def name(self):
        return '%s Badge' % self.action.name

    def description(self):
        return 'Completed %s action' % self.action.name

    def __unicode__(self):
        return self.slug

def create_action_badge(action):
    slug = '%s-action-badge' % action.slug
    attributes = {'slug': slug, 'action': action, 'events': [event_name(action)]}
    action_badge = type(str(slug), (ActionBadge,), attributes)
    badge_cache.register(action_badge)

for action in Action.objects.all():
    create_action_badge(action)

def update_action_badge(sender, instance, created, **kwargs):
    if created:
        create_action_badge(instance)
models.signals.post_save.connect(update_action_badge, sender=Action)
