from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from .managers import CustomUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from base.model import BaseModel
import uuid
from hr.models import Company


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name='Email Address' ,unique= True)
    phoneNumberRegex = RegexValidator(
        regex=r"^\+?1?\d{8,15}$", message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phoneNumberRegex], max_length=16
    )
    profile_picture = models.ImageField(upload_to='profile_pictures',blank=True)
    email_verified = models.BooleanField(default=False, blank=True)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    otp = models.CharField(max_length=10, null=True, blank=True)
    is_hr = models.BooleanField(default=False)
    is_candidate = models.BooleanField(default=True)
    username = None

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return self.email


class CandidateProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    passing_date = models.DateField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/%Y', blank=True)
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    postal_code = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.email



class HrProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hr_profile')
    biography = models.TextField(blank=True, max_length=1000)
    position = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    postal_code = models.CharField(max_length=200, blank=True)
    company = models.ForeignKey(Company, on_delete = models.CASCADE, blank= True, default='46821c24-d5d6-4d40-b426-3aebcfcedc85' )

    def __str__(self):
        return self.user.email



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        if created:
            if instance.is_hr:
                HrProfile.objects.create(user=instance)
            else:
                candidate = CandidateProfile.objects.create(user=instance)
                candidate.save()
    except Exception as e:
        print(e)
