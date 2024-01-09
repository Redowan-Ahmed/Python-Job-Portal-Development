from django.contrib import admin
from .models import IsSortList, MyApplyJobList, FavoriteJob


admin.site.register(MyApplyJobList)
admin.site.register(FavoriteJob)