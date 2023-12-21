from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.core.validators import RegexValidator
from .managers import CustomUserManager



class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name='Email Address' ,unique= True)
    phoneNumberRegex = RegexValidator(
        regex=r"^\+?1?\d{8,15}$", message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phoneNumberRegex], max_length=16, default=8801632398271
    )
    email_verified = models.BooleanField(default=False, blank=True)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    otp = models.CharField(max_length=10, null=True, blank=True)
    is_hr = models.BooleanField(default=False)
    is_candidate = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return "{}".format(self.email)