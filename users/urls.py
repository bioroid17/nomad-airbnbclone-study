from django.urls import path
from .views import UserTweets

urlpatterns = [
    path("<int:id>/tweets", UserTweets.as_view()),
]
