from django.db import models


class Recognition(models.Model):
    id = models.AutoField(primary_key=True,
                          unique=True,
                          auto_created=True,
                          null=False)
    uri = models.CharField(max_length=200, null=False, unique=True)
    result = models.JSONField()
    cAt = models.FloatField()
    uAt = models.FloatField()
