from django.db import models
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, blank=True, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, db_index=True)

    class Meta:
        abstract = True
