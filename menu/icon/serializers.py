from os import read
from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Category, Woman

class WomanSerializer(serializers.ModelSerializer):
    """ woman fields"""

    cat = serializers.SlugRelatedField(slug_field="name", read_only = True)
    class Meta:
        model = Woman
        fields = "__all__"


class WomanDetailSerializer(serializers.ModelSerializer):
    """ woman detail fields"""

    cat = serializers.SlugRelatedField(slug_field="name", read_only = True)
    class Meta:
        model = Woman
        exclude = ("is_published",) 


class CategorySerializer(serializers.ModelSerializer):
    """ Category serializer """

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "slug",
            "ico",
        )