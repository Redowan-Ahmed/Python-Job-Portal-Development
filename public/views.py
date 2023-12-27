from unicodedata import category
from django.shortcuts import redirect, render
from .models import SupportContact
from django.contrib import messages
from .forms import SupportContactForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login, logout
from accounts.models import User
from hr.models import JobCategory
# from django.shortcuts import get_object_or_404


def index(request):
    category = JobCategory.objects.filter(featured = True)[:8]
    context = {
        'categories': category
    }
    return render(request, 'index.html', context= context)


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


def AboutUs(request):
    return render(request, 'about.html')


def Contact(request):
    if request.method == 'POST':
        form = SupportContactForm(request.POST)
        context = {
            'errors': form.errors,
            'form': form
        }
        if form.is_valid():
            name = form.cleaned_data.get('full_name')
            email = form.cleaned_data.get('email')
            number = form.cleaned_data.get('phone_number')
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')
            SupportContact.objects.create(
                full_name=name, email=email, phone_number=number, subject=subject, message=message)
            messages.success(
                request, "Thank your for your Submission, We'll rechout with you soon")
            return render(request, 'contact.html', context=context)
        return render(request, 'contact.html', context=context)
    else:
        return render(request, 'contact.html')


def Jobs(request):
    return render(request, 'job-grid.html')


def JobDetails(request, pk):
    context = {
        'pk':pk
    }
    print(pk)
    return render(request, 'job-details.html', context)