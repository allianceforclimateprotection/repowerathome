from django.contrib.sitemaps import Sitemap
from datetime import datetime

class GenericUrl(object):
    def __init__(self, loc):
        self.location = loc
        
class RahSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5
    lastmod = datetime.now()
    
    def items(self):
        """Add urls here and they will be added to sitemap.xml"""
        urls = [
            "/actions/",
            "/teams/",
            "/",
            "/user/list/",
        ]
        return [GenericUrl(url) for url in urls]
    
    def location(self, obj):
        return obj.location