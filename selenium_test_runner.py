import os, time, threading, signal, subprocess, unittest

from django.conf import settings
from django.db.models import get_app, get_apps
from django.test.simple import DjangoTestSuiteRunner, build_suite, reorder_suite

SELENIUM_MODULE = "selenium.tests"

class ServerThread(threading.Thread):
    def __init__(self, command):
        threading.Thread.__init__(self)
        self.command = command
        self.process = None
    
    def run(self):
        self.process = subprocess.Popen(self.command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.process.communicate()
    
    def stop(self):
        if self.process:
            self.process.kill()
        self.process = None

def run_tests(test_labels, verbosity=1, interactive=True, failfast=False, extra_tests=None):
    import warnings
    warnings.warn(
        'The run_tests() test runner has been deprecated in favor of DjangoTestSuiteRunner.',
        PendingDeprecationWarning
    )
    selenium_server = ServerThread(["java", "-jar", "lib/selenium/selenium-server.jar"])
    selenium_server.start()
    if settings.SELENIUM_URL == "http://localhost:8001":
        dev_server = ServerThread(["python", "manage.py", "runserver", "8001"])
        dev_server.start()
    time.sleep(5)
    test_runner = DjangoTestSuiteRunner(verbosity=verbosity, interactive=interactive, failfast=failfast)
    for browser in settings.SELENIUM_BROWSERS:
        settings.SELENIUM_BROWSER = browser
        test_runner.run_tests(test_labels, extra_tests=extra_tests)
    selenium_server.stop()
    if settings.SELENIUM_URL == "http://localhost:8001":
        dev_server.stop()