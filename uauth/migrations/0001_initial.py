# Generated by Django 4.0.3 on 2022-03-09 16:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('isDeleted', models.BooleanField(auto_created=True, default=False)),
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(2), django.core.validators.RegexValidator('^[a-zA-Z ]')])),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=32, validators=[django.core.validators.MinLengthValidator(6)])),
                ('passwordResetToken', models.CharField(max_length=32, null=True)),
                ('verifyToken', models.CharField(max_length=32, null=True)),
                ('verifyTokenExpireAt', models.FloatField()),
                ('passwordResetTokenExpireAt', models.FloatField(null=True)),
                ('isActive', models.BooleanField()),
                ('isVerified', models.BooleanField()),
                ('cAt', models.FloatField()),
                ('uAt', models.FloatField()),
            ],
        ),
    ]
