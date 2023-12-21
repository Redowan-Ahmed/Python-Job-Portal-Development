from django.db import models
from config import settings
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, blank=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        abstract = True


class MyApplyJobList(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applied_user')
    job = models.ForeignKey(CandidateApplication,
                            on_delete=models.CASCADE, related_name='job')



class IsSortList(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name='is_shorted')
    job = models.OneToOneField(JobPost, on_delete= models.CASCADE)