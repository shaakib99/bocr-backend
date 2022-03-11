from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers


def JWTAuthGuard(required=True):

    return OpenApiParameter(name='Authorization',
                            type=str,
                            location=OpenApiParameter.HEADER,
                            description='Required JWT Header',
                            required=required)

class QueryParams(serializers.Serializer):
    pass