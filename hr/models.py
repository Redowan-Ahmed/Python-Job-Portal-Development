from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings
from accounts.models import CandidateProfile
from base.model import BaseModel


class JobPost(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_posts', db_index=True)
    title = models.CharField(max_length=300)
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)
    phone_number_validator = RegexValidator(regex=r"^\+?1?\d{8,15}$",
                                            message="Phone number must be entered in the format: '+999999999'. Up to "
                                                    "15 digits allowed.")
    phone_number = models.CharField(max_length=15, validators=[phone_number_validator])

    def __str__(self):
        return self.title


class CandidateApplication(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    job = models.OneToOneField(JobPost, on_delete=models.CASCADE, related_name="candidates_applications")
    candidate_profile = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='candidate_profile')

    def __str__(self):
        return self.job.title
