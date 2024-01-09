from django.shortcuts import redirect, render
from allauth.account.views import LoginView, SignupView
from hr.models import JobCategory
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404

# Create your views here.


class CustomLogin(LoginView):
    template_name = 'sign-in.html'

class CustomSignUp(SignupView):
    template_name = 'sign-up.html'
def SignUp(request):
    return render(request, 'sign-up.html')


def SignIn(request):
    if request.user.is_authenticated:
        return redirect('account')
    else:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            check_user_exist = User.objects.filter(email = email).exists()
            if check_user_exist:
                user = authenticate(request= request, email = email, password = password)
                if user:
                    login(request = request, user= user)
                    messages.info(request, "You are now logged in")
                    return redirect('account')
                else:
                    messages.error(request, "Invalid Email or Password")
            else:
                messages.error(request,'Account does not exist! Please sign up first.')
        return render(request, 'sign-in.html')

def SignOut(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, message="you're logged out")
        return redirect('signIn')
    else:
        messages.warning(request, message="Please login")
        return redirect('signIn')


@login_required
def Account(request):
    #print(request.user.hr_profile)
    return render(request, 'account.html')


@login_required(login_url='signIn')
def PostJob(request):
    if request.user.is_hr:
        categories = JobCategory.objects.all()
        if request.method == 'POST':
            category = request.POST.get('category')
            description = request.POST.get('description')
            requirements = request.POST.get('requirements')
            keywords = request.POST.get('keywords')
            salary = request.POST.get('salary')
            job_type = request.POST.get('job_type')
            address = request.POST.get('address')
            salary = request.POST.get('salary')
            salary = request.POST.get('salary')
            salary = request.POST.get('salary')
            thumbnail = request.FILES.get('thumbnail')
            try:
                category_obj = get_object_or_404(JobCategory, id = category)
                print(category_obj)
            except Exception as e:
                print("Error occured while posting job",e)
        context = {
            'categories': categories
        }
        return render(request,'account-post-job.html', context= context)
    return redirect('account')