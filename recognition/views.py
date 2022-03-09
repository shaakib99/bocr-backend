from datetime import datetime
import json
from urllib.request import Request
from rest_framework.decorators import api_view
from bocr.settings import IMG_BB_URL, IMGBB_API_KEY
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import Recognition as RecognitionModel
from .serializers.recognitionSerializer import RecognizerSerializer
from rest_framework.status import HTTP_503_SERVICE_UNAVAILABLE
from rest_framework.exceptions import NotFound
import requests
import base64


@api_view(["GET", "PUT"])
def recognition(request: Request):
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

                recognitionModel = RecognitionModel(**result)
                recognitionModel.save()

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
