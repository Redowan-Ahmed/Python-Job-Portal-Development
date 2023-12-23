from django.db import models
from base.model import BaseModel
from django.core.validators import RegexValidator



class SupportContact(BaseModel):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(verbose_name='Email Address')
    phoneNumberRegex = RegexValidator(
        regex=r"^\+?1?\d{8,15}$", message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phoneNumberRegex], max_length=17, default=8801632398271
    )
    subject = models.CharField(max_length=300)
    message = models.TextField(max_length=5000, blank=True)


    def __str__(self):
        return self.full_name