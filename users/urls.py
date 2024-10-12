from django.urls import path
from .views import Users, UserProfile, UserTweets, UserPassword, LogIn, LogOut

urlpatterns = [
    path("", Users.as_view()),
    path("<int:pk>", UserProfile.as_view()),
    path("<int:pk>/tweets", UserTweets.as_view()),
    path("password", UserPassword.as_view()),
    path("login", LogIn.as_view()),
    path("logout", LogOut.as_view()),
]
