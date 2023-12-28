from django.contrib import admin
from .models import CandidateApplication, JobPost, JobCategory, Company


admin.site.register(JobPost)
admin.site.register(JobCategory)
admin.site.register(CandidateApplication)
admin.site.register(Company)