from django.urls import include, path
from .views import PostJob, Account, ViewJobPosts, CompanyPost, Companies, savedJobs

urlpatterns = [
    path('', Account , name='account'),
    path('post-job/', PostJob , name='post-job'),
    path('company/add-company/', CompanyPost , name='add-company'),
    path('company/', Companies , name='dash-companies'),
    path('jobs/', ViewJobPosts , name='posted-jobs'),
    path('saved-jobs/', savedJobs , name='loved-jobs'),
]