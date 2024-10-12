from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Tweet
from .serializers import TweetSerializer


class Tweets(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        tweets = Tweet.objects.all()
        serializer = TweetSerializer(
            tweets,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = TweetSerializer(data=request.data)
        if serializer.is_valid():
            tweet = serializer.save(user=request.user)
            return Response(TweetSerializer(tweet).data)
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class TweetDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_tweet(self, pk):
        try:
            return Tweet.objects.get(pk=pk)
        except Tweet.DoesNotExist:
            raise NotFound("Tweet not found.")

    def get(self, request, pk):
        tweet = self.get_tweet(pk)
        serializer = TweetSerializer(
            tweet,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        tweet = self.get_tweet(pk)
        if tweet.user != request.user:
            raise PermissionDenied

        serializer = TweetSerializer(
            tweet,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_tweet = serializer.save()
            return Response(
                TweetSerializer(
                    updated_tweet,
                    context={"request": request},
                ).data
            )
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        tweet = self.get_tweet(pk)
        if tweet.user != request.user:
            raise PermissionDenied
        tweet.delete()
        return Response(status=HTTP_204_NO_CONTENT)
