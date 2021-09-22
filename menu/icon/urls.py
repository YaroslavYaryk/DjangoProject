from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page
from rest_framework import routers

router = routers.SimpleRouter()

router.register(r"categories_s", CategoryView, basename="category")


urlpatterns = [
    path("", Home_page.as_view(), name="home"),
    path("someth/", get_someth),
    path("storage/", storage),
    path("add_page_model/", NewsStore.as_view(), name="add_page_model"),
    path("edit/<slug:slug_name>", WomanEditView.as_view(), name="edit_page_model"),
    path("delete/<slug:slug_title>",
         WomanDeleteView.as_view(), name="delete_page_model"),
    path("about/", cache_page(60 * 15)(WomanAbout.as_view()), name="about"),
    path("post/<slug:slug_id>", NewsNyCategory.as_view(), name="post"),
    # path("categories/<path:category_name>", cache_page(60)(WomanCategory.as_view()),
    #      name="category"),  # adding name to the path with cache 60 seconds
    # it's gonna be "categories/{name of category}"
    path("categories/<path:category_name>", WomanCategory.as_view(),
         name="category"),
    # path("edit_comment/", WomanCommentEdit.as_view(), name = "edit_comment")  ,  

    path("likes/<slug:pk>", likeView, name = "like_post"),
    path("comment/like/<int:like_id>", commentLikeView, name = "comment_like"),
    path("tmp_views/", tmp_views),
    path("django_boottstrap/", django_boottstrap, name = "django_boottstrap"),
    path("woman/", WomanView.as_view()),
    path("woman/<int:pk>", WomanDetailView.as_view())
    
] + router.urls

