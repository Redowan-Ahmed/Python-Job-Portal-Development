from django.shortcuts import render
from allauth.account.views import LoginView
# Create your views here.


class CustomLogin(LoginView):
    template_name = 'sign-in.html'