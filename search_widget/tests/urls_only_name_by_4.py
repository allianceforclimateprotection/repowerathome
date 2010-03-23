from django.conf.urls.defaults import *

from search_widget.views import search_list

from models import Post

search_info = {
    'queryset': Post.objects.all(),
    'paginate_by': 4,
    'search_fields': ['name',],
}

urlpatterns = patterns('',
    url(r'^search/$', search_list, search_info, name='search_widget-search'),
)