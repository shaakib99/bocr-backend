from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework import serializers
from django.core.validators import MinLengthValidator, RegexValidator
from helper.util import randomStringGenerator, hashPassword, jwtEncode
from uauth.serializers.responseSerializers import LoginResponseSerializer, UserResponseSerializer
from uauth.models import User
from datetime import datetime, timedelta
from rest_framework.exceptions import NotFound, NotAcceptable


class AuthSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(
        max_length=30,
        validators=[
            MinLengthValidator(2),
            RegexValidator("^([a-zA-Z]+\s)*[a-zA-Z]+$")
        ],
        required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(max_length=32, required=False)
    passwordResetToken = serializers.CharField(max_length=32, required=False)
    verifyToken = serializers.CharField(max_length=32, required=False)
    verifyTokenExpireAt = serializers.FloatField(required=False)
    passwordResetTokenExpireAt = serializers.FloatField(required=False)
    isActive = serializers.BooleanField(required=False)
    isVerified = serializers.BooleanField(required=False)
    cAt = serializers.FloatField(required=False)
    uAt = serializers.FloatField(required=False)
    isDeleted = serializers.BooleanField(required=False)

    def create(self):
        self.name = self.initial_data['name']
        self.email = self.initial_data['email']
        self.password = hashPassword(self.initial_data['password'])
        self.passwordResetToken = randomStringGenerator(20)
        self.verifyToken = randomStringGenerator(20)
        self.verifyTokenExpireAt = (datetime.now() +
                                    timedelta(minutes=30)).timestamp()
        self.isActive = False
        self.isVerified = False
        self.cAt = datetime.now().timestamp()
        self.uAt = self.cAt
        self.isDeleted = False
        user = User.objects.create(**self.to_representation(self))
        user.save()
        return {'status_code': HTTP_201_CREATED}

    def login(self):
        email = self.initial_data['email']
        password = hashPassword(self.initial_data['password'])

        user: User = User.objects.filter(email=email,
                                         password=password).first()

        if not user:
            raise NotFound(f'{email} does not exist')

        user.isActive = True
        user.save()

        result = {'email': email, 'id': user.id}

        user.token = jwtEncode(result)
        serializedResult = LoginResponseSerializer(user)

        return serializedResult.data

    def update(self, id: str):
        if 'password' in self.initial_data:
            self.password = hashPassword(self.initial_data['password'])

        update = {**self.initial_data, **self.to_representation(self)}

        User.objects.filter(id=id).update(**update,
                                          uAt=datetime.now().timestamp())

        user = User.objects.filter(id=id).first()

        return UserResponseSerializer(user).data

    def generateNewVerificationToken(self):
        self.verifyToken = self.initial_data['verifyToken']
        user: User = User.objects.filter(verifyToken=self.verifyToken).first()

        if not user:
            raise NotFound('Verification token not found')

        user.verifyToken = randomStringGenerator(length=20)
        user.verifyTokenExpireAt = (datetime.now() +
                                    timedelta(minutes=30)).timestamp()
        user.save()
        return UserResponseSerializer(user).data

    def genreateNewPasswordResetToken(self):
        self.email = self.initial_data['email']
        user: User = User.objects.filter(email=self.email).first()

        if not user:
            raise NotFound('User not found')

        user.passwordResetToken = randomStringGenerator(length=20)
        user.passwordResetTokenExpireAt = (datetime.now() +
                                           timedelta(minutes=30)).timestamp()
        user.save()
        return {}

    def resetPassword(self):
        self.passwordResetToken = self.initial_data['passwordResetToken']
        user: User = User.objects.filter(
            passwordResetToken=self.passwordResetToken).first()

        if not user:
            raise NotFound('Token not found')

        if datetime.now().timestamp > user.passwordResetTokenExpireAt:
            raise NotAcceptable('Token expired')

        if user.password == hashPassword(self.initial_data['password']):
            raise NotAcceptable("Old and new password can't be the same")

        newPassword = hashPassword(self.initial_data['password'])

        if newPassword == user.password:
            raise NotAcceptable(
                'New password and old password can not be the same.')

        user.password = newPassword

        user.passwordResetToken = None
        user.save()
        return {}

    def verifyAccount(self):
        self.verifyToken = self.initial_data['verifyToken']
        user: User = User.objects.filter(verifyToken=self.verifyToken).first()

        if not user:
            raise NotFound('Token not found')

        if datetime.now().timestamp() > user.verifyTokenExpireAt:
            raise NotAcceptable('Token expired')

        user.isActive = True
        user.isVerified = True
        user.save()
        return {}
