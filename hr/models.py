
from email.policy import default
from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings
from base.model import BaseModel


class JobCategory(BaseModel):
    name = models.CharField(max_length=100, db_index = True)
    icon = models.ImageField(upload_to='category-img')
    featured = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class JobPost(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_posts', db_index=True)
    job_category = models.ForeignKey(JobCategory, models.CASCADE, related_name='jobs', db_index=True)
    thumbnail = models.ImageField(upload_to='job-thumbnail', default=None)
    title = models.CharField(max_length=300, db_index=True)
    description = models.TextField(max_length=5000, default=None)
    requirements = models.TextField(max_length=5000, default=None)
    company_name = models.CharField(max_length=150, default=None, db_index=True)
    minimum_experience = models.PositiveIntegerField(default=0, blank=True)
    job_type = models.CharField(max_length=100, default='Full Time', blank=True)
    looking_position = models.CharField(max_length=100, default=None)
    address = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=100, blank=True, db_index=True)
    city = models.CharField(max_length=50, blank=True, db_index=True)
    state = models.CharField(max_length=50, blank=True, db_index=True)
    zipcode = models.CharField(max_length=20, blank=True)
    phone_number_validator = RegexValidator(regex=r"^\+?1?\d{8,15}$",
                                            message="Phone number must be entered in the format: '+999999999'. Up to "
                                                    "15 digits allowed.")
    phone_number = models.CharField(max_length=15, validators=[phone_number_validator], blank=True)
    language = models.CharField(max_length=100, blank=True, default='English')
    salary = models.DecimalField(max_digits=65, decimal_places=2, blank=True, default=None)
    email = models.EmailField(blank=True, default= None)
    keywords = models.CharField(max_length=200, blank=True, db_index=True)
    last_date_of_apply = models.DateField(default=None)

    def __str__(self):
        return self.title


class CandidateApplication(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    job = models.OneToOneField(JobPost, on_delete=models.CASCADE, related_name="candidates_applications")

    def __str__(self):
        return self.job.title
