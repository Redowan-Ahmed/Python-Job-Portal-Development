from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')


def SignUp(request):
    return render(request, 'sign-up.html')


def SignIn(request):
    return render(request, 'sign-in.html')

def Account(request):
    return render(request, 'account.html')
