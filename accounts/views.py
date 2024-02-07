from datetime import date
from email.policy import default
from django.shortcuts import redirect, render
from allauth.account.views import LoginView, SignupView
from hr.models import JobCategory, Company, JobPost
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404, resolve_url
from candidates.models import FavoriteJob
from django.db import transaction
from django.core.paginator import Paginator
from message.models import Message, RoomMessage
from django.db.models import Avg, Max, Min, Count, Q

from hr.forms import CompanyForm, CompanyFormEdit
from message.models import MessageRoom

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
                    messages.info(request=request, message="You are now logged in")
                    return redirect('account')
                else:
                    messages.error(request, "Invalid Email or Password")
            else:
                messages.error(request,'Account does not exist! Please sign up first.')
        return render(request, 'sign-in.html')

def SignOut(request):
    if request.user.is_authenticated:
        logout(request=request)
        messages.info(request=request, message="you're logged out")
        return redirect('signIn')
    else:
        messages.warning(request=request, message="Please login")
        return redirect(to='signIn')


@login_required
def Account(request):
    #print(request.user.hr_profile)
    if request.user.is_hr:
        jobs = request.user.job_posts
        companies = request.user.companies.all().count()
        # def textData(data = 'Test'):
        #     print(data)
        #     return f'{data} Working'
        context = {
            'total_jobs': jobs.all().count(),
            'total_active_jobs': jobs.filter(last_date_of_apply__gte = currentDate).count(),
            'total_companies': companies,
            # 'test': textData
        }
        return render(request=request, template_name='account.html', context= context)
    return render(request=request, template_name='account.html')


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
                    messages.success(request=request, message="You're successfully posted a new job")
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
        return render(request=request,template_name='account-post-job.html', context= context)
    return redirect(to='account')

@login_required
def ViewJobPosts(request):
    jobs = JobPost.objects.filter(user= request.user).order_by('-created_at')
    page_number:int = request.GET.get('page')
    try:
        pagination = Paginator(object_list=jobs, per_page=6)
        page_obj = pagination.get_page(number=page_number)
    except Exception as e:
        print(e)
    context = {
        'jobs': page_obj.object_list,
        'today': currentDate,
        'page_obj': page_obj
    }
    return render(request=request, template_name='account-jobs.html', context= context)


@login_required
@transaction.atomic()
def EditJobPost(request, pk):
    try:
        job = get_object_or_404(JobPost, pk=pk)
        if request.user == job.user:
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
                    if title and category and description and requirements and keywords and salary and job_type and address and looking_position and experience and country:
                        job.title = title
                        job.job_category = category_obj
                        if thumbnail:
                            job.thumbnail = thumbnail
                        job.description = description
                        job.requirements = requirements
                        job.minimum_experience = experience
                        job.looking_position = looking_position
                        job.address = address
                        job.job_type = job_type
                        job.country = country
                        job.salary = salary
                        job.keywords = keywords
                        if last_date_of_apply:
                            job.last_date_of_apply = last_date_of_apply
                        job.company = company_obj
                        job.save()
                        messages.success(request=request, message=f"You're successfully updated {job.title} ")
                        return redirect('job-edit', job.pk)
                    else:
                        print(title, category , description , requirements , keywords , salary , job_type , address , looking_position , experience , country , thumbnail , last_date_of_apply)
                        messages.error(request=request, message='Something is wrong, Please fill the form properly')
                        raise ValueError('Got unexpected condition')
                except Exception as e:
                    print("Error occurred while posting job",e)
            context = {
                'job': job,
                'categories': categories,
                'companies': companies,
                'today': currentDate
            }
            return render(request=request, template_name='account-job-edit.html', context= context)
        else:
            messages.warning(request=request,message="This isn't your job! You can only edit or delete your own posts.")
            return redirect(to='posted-jobs')
    except Exception as e:
        print(e)

@login_required
def Companies(request):
    user = request.user
    companies = Company.objects.prefetch_related('jobs').filter(user = user).order_by('-created_at')
    context = {
        "companies": companies,
        'user': user
    }
    return render(request=request, template_name='account-companies.html', context=context)

