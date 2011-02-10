from django.db import models
from django.contrib.comments.models import Comment

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
        return self.action.name

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

class TrendsetterBadge(Badge):
    events = ['took_the_pledge']
    multiple = False
    levels = ['']
    slug = 'trendsetter-badge'
    name = 'Trendsetter'
    description = 'Took the Trendsetter Pledge'

    def award(self, **state):
        return BadgeAwarded()
badge_cache.register(TrendsetterBadge)

class FoundingFatherBadge(Badge):
    events = ['created_a_community']
    multiple = False
    levels = ['']
    slug = 'founding-father-badge'
    name = 'Founding Father'
    description = 'Started a community'

    def award(self, **state):
        return BadgeAwarded()
badge_cache.register(FoundingFatherBadge)

class HostingHeroBadge(Badge):
    events = ['created_an_event']
    multiple = False
    levels = ['']
    slug = 'hosting-hero-badge'
    name = 'Hosting Hero'
    description = 'Created an event'

    def award(self, **state):
        return BadgeAwarded()
badge_cache.register(HostingHeroBadge)

class GiftOfGabBadge(Badge):
    events = ['create_a_comment']
    multiple = False
    levels = ['Bronze', 'Silver', 'Gold']
    slug = 'gift-of-gab-badge'
    name = 'Gift Of Gab'
    description = '''
        <ul>
            <li>Bronze: Left one comment or question<li>
            <li>Silver: Left 5 comments or questions</li>
            <li>Gold: Left 15 comments or questions</li>
        </ul>
    '''

    def award(self, **state):
        user = state['user']
        num_of_comments = Comment.objects.filter(user=user).count()
        if num_of_comments >= 15:
            return BadgeAwarded(level=3)
        elif num_of_comments >= 5:
            return BadgeAwarded(level=2)
        return BadgeAwarded(level=1)
badge_cache.register(GiftOfGabBadge)

class ChampionChallengerBadge(Badge):
    events = ['created_a_challenge']
    multiple = False
    levels = ['']
    slug = 'champion-challenger-badge'
    name = 'Champion Challenger'
    description = 'Created a challenge'

    def award(self, **state):
        return BadgeAwarded()
#badge_cache.register(ChampionChallengerBadge)

