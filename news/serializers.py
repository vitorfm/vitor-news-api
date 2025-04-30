from rest_framework import serializers
from django.contrib.auth.models import User
from .models import News, Category, Subscription
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "is_staff"]
        read_only_fields = ["is_staff"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = [
            "id",
            "user",
            "is_pro",
            "has_poder",
            "has_tributos",
            "has_saude",
            "has_energia",
            "has_trabalhista",
        ]


class NewsSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    # Campos para escrita (IDs)
    author_id = serializers.IntegerField(write_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = News
        fields = [
            "id",
            "title",
            "subtitle",
            "image",
            "content",
            "pub_date",
            "scheduled_pub_date",
            "created_at",
            "updated_at",
            "author",
            "author_id",
            "status",
            "category",
            "category_id",
            "pro_only",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def create(self, validated_data):
        author_id = validated_data.pop("author_id")
        category_id = validated_data.pop("category_id")

        author = User.objects.get(id=author_id)
        category = Category.objects.get(id=category_id)

        news = News.objects.create(author=author, category=category, **validated_data)
        return news

    def update(self, instance, validated_data):
        if "author_id" in validated_data:
            author_id = validated_data.pop("author_id")
            instance.author = User.objects.get(id=author_id)

        if "category_id" in validated_data:
            category_id = validated_data.pop("category_id")
            instance.category = Category.objects.get(id=category_id)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
