from django.db import models


# Create your models here.
class imb(models.Model):
  dropboxid = models.IntegerField(default=1)
  imb = models.CharField(max_length=66)
  code39 = models.CharField(max_length=44)
  date = models.CharField(max_length=255)
  streetaddress = models.CharField(max_length=255)
  city = models.CharField(max_length=255)
  zipcode = models.CharField(max_length=255)
  status = models.CharField(max_length=255)

