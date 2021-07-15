from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    personal_pic = models.ImageField(
        upload_to="Users_Personal_Pics", verbose_name="Personal Pic"
    )
    gov_id = models.CharField(max_length=500, verbose_name="GOV ID")
    phone_number = models.CharField(max_length=500, verbose_name="Phone Number")
    address = models.CharField(max_length=500, verbose_name="Address")
    role = models.CharField(max_length=350, verbose_name="User Role")
    device_identifier = models.CharField(
        max_length=500, verbose_name="Device Identifier"
    )

