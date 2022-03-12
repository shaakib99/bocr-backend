from datetime import datetime
import json
from urllib.request import Request
from rest_framework.decorators import api_view
from bocr.settings import IMG_BB_URL, IMGBB_API_KEY
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import Recognition as RecognitionModel
from .serializers.recognitionSerializer import RecognizerSerializer, RecognitionSerializer
from rest_framework.status import HTTP_503_SERVICE_UNAVAILABLE
from rest_framework.exceptions import NotFound
from helper.common.decorators import responsify, jwtAuthGuardExcept
from uploads.models import Uploads
from drf_spectacular.utils import extend_schema
from recognition.serializers.paramsSerializer import RecognitionParamsSerializer, RecognitionImageUploadSerializer
from helper.common.requestSerializer import JWTAuthGuard
from uauth.models import User
from rest_framework import serializers
import requests
import base64


@extend_schema(parameters=[RecognitionParamsSerializer],
               methods=['GET'],
               responses={200: RecognitionSerializer},
               tags=['Recognition'])
@extend_schema(
    parameters=[
        JWTAuthGuard(required=False),
    ],
    request=serializers.ListSerializer(child = RecognitionImageUploadSerializer()),
    methods=['PUT'],
    responses={200: serializers.ListSerializer(child=RecognitionSerializer())},
    tags=['Recognition'])
@api_view(["GET", "PUT"])
@jwtAuthGuardExcept
@responsify
def recognition(request: Request, user=None):
    if request.method.lower() == 'put':
        finalResult = []
        images: list[InMemoryUploadedFile] = request.FILES.getlist('images')
        for img in images:
            data = {
                "image": base64.b64encode(img.read()).decode(),
            }
            response = requests.post(IMG_BB_URL,
                                     params={"key": IMGBB_API_KEY},
                                     data=data)
            response = json.loads(response.content)

            if 'status' in response and response[
                    'status'] == 200 and 'success' in response and response[
                        'success'] == True:
                url = response['data']['image']['url']

                result = RecognizerSerializer(data={"uri": url}).getResult()
                result['cAt'] = datetime.now().timestamp()

                recognitionModel = RecognitionModel.objects.filter(uri=url).first()

                recognitionModel.update_or_create(**result)

                if user:
                    userUploadModel = Uploads.objects.create(
                        uid=User.objects.filter(id = user['id']).first(), recid=recognitionModel)
                    userUploadModel.save()

                finalResult.append(result)
            else:
                return {
                    "status_code": HTTP_503_SERVICE_UNAVAILABLE,
                    "message": response['message']
                }
        return finalResult

    else:
        id = request.GET['id']
        recognition: RecognitionModel = RecognitionModel.objects.filter(
            id=id).first()

        if not recognition:
            raise NotFound('Image not found')
        result = RecognizerSerializer(data={"uri": url}).getResult()
        result = RecognitionModel.objects.filter(id=id).update(
            **result).__dict__()
        return result
