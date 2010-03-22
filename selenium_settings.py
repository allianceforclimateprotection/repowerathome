try:
    from test_settings import *
except ImportError:
    print 'settings could not be imported'

INSTALLED_APPS = (
    'rah.selenium',
    'groups.selenium',
)

TEST_RUNNER = 'selenium_test_runner.run_tests'

SELENIUM_BROWSERS = (
    '*firefox',
    '*safari',
)
SELENIUM_URL = 'http://localhost:8001'