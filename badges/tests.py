
from django.test import TestCase

from models import all_badges, get_badge

class BadgeTest(TestCase):
    fixtures = ['actions.json']

    def setUp(self):
        import badges

    def test_all_badges(self):
        badges = all_badges()
        self.failUnlessEqual(len(badges), 37)

    def test_get_badge(self):
        thermostat_badge = get_badge('dial-down-thermostat-action-badge')
        self.failUnlessEqual(thermostat_badge.name, 'Dial down your thermostat')

        replace_windows = get_badge('replace-your-windows-action-badge')
        self.failUnlessEqual(replace_windows.name, 'Replace an old window')

        trendsetter = get_badge('trendsetter-badge')
        self.failUnlessEqual(trendsetter.name, 'Trendsetter')

        comment_badge = get_badge('gift-of-gab-badge')
        self.failUnlessEqual(comment_badge.name, 'Gift of Gab')

        momentum_badge = get_badge('momentum-builder-badge')
        self.failUnlessEqual(momentum_badge.name, 'Momentum Builder')
