from urllib.request import Request
from rest_framework.decorators import api_view
from common.decorators import jwtAuthGuard
from .models import UserUpload as UserUploadModel


@api_view(['GET'])
@jwtAuthGuard
def userImages(request: Request, user):
    return UserUploadModel.objects.filter(uid=user['id'])
