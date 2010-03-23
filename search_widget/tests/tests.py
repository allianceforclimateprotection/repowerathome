from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from models import Post

class SearchViewTest(TestCase):
    urls = "search_widget.tests.urls_all_by_2"
    fixtures = ["test_search_widget.json",]
    
    def setUp(self):
        self.client = Client()
        self.url = reverse("search_widget-search")
        
    def test_no_search(self):
        response = self.client.get(self.url)
        self.failUnlessEqual(list(response.context["object_list"]), [])
        self.failUnlessEqual(response.context["has_next"], False)
        
    def test_post_search(self):
        self.urls = "search_widget.tests.urls_all_by_2"
        self._urlconf_setup()
        
        response = self.client.get(self.url, {"search": "Post"})
        object_list = response.context["object_list"]
        self.failUnlessEqual(len(object_list), 2)
        self.failUnlessEqual(object_list[0].name, "first name")
        self.failUnlessEqual(object_list[1].name, "second name")
        self.failUnlessEqual(response.context["has_next"], True)
        self.failUnlessEqual(response.context["pages"], 3)
        page_obj = response.context["page_obj"]
        
        response = self.client.get(self.url, {"search": "Post", "page": page_obj.next_page_number()})
        object_list = response.context["object_list"]
        self.failUnlessEqual(object_list[0].name, "third name")
        self.failUnlessEqual(object_list[1].name, "4th name")
        self.failUnlessEqual(response.context["has_next"], True)
        self.failUnlessEqual(response.context["pages"], 3)
        
    def test_posting_search(self):
        self.urls = "search_widget.tests.urls_posting_by_3"
        self._urlconf_setup()
        
        response = self.client.get(self.url, {"search": "Post"})
        object_list = response.context["object_list"]
        self.failUnlessEqual(len(object_list), 3)
        self.failUnlessEqual(object_list[0].name, "first name")
        self.failUnlessEqual(object_list[1].name, "second name")
        self.failUnlessEqual(object_list[2].name, "third name")
        self.failUnlessEqual(response.context["has_next"], False)
        self.failUnlessEqual(response.context["pages"], 1)
        
    def test_only_by_name(self):
        self.urls = "search_widget.tests.urls_only_name_by_4"
        self._urlconf_setup()
        
        response = self.client.get(self.url, {"search": "Post"})
        self.failUnlessEqual(list(response.context["object_list"]), [])
        self.failUnlessEqual(response.context["has_next"], False)
        self.failUnlessEqual(response.context["pages"], 1)
        
        response = self.client.get(self.url, {"search": "name"})
        object_list = response.context["object_list"]
        self.failUnlessEqual(len(object_list), 4)
        self.failUnlessEqual(object_list[0].name, "first name")
        self.failUnlessEqual(object_list[1].name, "second name")
        self.failUnlessEqual(object_list[2].name, "third name")
        self.failUnlessEqual(object_list[3].name, "4th name")
        self.failUnlessEqual(response.context["has_next"], True)
        self.failUnlessEqual(response.context["pages"], 2)
        page_obj = response.context["page_obj"]
        
        response = self.client.get(self.url, {"search": "name", "page": page_obj.next_page_number()})
        object_list = response.context["object_list"]
        self.failUnlessEqual(len(object_list), 2)
        self.failUnlessEqual(object_list[0].name, "5th name")
        self.failUnlessEqual(object_list[1].name, "6th name")
        self.failUnlessEqual(response.context["has_next"], False)
        self.failUnlessEqual(response.context["pages"], 2)