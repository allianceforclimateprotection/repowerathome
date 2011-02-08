from django.db import models

from actions.models import UserActionProgress

from brabeion import badges as badge_cache
from brabeion.models import BadgeAward

def all_badges(user=None):
    badges_dict = badge_cache._registry
    if user and user.is_authenticated():
        for award in BadgeAward.objects.filter(user=user):
            badges_dict[award.slug].awarded_at = award.awarded_at
    return badges_dict.values()

def get_badge(slug, user=None):
    badge = badge_cache._registry.get(slug, None)
    if badge and user and user.is_authenticated():
        try:
            award = BadgeAward.objects.get(slug=slug, user=user)
            badge.awarded_at = award.awarded_at
        except BadgeAward.DoesNotExist:
            pass
    return badge

def possibly_award_badge(sender, instance, created, **kwargs):
    if instance.is_completed:
        import badges # this is a hack to make sure all Badge Classes have been loaded into the BadgeCache
        from badges import event_name
        badge_cache.possibly_award_badge(event_name(instance.action), user=instance.user)
models.signals.post_save.connect(possibly_award_badge, sender=UserActionProgress)
