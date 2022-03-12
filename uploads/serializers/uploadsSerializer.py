from rest_framework import serializers
from uploads.models import Uploads


class UserImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Uploads
        fields = '__all__'
