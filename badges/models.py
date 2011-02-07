from django.db import models

from actions.models import UserActionProgress

from brabeion import badges as badge_cache

def possibly_award_badge(sender, instance, created, **kwargs):
    if instance.is_completed:
        import badges # this is a hack to make sure all Badge Classes have been loaded into the BadgeCache
        from badges import event_name
        badge_cache.possibly_award_badge(event_name(instance.action), user=instance.user)
models.signals.post_save.connect(possibly_award_badge, sender=UserActionProgress)
