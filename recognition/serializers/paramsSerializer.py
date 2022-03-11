from rest_framework import serializers


class ParamsSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
