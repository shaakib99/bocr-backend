from rest_framework import serializers
from userUploads.models import UserUploads


class UserImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserUploads
        fields = '__all__'
