from django.db import models
from hr.models import JobPost, CandidateApplication
from django.conf import settings
from accounts.models import CandidateProfile
from base.model import BaseModel


class MyApplyJobList(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applied_user', db_index= True)
    job = models.ForeignKey(CandidateApplication,
                            on_delete=models.CASCADE, related_name='applied_job', db_index=True)



class IsSortList(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='is_shorted', db_index=True)
    job = models.OneToOneField(JobPost, on_delete=models.CASCADE, related_name='job', db_index=True)
    candidate_profile = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='candidate_profile_accounts', db_index=True)
    def __str__(self):
        return self.candidate_profile