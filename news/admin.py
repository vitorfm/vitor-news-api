from django.contrib import admin
from .models import News, Category, Subscription


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "status", "pub_date", "pro_only")
    list_filter = ("status", "category", "pro_only")
    search_fields = ("title", "subtitle", "content")
    date_hierarchy = "created_at"
    raw_id_fields = ("author",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "is_pro",
        "has_poder",
        "has_tributos",
        "has_saude",
        "has_energia",
        "has_trabalhista",
    )
    list_filter = (
        "is_pro",
        "has_poder",
        "has_tributos",
        "has_saude",
        "has_energia",
        "has_trabalhista",
    )
    search_fields = ("user__username", "user__email")
