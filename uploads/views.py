from urllib.request import Request
from rest_framework.decorators import api_view
from helper.common.decorators import responsify
from helper.common.decorators import jwtAuthGuard
from .models import Uploads as UserUploadModel
from uploads.serializers.uploadsSerializer import UploadImagesSerializer
from drf_spectacular.utils import extend_schema
from helper.common.requestSerializer import JWTAuthGuard
from rest_framework import serializers


@extend_schema(parameters=[JWTAuthGuard(required=True)],
               responses={
                   200:
                   serializers.ListSerializer(child=UploadImagesSerializer())
               },
               tags=['User upload'])
@api_view(['GET'])
@responsify
@jwtAuthGuard
def userImages(request: Request, user):
    uploads = UserUploadModel.objects.filter(uid=user['id']).select_related()
    return UploadImagesSerializer(uploads, many=True).data
