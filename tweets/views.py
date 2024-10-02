from django.shortcuts import render
from .models import Tweet


# Create your views here.
def get_all_tweets(request):
    tweets = Tweet.objects.all()
    return render(
        request,
        "all_tweets.html",
        {
            "title": "Title from django",
            "tweets": tweets,
        },
    )
