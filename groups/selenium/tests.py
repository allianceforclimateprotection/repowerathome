from selenium.selenium import selenium
import unittest, time, re

from django.conf import settings

class CreateDeleteGroup(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, settings.SELENIUM_BROWSER, settings.SELENIUM_URL)
        self.selenium.start()
    
    def test_create_delete_group(self):
        sel = self.selenium
        sel.open("/")
        sel.click("link=Login")
        sel.wait_for_page_to_load("30000")
        sel.type("id_email", "test@repowerathome.com")
        sel.type("id_password", "repotest10")
        sel.click("//input[@value='Login']")
        sel.wait_for_page_to_load("30000")
        sel.click("link=Create a group")
        sel.wait_for_page_to_load("30000")
        sel.type("id_name", "test group")
        sel.key_up("id_name", "p")
        sel.type("id_description", "creating a test group")
        sel.click("//input[@value='Create Group']")
        sel.wait_for_page_to_load("30000")
        try: self.failUnless(sel.is_text_present("test group has been created."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("test group", sel.get_text("//h1/a"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=Edit Group")
        sel.wait_for_page_to_load("30000")
        sel.click("delete_group")
        sel.wait_for_page_to_load("30000")
        self.failUnless(re.search(r"^Are you sure you delete\? This cannot be undone\.$", sel.get_confirmation()))
        try: self.failUnless(sel.is_text_present("test group has been deleted."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=Logout")
        sel.wait_for_page_to_load("30000")
        try: self.failUnless(sel.is_text_present("You have successfully logged out."))
        except AssertionError, e: self.verificationErrors.append(str(e))
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
