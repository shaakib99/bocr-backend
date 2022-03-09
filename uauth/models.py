from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator


class User(models.Model):
    id = models.AutoField(primary_key=True,
                          auto_created=True,
                          null=False,
                          unique=True)
    name = models.CharField(
        max_length=30,
        validators=[MinLengthValidator(2),
                    RegexValidator("^[a-zA-Z ]")])
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(validators=[MinLengthValidator(6)],
                                max_length=32,
                                null=False)
    passwordResetToken = models.CharField(max_length=32, null=True)
    verifyToken = models.CharField(max_length=32, null=True)
    verifyTokenExpireAt = models.FloatField(null=False)
    passwordResetTokenExpireAt = models.FloatField(null=True)
    isActive = models.BooleanField(null=False)
    isVerified = models.BooleanField(null=False)
    cAt = models.FloatField(null=False)
    uAt = models.FloatField(null=False)
    isDeleted = models.BooleanField(default=False, auto_created=True)
