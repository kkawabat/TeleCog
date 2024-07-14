from django.db import models


# Create your models here.
class Assessment(models.Model):
    call_sid = models.CharField(max_length=34)
    object_naming_result = models.IntegerField(blank=True, null=True)
