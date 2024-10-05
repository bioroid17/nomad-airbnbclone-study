from rest_framework import serializers
from users.serializers import TinyUserSerializer
from .models import Tweet


class TweetSerializer(serializers.ModelSerializer):

    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = "__all__"
