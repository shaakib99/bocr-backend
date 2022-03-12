from rest_framework import serializers
from uploads.models import Uploads
from recognition.serializers.recognitionSerializer import RecognitionSerializer


class UploadImagesSerializer(serializers.ModelSerializer):
    recid = RecognitionSerializer()
    class Meta:
        model = Uploads
        fields = ['id', 'uid', 'recid', 'isDeleted']
