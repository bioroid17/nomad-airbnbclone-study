from django.urls import path
from .views import get_all_tweets

urlpatterns = [
    path("", get_all_tweets),
]
