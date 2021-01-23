from django.db import models

# Create your models here.
class Tags(models.Model):
    key = models.CharField(max_length=50, blank=False, null=False, default='')
    value = models.CharField(max_length=50, blank=False, null=True, default='')
