from rest_framework import serializers
from uauth.models import User


class LoginResponseSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=200)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', "token"]


class UserResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'isActive']
