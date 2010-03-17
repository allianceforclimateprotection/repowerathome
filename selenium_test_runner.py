import unittest

from django.conf import settings
from django.db.models import get_app, get_apps
from django.test.simple import DjangoTestSuiteRunner, build_suite, reorder_suite

SELENIUM_MODULE = "selenium.tests"

def run_tests(test_labels, verbosity=1, interactive=True, failfast=False, extra_tests=None):
    import warnings
    warnings.warn(
        'The run_tests() test runner has been deprecated in favor of DjangoTestSuiteRunner.',
        PendingDeprecationWarning
    )
    test_runner = DjangoTestSuiteRunner(verbosity=verbosity, interactive=interactive, failfast=failfast)
    for browser in settings.SELENIUM_BROWSERS:
        settings.SELENIUM_BROWSER = browser
        test_runner.run_tests(test_labels, extra_tests=extra_tests)