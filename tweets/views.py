from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Tweet
from .serializers import TweetSerializer


class Tweets(APIView):

    def get(self, request):
        tweets = Tweet.objects.all()
        serializer = TweetSerializer(tweets, many=True)
        return Response({"tweets": serializer.data})
