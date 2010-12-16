from django.conf.urls.defaults import *

urlpatterns = patterns('media_widget.views',
    url(r'^sticker_upload/$', 'sticker_upload', name='sticker_upload'),
)
