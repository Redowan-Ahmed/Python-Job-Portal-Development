from django.contrib import admin
from .models import CandidateApplication, JobPost


admin.site.register(JobPost)
admin.site.register(CandidateApplication)