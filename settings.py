import sys, os

from utils import local_join

sys.path.insert(0, local_join('lib'))

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = local_join('static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Caching
CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
CACHE_MIDDLEWARE_SECONDS = 60 * 60
CACHE_MIDDLEWARE_KEY_PREFIX = os.path.dirname(__file__)[:12] # This is enough for /scripts/{pr|de|st}

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    # 'django.middleware.transaction.TransactionMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'facebook_app.context_processors.facebook_appid',
    'records.context_processors.ask_to_share',
)

TEMPLATE_DIRS = (
    local_join('templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.comments',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'django.contrib.flatpages',
    'rah',
    'rateable',
    'records',
    'geo',
    'basic.blog',
    'basic.inlines',
    'tagging',
    'twitter_app',
    'django_extensions',
    'groups',
    'search_widget',
    'sorl.thumbnail',
    'flagged',
    'invite',
    'dated_static',
    'notification',
    'actions',
    'events',
    'migrations',
    'messaging',
    'facebook_app',
)

FIXTURE_DIR = ('fixtures',)

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda user: "/user/%s/" % user.id,
}

AUTHENTICATION_BACKENDS = ('rah.backends.EmailBackend',)
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "/login"
LOGOUT_URL = "/logout"
AUTH_PROFILE_MODULE = 'rah.Profile'

MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'
GA_TRACK_PAGEVIEW = 50
MESSAGE_TAGS = {
    GA_TRACK_PAGEVIEW: 'ga_track_pageview',
}

# sync media s3
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_BUCKET_NAME = 'rahstatic'
FILTER_LIST = ['.DS_Store', '.svn', '.hg', '.git', 'Thumbs.db', 'minify', 'group_images', '*.psd', '*.eps']
GZIP_CONTENT_TYPES = (
    'text/css',
    'application/javascript',
    'application/x-javascript'
)

COMMENTS_ALLOW_PROFANITIES = True

IGNORABLE_404_ENDS = ('.google-analytics.com/ga.js/', '/b.js/')

THUMBNAIL_EXTENSION = 'png'

MYSQLDUPLICATE_EXCLUDE = ("django_site",)

# Date defaults
DATETIME_FORMAT = "F j, Y, P"
DATE_FORMAT = "F j, Y"
TIME_FORMAT = "P"
SHORT_DATE_FORMAT = "m/d/Y"
SHORT_DATETIME_FORMAT = "m/d/Y P"
YEAR_MONTH_FORMAT = "F Y"
MONTH_DAY_FORMAT = "F j"
LONG_DATE_FORMAT = "l F j, Y"

try:
    from local_settings import *
except ImportError:
    print 'local_settings could not be imported'