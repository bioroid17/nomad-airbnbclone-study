from django.urls import path
from .views import get_user_tweets

urlpatterns = [
    path("<int:id>/tweets", get_user_tweets),
]
