from django.test.testcases import TestCase
from django.test import Client
from django.urls import  reverse
from icon.views import *
from icon.models import Woman, Category, WomanLike


class ViewsTest(TestCase):

    def setUp(self):
        self.category1 = Category.objects.create(
            name = "new category"
        )
        self.user = User.objects.create(
            username = "yaroslav",
        )
        self.post = Woman.objects.create(
            title = "new post",
            cat = self.category1
        )
        self.category2 = Category.objects.create(
            name = "new category2"
        )


    def test_is_category_slug_correct(self):
        self.assertEquals(self.category1.slug, "new-category")    


    def test_is_like_created(self):

        self.like = WomanLike.objects.create(
            user = self.user,
            post = self.post
        )

        self.assertIn(self.like, WomanLike.objects.all())


    def test_get_absolute_url(self):
        post_news=Woman.objects.get(id=1)
        #This will also fail if the urlconf is not defined.
        self.assertEquals(post_news.get_absolute_url(),f'/post/{post_news.slug}')    


    def test_first_name_label(self):
        post=Woman.objects.get(id=1)
        field_label = post._meta.get_field('cat').verbose_name
        self.assertEquals(field_label,'Category')    


    def test_create_category_without_posts(self):
        
        cat = Category.objects.get(name="new category2").woman_set.first()
        self.assertIsNone(cat)    

    def test_create_and_add_post(self):
        
        cat = Category.objects.get(name="new category").woman_set.first()
        self.assertIsNotNone(cat)   