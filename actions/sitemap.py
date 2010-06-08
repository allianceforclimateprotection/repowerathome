from django.contrib.sitemaps import Sitemap
from actions.models import Action

class ActionSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Action.objects.all()

    def lastmod(self, obj):
        return obj.updated