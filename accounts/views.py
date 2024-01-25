from datetime import date
from django.shortcuts import redirect, render
from allauth.account.views import LoginView, SignupView
from hr.models import JobCategory, Company, JobPost
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404
from candidates.models import FavoriteJob

# Create your views here.

currentDate = date.today()

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
    if request.user.is_hr:
        jobs = request.user.job_posts
        companies = request.user.companies.all().count()
        context = {
            'total_jobs': jobs.all().count(),
            'total_active_jobs': jobs.filter(last_date_of_apply__gte = currentDate).count(),
            'total_companies': companies
        }
        return render(request, 'account.html', context= context)
    return render(request, 'account.html')


@login_required(login_url='signIn')
def PostJob(request):
    if request.user.is_hr:
        companies = Company.objects.filter(user = request.user)
        categories = JobCategory.objects.all()
        if request.method == 'POST':
            title = request.POST.get('title')
            category = request.POST.get('category')
            description = request.POST.get('description')
            requirements = request.POST.get('requirements')
            keywords = request.POST.get('keywords')
            salary = request.POST.get('salary')
            job_type = request.POST.get('job_type')
            address = request.POST.get('address')
            company = request.POST.get('company')
            looking_position = request.POST.get('looking_position')
            experience = request.POST.get('experience')
            country = request.POST.get('country')
            last_date_of_apply = request.POST.get('last_date_of_apply')
            thumbnail = request.FILES.get('thumbnail')
            try:
                category_obj = get_object_or_404(JobCategory, id = category)
                company_obj = get_object_or_404(Company, id = company)

                if title and category and description and requirements and keywords and salary and job_type and address and looking_position and experience and country and thumbnail and last_date_of_apply:
                    post = JobPost.objects.create(user= request.user, job_category =category_obj, company=company_obj, thumbnail= thumbnail, title= title, description= description, requirements=requirements, minimum_experience= experience, job_type= job_type, looking_position= looking_position, address=address, country= country, salary = salary, keywords=keywords, last_date_of_apply= last_date_of_apply)
                    messages.success(request, "You're successfully posted a new job")
                    return redirect('job', post.pk)
                else:
                    print(title, category , description , requirements , keywords , salary , job_type , address , looking_position , experience , country , thumbnail , last_date_of_apply)
                    messages.error(request, 'Something is wrong, Please fill the form properly')
                    raise ValueError('Got unexpected condition')
            except Exception as e:
                print("Error occurred while posting job",e)
        context = {
            'categories': categories,
            'companies': companies
        }
        return render(request,'account-post-job.html', context= context)
    return redirect('account')

@login_required
def ViewJobPosts(request):
    jobs = JobPost.objects.filter(user= request.user).order_by('-created_at')
    context = {
        'jobs': jobs,
        'today': currentDate
    }
    return render(request, 'account-jobs.html', context= context)

@login_required
def Companies(request):

    return render(request, 'account-company.html')

@login_required
def CompanyPost(request):

    return render(request, 'account-company.html')

@login_required
def savedJobs(request):
    jobs = request.user.loved_jobs.all().order_by('-created_at')
    print(jobs)
    return render(request, 'account-company.html')


@login_required
def AccountChat(request):
    return render(request, 'account-Chat.html')