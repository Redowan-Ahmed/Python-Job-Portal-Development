from django.urls import path
from .views import PostJob, Account, ViewJobPosts, CompanyPost, Companies, savedJobs, AccountChat, EditJobPost, AccountChats, CompanyEdit

urlpatterns = [
    path(route='', view=Account , name='account'),
    path(route='post-job/', view=PostJob , name='post-job'),
    path(route='edit/<str:pk>/', view=EditJobPost , name='edit-job'),
    path(route='company/add-company/', view=CompanyPost , name='add-company'),
    path(route='company/edit-company/<str:pk>/', view=CompanyEdit , name='edit-company'),
    path(route='company/', view=Companies , name='dash-companies'),
    path(route='jobs/', view=ViewJobPosts , name='posted-jobs'),
    path(route='saved-jobs/', view=savedJobs , name='loved-jobs'),
    path(route='messages/', view=AccountChats, name="messages"),
    path(route='messages/<str:pk>/', view=AccountChat, name="message"),
]