@login_required
def CompanyPost(request):
    user = request.user
    form = CompanyForm()
    if request.method == 'POST':
        form = CompanyForm(data=request.POST or None, files=request.FILES or None)
        if form.is_valid():
            name = form.cleaned_data.get('company_name')
            logo = form.files.get('company_logo')
            location = form.cleaned_data.get('location')
            website = form.cleaned_data.get('website')
            email = form.cleaned_data.get('email')
            employ = form.cleaned_data.get('employ_volume_average')
            phone_number = form.cleaned_data.get('phone_number')
            company = Company.objects.create(user = user, website = website, company_name = name, email = email, phone_number = phone_number,employ_volume_average = employ,  company_logo = logo, location= location)
            messages.success(request=request, message=f'{company.company_name} is successfully created')
            return redirect(to='dash-companies')
        else:
            messages.error(request=request, message='Something went wrong')
    context = {
        'form': form
    }
    return render(request=request, template_name='account-company.html', context=context)

@login_required
def CompanyEdit(request, pk):
    user = request.user
    try:
        companyObj = get_object_or_404(klass=Company, pk=pk)
        if companyObj.user == user:
            form = CompanyFormEdit(initial=companyObj.__dict__, instance=companyObj)
            if request.method == 'POST':
                form = CompanyFormEdit(data=request.POST or None, files=request.FILES or None, initial=companyObj.__dict__, instance=companyObj)
                if form.is_valid():
                    name = form.cleaned_data.get('company_name')
                    logo = form.files.get('company_logo')
                    location = form.cleaned_data.get('location')
                    website = form.cleaned_data.get('website')
                    email = form.cleaned_data.get('email')
                    employ = form.cleaned_data.get('employ_volume_average')
                    phone_number = form.cleaned_data.get('phone_number')
                    status = form.cleaned_data.get('status')
                    with transaction.atomic():
                        companyObj.company_name = name
                        if logo:
                            companyObj.company_logo = logo
                        companyObj.location = location
                        companyObj.website = website
                        companyObj.email = email
                        companyObj.employ_volume_average = employ
                        companyObj.phone_number = phone_number
                        companyObj.status = status
                        companyObj.save()
                    messages.success(request=request, message=f'{companyObj.company_name} is successfully save')
                    return redirect(to='dash-companies')
                else:
                    messages.error(request=request, message='Something went wrong')
            context = {
                'form': form,
                'edit':True,
                'currentThumbnail': companyObj.company_logo
            }
            return render(request=request, template_name='account-company.html', context=context)
        else:
            messages.warning(request=request, message="You don't have any access to this company")
            return redirect(to='dash-companies')
    except Exception as e:
        raise Exception(f'Something went wrong {e}')

@login_required
def savedJobs(request):
    jobs = request.user.loved_jobs.all().order_by('-created_at')
    print(jobs)
    return render(request, 'account-company.html')


@login_required
def AccountChat(request, pk):
    user = request.user
    userChatRooms = user.chat_rooms.all()
    room_obj = MessageRoom.objects.get(pk = pk)
    room_obj_users = room_obj.users.all()
    if user in room_obj_users:
        receiverUser = room_obj_users.exclude(pk__contains=[user.pk]).first()
        messages_obj = RoomMessage.objects.filter(room = room_obj).order_by('-created_at')
        # message_list_obj = RoomMessage.objects.filter(Q())
        # print(message_list_obj)
        page:int = request.GET.get('page')
        try:
            if not page :
                page = 1
            pagination = Paginator(object_list=messages_obj, per_page=10)
            page_obj = pagination.get_page(number=page)
            reversedList = list(reversed(page_obj.object_list))
            context = {
                "room_name": pk,
                'user':user,
                'messages_obj':reversedList,
                'page_obj': page_obj,
                'receiverUser' : receiverUser,
                'home': False,
                'chat_rooms': userChatRooms,
                'room': room_obj
                }
            return render(request=request, template_name='account-Chat.html', context=context)
        except Exception as e:
            print(e)
    else:
        messages.warning(request= request, message='You are not allowed to view this chat!')
        return redirect(to='account')
    # return render(request=request, template_name='account-Chat.html', context={"room_name": pk, 'user':user.pk})

@login_required
def AccountChats(request):
    user = request.user
    userChatRooms = user.chat_rooms.all()
    try:
        context = {
            'user':user,
            'chat_rooms': userChatRooms,
            'home': True
            }
        return render(request=request, template_name='account-Chat.html', context=context)
    except Exception as e:
        print(e)