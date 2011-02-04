from django.db import models

from actions.models import Action, UserActionProgress

from brabeion import badges
from brabeion.base import Badge, BadgeAwarded

class ActionBadge(Badge):
    events = ['action_completed']
    multiple = False
    action = None

    def award(self, **state):
        if not ActionBadge.action:
            raise NotImplementedError('%s can not be used as a badge' % self.__class__)
        user = state['user']
        if UserActionProgress.objects.filter(user=user, 
                action=ActionBadge.action, is_completed=True).exists():
            return BadgeAwarded()

for action in Action.objects.all():
    name = '%s-action-badge' % action.slug
    attributes = {'slug': name, 'action': action}
    action_badge = type(name, (ActionBadge,), attributes)
    badges.register(action_badge)

def possibly_award_badge(sender, instance, created, **kwargs):
    if instance.is_completed:
        badges.possibly_award_badge('action_completed', user=instance.user)
models.signals.post_save.connect(possibly_award_badge, sender=UserActionProgress)
