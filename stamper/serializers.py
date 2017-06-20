import base64

from rest_framework import serializers
from stamper.models import WebPage


class Base64Field(serializers.CharField):
    def to_representation(self, value):
        return base64.encodebytes(value)


class WebPageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    url = serializers.URLField()
    body = serializers.CharField(required=False)
    signature = Base64Field(required=False)
    status = serializers.CharField(required=False, source='get_status_display')


    def create(self, validated_data):
        return WebPage.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.url = validated_data.get('url', instance.url)
        instance.body = validated_data.get('body', instance.body)
        instance.signature = validated_data.get('signature', instance.signature)
        instance.save()
        return instance
