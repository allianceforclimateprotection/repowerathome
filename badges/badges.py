from django.db import models
from django.contrib.comments.models import Comment

from settings import SITE_NAME
from actions.models import Action, UserActionProgress
from commitments.models import ContributorSurvey

from brabeion import badges as badge_cache
from brabeion.base import Badge, BadgeAwarded

def event_name(action):
    return '%s-action-completed' % action.slug

class ActionBadge(Badge):
    events = ['action_completed']
    multiple = False
    action = None
    levels = ['']
    slug = None

    def award(self, **state):
        if not self.action:
            raise NotImplementedError('%s can not be used as a badge' % self.__class__)
        user = state['user']
        if UserActionProgress.objects.filter(user=user, action=self.action,
                is_completed=True).exists():
            return BadgeAwarded()

    def get_name(self):
        return self.action.name
    name = property(get_name)

    def get_description(self):
        return 'Completed %s action' % self.action.name
    description = property(get_description)

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
    name = 'Gift of Gab'
    description = '''
        <ul>
            <li>Bronze: Left one comment or question</li>
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

class IdeaMachineBadge(Badge):
    events = ['create_a_comment']
    multiple = False
    levels = ['Bronze', 'Silver', 'Gold']
    slug = 'idea-machine-badge'
    name = 'Idea Machine'
    description = '''
        <ul>
            <li>Bronze: Shared one idea or tip</li>
            <li>Silver: Shared 5 ideas or tips</li>
            <li>Gold: Shared 15 ideas or tips</li>
        </ul>
    '''

    def award(self, **state):
        pass #TODO: this should be implemented when we have a new commenting system
#badge_cache.register(IdeaMachineBadge)

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

class PaparazziBadge(Badge):
    events = ['uploaded_an_image']
    multiple = False
    levels = ['']
    slug = 'paparazzi-badge'
    name = 'Paparazzi'
    description = 'Uploaded an image to an action, event or community'

    def award(self, **state):
        return BadgeAwarded()
badge_cache.register(PaparazziBadge)

class MomentumBuilderBadge(Badge):
    events = ['invited_a_friend']
    multiple = False
    levels = ['']
    slug = 'momentum-builder-badge'
    name = 'Momentum Builder'
    description = 'Invited friends to %s' % SITE_NAME

    def award(self, **state):
        return BadgeAwarded()
badge_cache.register(MomentumBuilderBadge)

class SocialMediaMavenBadge(Badge):
    events = ['linked_social_account']
    multiple = False
    levels = ['Silver', 'Gold']
    slug = 'social-media-maven-badge'
    name = 'Social Media Maven'
    description = '''
        <ul>
            <li>Silver: Linked Twitter or Facebook account to %s</li>
            <li>Gold: Linked both Twitter and Facebook accounts to %s</li>
        </ul>
    ''' % (SITE_NAME, SITE_NAME)

    def award(self, **state):
        user = state['user']
        profile = user.get_profile()
        if profile.twitter_access_token and profile.facebook_access_token:
            return BadgeAwarded(level=2)
        if profile.twitter_access_token or profile.facebook_access_token:
            return BadgeAwarded(level=1)
badge_cache.register(SocialMediaMavenBadge)

class FollowThroughBadge(Badge):
    events = ['entered_commitment_card']
    multiple = False
    levels = ['Bronze', 'Silver', 'Gold']
    slug = 'follow-through-badge'
    name = 'Follow Through'
    description = '''
        <ul>
            <li>Bronze: Entered 5 commitment cards</li>
            <li>Silver: Entered 15 commitment cards</li>
            <li>Gold: Entered 30 commitment cards</li>
        </ul>
    '''

    def award(self, **state):
        user = state['user']
        num_of_surveys = ContributorSurvey.objects.filter(entered_by=user).count()
        if num_of_surveys >= 30:
            return BadgeAwarded(level=3)
        elif num_of_surveys >= 15:
            return BadgeAwarded(level=2)
        elif num_of_surveys >= 5:
            return BadgeAwarded(level=1)
badge_cache.register(FollowThroughBadge)

class ShoutOutBadge(Badge):
    events = ['opted_to_share_activity']
    multiple = False
    levels = ['']
    slug = 'shout-out-badge'
    name = 'Shout Out'
    description = 'Opted to automatically share activity on Twitter or Facebook'

    def award(self, **state):
        return BadgeAwarded()
badge_cache.register(ShoutOutBadge)

class StorytellerBadge(Badge):
    events = ['completed_profile']
    multiple = False
    levels = ['']
    slug = 'storyteller-badge'
    name = 'StoryTeller'
    description = 'Completed profile'

    def award(self, **state):
        return BadgeAwarded()
badge_cache.register(StorytellerBadge)

class DoggedBadge(Badge):
    events = ['completed_a_commitment']
    multiple = False
    levels = ['Bronze', 'Silver', 'Gold']
    slug = 'dogged-badge'
    name = 'Dogged'
    description = '''
        <ul>
            <li>Bronze: Completed one commitment</li>
            <li>Silver: Completed 3 commitments</li>
            <li>Gold: Completed 5 commitments</li>
        </ul>
    '''

    def award(self, **state):
        user = state['user']
        num_dogged_actions = UserActionProgress.objects.filter(user=user, is_completed=True, 
                date_committed__isnull=False).count()
        if num_dogged_actions >= 5:
            return BadgeAwarded(level=3)
        elif num_dogged_actions >= 3:
            return BadgeAwarded(level=2)
        elif num_dogged_actions:
            return BadgeAwarded(level=1)
badge_cache.register(DoggedBadge)

class UnbelievableBadge(Badge):
    events = ['completed_an_action']
    multiple = False
    levels = ['']
    slug = 'unbelievable-badge'
    name = 'Unbelievable'
    description = 'Completed all the home energy actions'

    def award(self, **state):
        user = state['user']
        num_of_actions = Action.objects.all().count()
        num_of_completed = UserActionProgress.objects.filter(user=user, is_completed=True)
        if num_of_actions == num_of_completed:
            return BadgeAwarded()
badge_cache.register(UnbelievableBadge)
