from django.db import models


# Create your models here.
class EnvelopeScan(models.Model):
    id = models.AutoField(primary_key=True)
    dropboxid = models.IntegerField(default=1)  # Required (default doesn't make it optional)
    imb = models.CharField(max_length=66, blank=True, null=True)  # Optional
    code39 = models.CharField(max_length=44, unique=True)  # Required
    date = models.CharField(max_length=255)  # Required
    streetaddress = models.CharField(max_length=255, blank=True, null=True)  # Optional
    city = models.CharField(max_length=255, blank=True, null=True)  # Optional
    zipcode = models.CharField(max_length=255, blank=True, null=True)  # Optional
    status = models.CharField(max_length=255, blank=True, null=True)  # Optional

    def __str__(self):
        return f"EnvelopeScan {self.code39}"

