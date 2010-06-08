from django.contrib.sitemaps import Sitemap
from groups.models import Group

class GroupSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Group.objects.filter(is_geo_group=False)

    def lastmod(self, obj):
        return obj.updated