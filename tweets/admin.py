from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from .models import Tweet, Like


class ElonMuskFilter(admin.SimpleListFilter):
    title = "Filter by payload 'Elon Musk'"
    parameter_name = "contains__em"

    def lookups(self, request, model_admin) -> list[tuple[Any, str]]:
        return [
            ("yes", "Contain"),
            ("no", "Do not contain"),
        ]

    def queryset(self, request, tweets):
        if self.value() == "yes":
            return tweets.filter(payload__icontains="Elon Musk")
        elif self.value() == "no":
            return tweets.exclude(payload__icontains="Elon Musk")
        else:
            return tweets


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "payload",
        "total_likes",
    )

    search_fields = (
        "payload",
        "user__username",
    )

    list_filter = (
        "created_at",
        ElonMuskFilter,
    )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "tweet",
    )

    search_fields = ("user__username",)

    list_filter = ("created_at",)
