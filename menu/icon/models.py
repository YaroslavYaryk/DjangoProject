from django.db import models

# Create your models here.
from django.urls import reverse
import re
from django.core.validators import RegexValidator
from django.utils.text import slugify
from django.db.models import *
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models.functions import *


class WomanFlterShowLenContent(models.Manager):

    """create manager that show len title and content and compare them"""

    def get_queryset(self):
        return Woman.objects.annotate(len_t = Length('title'), len_c = Length("content"))
        

class WomanFilterManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().order_by("creation_date")


class CountCategory(models.Manager):

    def get_queryset(self):
        return super().get_queryset().annotate(cnt=Count("woman"))


class CountWiews(models.Manager):

    def get_queryset(self):
        return super().get_queryset().annotate(max_view=Max("woman__view"))

# Create your models here.

class IpModel(models.Model):

    """class for getting ip adress of anyone"""
    post_news = models.ForeignKey("Woman", related_name="ip", on_delete=models.CASCADE, null=True)
    ip = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.ip}"
    

class Woman(models.Model):

    """creating fields in databace"""

    title = models.CharField(max_length=100, unique=True)

    slug = models.SlugField(max_length=255,
                            unique=True,
                            db_index=True,
                            verbose_name="URL",
                            null=True,
                            )

    content = models.TextField(blank=True)  # is not required to be filled

    # date set only one time and never changes
    creation_date = models.DateTimeField(auto_now_add=True)

    # if we change someth date will change
    updation_date = models.DateTimeField(auto_now=True)

    # will upload photo to this path
    photo = models.ImageField(upload_to="photos/Data%y/%m/%d/", blank=True)

    is_published = models.BooleanField(default=True)  # default is True

    cat = models.ForeignKey("Category", on_delete=models.PROTECT,
                            verbose_name="Category"
                            )  # add field from another model

    notes = GenericRelation('Note')

    objects = models.Manager()

    sorted_objects = WomanFilterManager()

    show_lengths = WomanFlterShowLenContent()

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Woman, self).save(*args, **kwargs)     

    def get_slag(self):
        return str(self.title).replace(" ", "_")

    def get_absolute_url(self):
        """to add link to path the same as title is"""
        return reverse("post", kwargs={"slug_id": self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Woman, self).save(*args, **kwargs)

    def get_date(self):
        return f"{self.creation_date.day} : {self.creation_date.month} : {self.creation_date.year}"

    def delete(self, *args, **kwargs):
        """delete photo after deleting post"""

        self.photo.delete(save=False)
        super().delete(*args, **kwargs)

    def get_view_count(self):
        return self.ip.count()    
    

    # def get_total_view(self):
    #     return self.views.count()    

    class Meta:

        """our model display in django-admin"""
        verbose_name = "New"
        verbose_name_plural = "News"
        ordering = ["-creation_date"]  # sorting news at site
        get_latest_by = "creation_date"



class Category(models.Model):

    """creating fields in databace"""

    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255,
                            unique=True,
                            db_index=True,
                            verbose_name="URL",
                            null=True,
                            )
    ico = models.ImageField(
        upload_to="icons/Data%y/%m/%d/", null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Category, self).save(*args, **kwargs)    

    def __str__(self):
        return str(self.name).lower()

    def get_slug_cat(self):
        return str(self.slug)

    def get_absolute_url(self):
        return reverse("category", kwargs={"category_name": self.slug})

    objects = models.Manager()

    sorted_objects = WomanFilterManager()

    count_cat = CountCategory()

    max_view = CountWiews()

    class Meta:

        """our model display in django-admin"""
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]  # sorting categories at site


class WomanImage(models.Model):
    post = models.ForeignKey(Woman, default=None, on_delete=models.CASCADE)
    images = models.FileField(upload_to="photos/Data%y/%m/%d/")

    def __str__(self):
        return self.post.title

    class Meta:

        """our model display in django-admin"""
        verbose_name = "Image"
        verbose_name_plural = "Images"
        ordering = ["id"]  # sorting categories at site


class WomanComment(models.Model):

    """Model for creating comment part """
    post = models.ForeignKey(
        Woman, related_name="all_comments", on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    comment = models.TextField(max_length=200)
    creation_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="com_likes", blank=True)
    notes = GenericRelation('Note')

    def __str__(self):
        return self.comment[:30]

    def get_comment_likes(self):
        return self.likes.count()

    class Meta:

        """our model display in django-admin"""
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["creation_date"]  # sorting categories at site



class WomanLike(models.Model):

    """ add like to our post """

    post = models.ForeignKey(
        Woman, related_name="likes", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="likes",
                             on_delete=models.CASCADE)


class LikedComment(models.Model):
    """Class container thats gonna consist user that already liked comment"""

    post_comment = models.ForeignKey(
        WomanComment, related_name="likes_comment", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="likes_comment",
                             on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=False, name="is_liked")
    choice = models.CharField(max_length=50, default="No")

    def __str__(self):
        return str(self.post_comment) if len(str(self.post_comment)) < 100 else str(self.post_comment)[:100]


class Note(models.Model):

    """class for taking notes for post and comment"""

    content = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type',fk_field= 'object_id')
