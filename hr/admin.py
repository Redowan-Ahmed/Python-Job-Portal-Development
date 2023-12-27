from django.contrib import admin
from .models import CandidateApplication, JobPost, JobCategory


admin.site.register(JobPost)
admin.site.register(JobCategory)
admin.site.register(CandidateApplication)