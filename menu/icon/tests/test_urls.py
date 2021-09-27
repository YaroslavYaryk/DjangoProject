from django.test.testcases import TestCase
from django.urls import resolve, reverse
from icon.views import *


class TestUrls(TestCase):

    def test_home_urls(self):
        url = reverse("home")
        self.assertEquals(resolve(url).func.view_class, Home_page)


    def test_category_urls(self):
        url = reverse("add_page_model")
        self.assertEquals(resolve(url).func.view_class, NewsStore)


    def test_send_feedback_urls(self):
        url = reverse("send_feedback")
        self.assertEquals(resolve(url).func, send_feedback)        

    def test_about_urls(self):
        url = reverse("about")
        self.assertEquals(resolve(url).func.view_class, WomanAbout)     

    def test_sign_in_urls(self):
        url = reverse("sign_in")
        self.assertEquals(resolve(url).func.view_class, LoginUser)    