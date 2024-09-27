from django.contrib import admin
from .models import Tweet, Like


# Register your models here.
@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "payload",
    )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "tweet",
    )
