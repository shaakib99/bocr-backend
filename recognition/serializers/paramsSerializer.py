from rest_framework import serializers


class RecognitionParamsSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)

class RecognitionImageUploadSerializer(serializers.Serializer):
    images = serializers.ImageField(required = True)
