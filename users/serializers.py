from rest_framework import serializers


class TinyUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    name = serializers.CharField()
