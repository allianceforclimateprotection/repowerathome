from django.db import models

class ChallengeManager(models.Manager):
    def all_challenges(self, user=None):
        challenges = self.all()
        if user and user.is_authenticated():
            challenges = challenges.extra(select={'status':
                """
                SELECT CASE WHEN s.contributor_id IS NOT NULL THEN "completed" ELSE "" END
                FROM commitments_contributor c
                LEFT JOIN challenges_support s ON c.id = s.contributor_id
                WHERE c.user_id = %s AND s.challenge_id = challenges_challenge.id
                """}, select_params = (user.id,))
        return challenges

class Challenge(models.Model):
    title = models.CharField(max_length=75)
    description = models.TextField(blank=False)
    goal = models.IntegerField(help_text='How many petions do you want signed?')
    creator = models.ForeignKey('auth.user')
    supporters = models.ManyToManyField('commitments.contributor', through='Support')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = ChallengeManager()

    def number_of_supporters(self):
        return self.supporters.all().count()

    @models.permalink
    def get_absolute_url(self):
        return ('challenges_detail', [str(self.id)])

    def __unicode__(self):
        return self.title

class Support(models.Model):
    challenge = models.ForeignKey(Challenge)
    contributor = models.ForeignKey('commitments.contributor')
    send_updates = models.BooleanField(default=False)
    pledged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('challenge', 'contributor',)
