from django.test.testcases import TestCase
from django.test import Client
from django.urls import  reverse
from icon.views import *
from icon.models import Woman, Category


class ViewsTest(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.category1 = Category.objects.create(
            name = "category1",
            ico = "../../assets/menu/img/5.jpg"
        )

    def test_home_page(self):

        response = self.client.get(reverse("home"))

        self.assertEquals(response.status_code, 200) #is get method
        self.assertTemplateUsed(response, 'icon/home.html') #is template is home.html


    def test_category_page(self):

        response = self.client.get(reverse("category", args=["category1"]))
        self.assertEquals(response.status_code, 200)
        

    def test_project_post_view_GET(self):


        self.obj = Woman.objects.create(
            cat = self.category1,
            title = "new post"
        )   
        self.post_url = reverse("post", args=[str(self.obj.slug)])

        response = self.client.get(self.post_url)


        self.assertEquals(self.category1.name, self.obj.cat.name)
        self.assertEquals(response.status_code, 200)

