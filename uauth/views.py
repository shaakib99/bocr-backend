from urllib.request import Request
from rest_framework.decorators import api_view

from uauth.serializers.requestSerializers import RegisterSerializer, LoginSerializer, UpdateSerializer, GenerateNewVerificationTokenSerializer, GenerateNewPasswordResetTokenSerializer, ResetPasswordSerializer, VerifyAccountSerializer
from uauth.serializers.authSerializer import AuthSerializer
from common.decorators import responsify


@api_view(['POST'])
@responsify
def register(request: Request):
    serilizer = RegisterSerializer(data=request.data)
    serilizer.is_valid(raise_exception=True)

    auth = AuthSerializer(data=serilizer.validated_data)
    return auth.create()


@api_view(['POST'])
@responsify
def login(request: Request):
    serilizer = LoginSerializer(data=request.data)
    serilizer.is_valid(raise_exception=True)
    auth = AuthSerializer(data=serilizer.validated_data)
    return auth.login()


@api_view(['PATCH'])
@responsify
def update(request: Request):
    serilizer = UpdateSerializer(data=request.data)
    serilizer.is_valid(raise_exception=True)

    auth = AuthSerializer(data=serilizer.validated_data)
    return auth.update()


@api_view(['GET'])
@responsify
def generateNewVerificationToken(request: Request):
    serilizer = GenerateNewVerificationTokenSerializer(data=request.data)
    serilizer.is_valid(raise_exception=True)

    auth = AuthSerializer(data=serilizer.validated_data)
    return auth.generateNewVerificationToken()


@api_view(['GET'])
@responsify
def generateNewPasswordResetToken(request: Request):
    serilizer = GenerateNewPasswordResetTokenSerializer(data=request.data)
    serilizer.is_valid(raise_exception=True)

    auth = AuthSerializer(data=serilizer.validated_data)
    return auth.genreateNewPasswordResetToken()


@api_view(['POST'])
@responsify
def resetPassword(request: Request):
    serilizer = ResetPasswordSerializer(data=request.data)
    serilizer.is_valid(raise_exception=True)

    auth = AuthSerializer(data=serilizer.validated_data)
    return auth.resetPassword()


@api_view(['GET'])
@responsify
def verifyAccount(request: Request):
    serilizer = VerifyAccountSerializer(data=request.data)
    serilizer.is_valid(raise_exception=True)

    auth = AuthSerializer(data=serilizer.validated_data)
    return auth.verifyAccount()