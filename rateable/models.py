from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

class RatingManager(models.Manager):
    
    def get_users_current_score(self, content_object, user):
        if user.is_authenticated():
            content_type = ContentType.objects.get_for_model(content_object)
            current_rating = self.filter(content_type=content_type, object_pk=content_object.pk, user=user)
            if current_rating:
                return current_rating[0].score
        return None
        
    def create_or_update(self, content_type, object_pk, user, score):
        if not user.is_authenticated():
            return None, False
        try:
            rating = self.get(content_type=content_type, object_pk=object_pk, user=user)
            created = False
        except Rating.DoesNotExist:
            rating = Rating(content_type=content_type, object_pk=object_pk, user=user)
            created = True
        rating.score = score
        rating.save()
        return rating, created

class Rating(models.Model):
    """
    A user rating for some object.
    """
    content_type = models.ForeignKey(ContentType, verbose_name=_("content type"), related_name="%(class)s")
    object_pk = models.PositiveIntegerField(_("object ID"))
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")
    user = models.ForeignKey(User, verbose_name=_("name"), related_name="%(class)s_rating")
    score = models.IntegerField()
    submit_date = models.DateTimeField(_("date/time submitted"), auto_now=True)
    
    objects = RatingManager()
    
    class Meta:
        db_table = "rateable_ratings"
        ordering = ("submit_date",)
        verbose_name = _("rating")
        verbose_name_plural = _("ratings")
        unique_together = ("content_type", "object_pk", "user",)
        
    def __unicode__(self):
        return u"%s gave a %d" % (self.user, self.score)
    
    def get_content_object_url(self):
        """
        Get a URL suitable for redirecting to the content object.
        """
        return urlresolvers.reverse("ratings-url-redirect", args=(self.content_type_id, self.object_pk))