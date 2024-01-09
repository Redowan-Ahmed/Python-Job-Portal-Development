from django.urls import include, path
from .views import PostJob, Account, ViewJobPosts

urlpatterns = [
    path('', Account , name='account'),
    path('post-job/', PostJob , name='post-job'),
    path('jobs/', ViewJobPosts , name='posted-jobs'),
]