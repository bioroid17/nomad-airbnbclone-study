from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from tweets.models import Tweet
from tweets.serializers import TweetSerializer
from .models import User


@api_view(["GET"])
def get_user_tweets(request, id):
    if request.method == "GET":
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            raise NotFound("User not found")
        tweets = Tweet.objects.filter(user=user)
        serializer = TweetSerializer(tweets, many=True)

        return Response({"tweets": serializer.data})
