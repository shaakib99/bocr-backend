from rest_framework import serializers
from uauth.models import User
from django.core.validators import MinLengthValidator, RegexValidator


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.RegexField(
        '^(?=.*\d)(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z]).{6,32}$')

    class Meta:
        model = User
        fields = ['name', 'email', 'password']


class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password']


class UpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=30,
        validators=[MinLengthValidator(2),
                    RegexValidator("^[a-zA-Z ]")],
        required=False)
    email = serializers.EmailField(required=False)
    password = serializers.RegexField(
        '^(?=.*\d)(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z]).{6,32}$',
        required=False)
    isActive = serializers.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'isActive']


class GenerateNewVerificationTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['verifyToken']


class GenerateNewPasswordResetTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email']


class ResetPasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['password', 'passwordResetToken']


class VerifyAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['verifyToken']
