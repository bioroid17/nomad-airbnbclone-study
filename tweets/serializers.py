from rest_framework import serializers
from users.serializers import TinyUserSerializer
from .models import Tweet, Like


class TweetSerializer(serializers.ModelSerializer):

    user = TinyUserSerializer(read_only=True)

    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = "__all__"

    def get_is_liked(self, tweet):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return tweet.likes.filter(user=request.user).exists()
        else:
            return False
