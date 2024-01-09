from django.urls import include, path
from .views import CustomLogin, CustomSignUp, PostJob, Account, SignOut

urlpatterns = [
    path('', Account , name='account'),
    path('post-job/', PostJob , name='post-job'),
]