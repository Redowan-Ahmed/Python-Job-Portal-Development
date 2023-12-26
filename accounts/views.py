from django.shortcuts import render
from allauth.account.views import LoginView, SignupView
# Create your views here.


class CustomLogin(LoginView):
    template_name = 'sign-in.html'

class CustomSignUp(SignupView):
    template_name = 'sign-up.html'