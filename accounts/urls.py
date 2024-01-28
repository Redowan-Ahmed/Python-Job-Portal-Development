from django.urls import include, path
from .views import PostJob, Account, ViewJobPosts, CompanyPost, Companies, savedJobs, AccountChat, EditJobPost

urlpatterns = [
    path('', Account , name='account'),
    path('post-job/', PostJob , name='post-job'),
    path('edit/<str:pk>/', EditJobPost , name='edit-job'),
    path('company/add-company/', CompanyPost , name='add-company'),
    path('company/', Companies , name='dash-companies'),
    path('jobs/', ViewJobPosts , name='posted-jobs'),
    path('saved-jobs/', savedJobs , name='loved-jobs'),
    path('messages/', AccountChat, name="messages"),
]