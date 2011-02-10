from django.db import models
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment

from actions.models import UserActionProgress
from commitments.models import Commitment
from events.models import Event
from media_widget.models import StickerImage
from invite.models import Invitation

from brabeion import badges as badge_cache
from brabeion.models import BadgeAward

def all_badges(user=None):
    badges_dict = badge_cache._registry
    if user and user.is_authenticated():
        for award in BadgeAward.objects.filter(user=user):
            badges_dict[award.slug].awarded_at = award.awarded_at
    return badges_dict.values()

def get_badge(slug, user=None):
    badge = badge_cache._registry[slug]
    if user and user.is_authenticated():
        try:
            award = BadgeAward.objects.get(slug=slug, user=user)
            badge.awarded_at = award.awarded_at
        except BadgeAward.DoesNotExist:
            pass
    return badge

def possibly_award_action_badge(sender, instance, created, **kwargs):
    if instance.is_completed:
        import badges # this is a hack to make sure all Badge Classes have been loaded into the BadgeCache
        from badges import event_name
        badge_cache.possibly_award_badge(event_name(instance.action), user=instance.user)
models.signals.post_save.connect(possibly_award_action_badge, sender=UserActionProgress)

def possibly_award_trendsetter_badge(sender, instance, created, **kwargs):
    if created and instance.question == 'pledge':
        badge_cache.possibly_award_badge('took_the_pledge', user=instance.contributor.user)
models.signals.post_save.connect(possibly_award_trendsetter_badge, sender=Commitment)

def possibly_award_hosting_hero_badge(sender, instance, created, **kwargs):
    if created:
        badge_cache.possibly_award_badge('created_an_event', user=instance.creator)
models.signals.post_save.connect(possibly_award_hosting_hero_badge, sender=Event)

def possibly_award_gift_of_gab_badge(sender, instance, created, **kwargs):
    if created:
        badge_cache.possibly_award_badge('created_a_comment', user=instance.user)
models.signals.post_save.connect(possibly_award_gift_of_gab_badge, sender=Comment)

def possibly_award_paparazzi_badge(sender, instance, created, **kwargs):
    if instance.approved:
        try:
            user = User.objects.get(email=instance.email)
            badge_cache.possibly_award_badge('uploaded_an_image', user=user)
        except User.DoesNotExist:
            pass
models.signals.post_save.connect(possibly_award_paparazzi_badge, sender=StickerImage)

def possibly_award_momentum_builder_badge(sender, instance, created, **kwargs):
    if created:
        badge_cache.possibly_award_badge('invited_a_friend', user=instance.user)
models.signals.post_save.connect(possibly_award_momentum_builder_badge, sender=Invitation)
