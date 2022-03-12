from urllib.request import Request
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema


from uauth.serializers.requestSerializers import RegisterSerializer, LoginSerializer, UpdateSerializer, GenerateNewVerificationTokenSerializer, GenerateNewPasswordResetTokenSerializer, ResetPasswordSerializer, VerifyAccountSerializer
from uauth.serializers.responseSerializers import LoginResponseSerializer, UserResponseSerializer
from uauth.serializers.authSerializer import AuthSerializer
from helper.common.decorators import responsify, jwtAuthGuard
from helper.common.requestSerializer import JWTAuthGuard


@extend_schema(request=RegisterSerializer,
               responses={201: None},
               tags=['User'])
@api_view(['POST'])
@responsify
def register(request: Request):
    serilizer = RegisterSerializer(data=request.data)
    serilizer.is_valid(raise_exception=True)

    auth = AuthSerializer(data=serilizer.validated_data)
    return auth.create()


@extend_schema(request=LoginSerializer,
               responses={200: LoginResponseSerializer},
               tags=['User'])
@api_view(['POST'])
@responsify
def login(request: Request):
    serilizer = LoginSerializer(data=request.data)
    serilizer.is_valid(raise_exception=True)

    auth = AuthSerializer(data=serilizer.data)
    return auth.login()


@extend_schema(parameters=[JWTAuthGuard()],
               request=UpdateSerializer,
               responses={200: UserResponseSerializer},
               tags=['User'])
@api_view(['PATCH'])
@jwtAuthGuard
@responsify
def update(request: Request, user):
    serilizer = UpdateSerializer(data=request.data)
    serilizer.is_valid(raise_exception=True)

    auth = AuthSerializer(data=serilizer.validated_data)
    return auth.update(user['id'])


@extend_schema(request=GenerateNewVerificationTokenSerializer,
               responses={200: None},
               tags=['User'])
@api_view(['GET'])
@responsify
def generateNewVerificationToken(request: Request):
    serilizer = GenerateNewVerificationTokenSerializer(data=request.data)
    serilizer.is_valid(raise_exception=True)

    auth = AuthSerializer(data=serilizer.validated_data)
    return auth.generateNewVerificationToken()


@extend_schema(request=GenerateNewPasswordResetTokenSerializer,
               responses={200: None},
               tags=['User'])
@api_view(['GET'])
@responsify
def generateNewPasswordResetToken(request: Request):
    serilizer = GenerateNewPasswordResetTokenSerializer(data=request.data)
    serilizer.is_valid(raise_exception=True)

    auth = AuthSerializer(data=serilizer.validated_data)
    return auth.genreateNewPasswordResetToken()


@extend_schema(request=ResetPasswordSerializer,
               responses={200: None},
               tags=['User'])
@api_view(['POST'])
@responsify
def resetPassword(request: Request):
    serilizer = ResetPasswordSerializer(data=request.data)
    serilizer.is_valid(raise_exception=True)

    auth = AuthSerializer(data=serilizer.validated_data)
    return auth.resetPassword()


@extend_schema(parameters=[VerifyAccountSerializer],
               responses={200: None},
               tags=['User'])
@api_view(['GET'])
@responsify
def verifyAccount(request: Request):
    serilizer = VerifyAccountSerializer(data=request.data)
    serilizer.is_valid(raise_exception=True)

    auth = AuthSerializer(data=serilizer.validated_data)
    return auth.verifyAccount()