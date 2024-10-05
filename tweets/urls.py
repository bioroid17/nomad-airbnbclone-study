from django.urls import path
from .views import Tweets

urlpatterns = [
    path("", Tweets.as_view()),
]
