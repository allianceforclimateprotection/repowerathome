from smtplib import SMTPException

from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.db import models
from django.template import Context, loader
from django.utils.translation import ugettext_lazy as _

class FlagManager(models.Manager):
    
    def has_user_flagged_object(self, content_object, user):
        if not user.is_authenticated():
            return False    
        content_type = ContentType.objects.get_for_model(content_object)
        return self.filter(content_type=content_type, object_pk=content_object.pk, user=user).exists()
            
    def get_flagged_object_for_user(self, content_object, user):
        if user.is_authenticated():
            content_type = ContentType.objects.get_for_model(content_object)
            try:
                return self.get(content_type=content_type, object_pk=content_object.pk, user=user)
            except Flag.DoesNotExist: pass
        return Flag(content_object=content_object)
            
    def flag_content(self, content_object, user):
        if user.is_authenticated():
            content_type = ContentType.objects.get_for_model(content_object)
            try:
                self.get(content_type=content_type, object_pk=content_object.pk, user=user)
            except Flag.DoesNotExist:
                self.create(content_type=content_type, object_pk=content_object.pk, user=user)
                return True
        return False
        
    def unflag_content(self, content_object, user):
        if user.is_authenticated():
            content_type = ContentType.objects.get_for_model(content_object)
            try:
                self.get(content_type=content_type, object_pk=content_object.pk, user=user).delete()
                return True
            except Flag.DoesNotExist:
                pass
        return False

class Flag(models.Model):
    """
    An instance of this class suggests that some user has flagged content as inappropriate
    or offensive.
    """
    content_type = models.ForeignKey(ContentType, verbose_name=_("content type"), related_name="%(class)s")
    object_pk = models.PositiveIntegerField(_("object ID"))
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")
    user = models.ForeignKey(User, verbose_name=_("name"), related_name="%(class)s_rating")
    submit_date = models.DateTimeField(_("date/time submitted"), auto_now=True)
    
    objects = FlagManager()
    
    class Meta:
        db_table = "flagged_flags"
        ordering = ("submit_date",)
        verbose_name = _("flag")
        verbose_name_plural = _("flags")
        unique_together = ("content_type", "object_pk", "user",)
        
    def __unicode__(self):
        return u"%s has flagged %s" % (self.user, self.content_object)
        
def inform_feedback_of_flag(sender, instance, **kwargs):
    template = loader.get_template("flagged/email.html")
    context = { "flag": instance, "domain": Site.objects.get_current().domain, }
    try:
        send_mail("Content Flagged", template.render(Context(context)), None, ["feedback@repowerathome.com"], fail_silently=False)
        return True
    except SMTPException, e:
        pass
    return False

models.signals.post_save.connect(inform_feedback_of_flag, sender=Flag)