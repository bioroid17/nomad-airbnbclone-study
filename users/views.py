from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from tweets.models import Tweet
from tweets.serializers import TweetSerializer
from .models import User


class UserTweets(APIView):

    def get_user(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise NotFound("User not found")

    def get(self, request, id):
        user = self.get_user(id)
        tweets = Tweet.objects.filter(user=user)
        serializer = TweetSerializer(tweets, many=True)

        return Response({"tweets": serializer.data})
