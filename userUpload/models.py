from django.db import models
from uauth.models import User
from recognition.models import Recognition


class UserUpload(models.Model):
    id = models.AutoField(primary_key=True,
                          unique=True,
                          null=False,
                          auto_created=True)
    uid = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    recid = models.ForeignKey(Recognition,
                              on_delete=models.CASCADE,
                              null=False)
    isDeleted = models.BooleanField(default=False, null=False)
