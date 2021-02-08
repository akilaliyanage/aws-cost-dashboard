from django.db import models

# Create your models here.
class Tags(models.Model):
    id = models.CharField(primary_key=True,max_length=30)
    key = models.CharField(max_length=50, blank=False, null=False, default='')
    value = models.CharField(max_length=50, blank=False, null=True, default='')
