from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    birthday = models.DateField(null=True, blank=True)  # Changed from age to birthday
    profile_picture = models.ImageField(upload_to='account/avatar/', blank=True, null=True)

    # New fields
    job_role = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    whatsapp = models.CharField(max_length=20, blank=True, null=True)
    telegram = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.username