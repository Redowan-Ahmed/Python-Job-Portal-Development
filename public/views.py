from unicodedata import category
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import redirect, render
from .models import SupportContact, BlogPost, Category, Comment
from django.contrib import messages
from .forms import SupportContactForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login, logout
from accounts.models import User
from hr.models import JobCategory, JobPost, Company
from datetime import date
from django.shortcuts import get_object_or_404
from django.db.models import Q


currentDate = date.today()

def index(request):
    categories = JobCategory.objects.filter(featured = True)[:8]
    jobs = JobPost.objects.select_related('user','job_category','company').filter(last_date_of_apply__gte = currentDate)[:6]
    companies = Company.objects.select_related('user').all()[:4]
    posts = BlogPost.objects.select_related('category').filter(status='Published').order_by('-created_at')[:3]
    context = {
        'categories': categories,
        'today': currentDate,
        'jobs': jobs,
        'companies': companies,
        'posts': posts
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
    blogs = BlogPost.objects.filter(status="Published").order_by('-created_at')[:3]
    context= {
        'blogs': blogs
    }
    return render(request, 'about.html', context)


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

def CategorizedJobs(request, category):
    try:
        category = JobCategory.objects.get(name = category)
        jobs = JobPost.objects.filter(job_category = category, last_date_of_apply__gte = currentDate).order_by("-created_at")
        paginator = Paginator(jobs, 8)
        page_number = request.GET.get("page")
        try:
            page_obj = paginator.get_page(page_number)
            context = {
                'category': category,
                'jobs': page_obj.object_list,
                "page_obj": page_obj
            }
            return render(request, 'categorized-jobs.html', context)
        except Exception as e:
            print(e)
            raise Http404('No more page Exit')
    except Exception as e:
        print("Error in categorized jobs", str(e))
        raise Http404('page is not found')


def Jobs(request):
    if request.GET.get('keyword') and request.GET.get('location'):
        try:
            keyword = request.GET.get('keyword')
            location = request.GET.get('location')
            jobs = JobPost.objects.filter( Q(address__icontains = location) | Q(country__icontains = location) | Q(state__icontains = location) | Q(city__icontains = location) | Q(company__location__icontains = location) and Q(title__icontains = keyword) | Q(description__icontains = keyword)| Q(keywords__icontains = keyword) | Q(looking_position__icontains = keyword)).order_by('-created_at')
            paginator = Paginator(jobs, 8)
            page_number = request.GET.get('page')
            try:
                page_obj = paginator.get_page(page_number)
                context = {
                    'jobs': page_obj.object_list,
                    "page_obj": page_obj,
                    'pages': page_obj.number,
                    'keyword': keyword,
                    'location': location,
                    'query': True,
                }
                return render(request, 'job-grid.html', context= context)
            except Exception as e:
                print(e)
                raise Http404('NO page is available')
        except Exception as e:
            print(e)
            return render(request, 'job-grid.html')
    else:
        jobs = JobPost.objects.all().order_by('-created_at')
        paginator = Paginator(jobs, 8)
        page_number = request.GET.get("page")
        try:
            page_obj = paginator.get_page(page_number)
            context = {
                'jobs': page_obj.object_list,
                "page_obj": page_obj
            }
            return render(request, 'job-grid.html', context=context)
        except Exception as e:
            print(e)
            raise Http404('No more page Exit')



def JobDetails(request, pk):
    try:
        job = get_object_or_404(JobPost, pk=pk)
        related_jobs = JobPost.objects.filter(job_category__name = job.job_category.name, last_date_of_apply__gte = currentDate).exclude(pk=job.pk).order_by('-created_at')[:5]
        job_keyword = job.keywords.split(',')
        context = {
            'job': job,
            'related_jobs': related_jobs,
            'keywords':job_keyword
        }
        return render(request, 'job-details.html', context)
    except Exception as e:
        print(e)
        raise Http404("Page not found")


def Blogs(request):
    try:
        blogs = BlogPost.objects.filter(status='Published').order_by('-created_at')
        paginator = Paginator(blogs, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            'blogs': page_obj.object_list,
            'page_obj': page_obj
        }
        return render(request, 'blog.html', context=context)
    except Exception as e:
        print(e)
        raise Http404('Something Went wrong')


def BlogDetails(request, slug):
    try:
        blog = get_object_or_404(BlogPost, slug=slug)
        if request.method == 'POST':
            if request.user.is_authenticated:
                comment = request.POST.get('comment')
                commenter = request.user
                Comment.objects.create(comment = comment, user = commenter, post = blog)
                return redirect('blog', slug)
            else:
                return redirect('blog', slug)
        else:
            try:
                categories = Category.objects.all()
                related_posts = BlogPost.objects.filter(Q(category = blog.category) | Q(tags__icontains = blog.tags))[:4]
                tags = blog.tags
                context = {
                    'blog': blog,
                    'categories': categories,
                    'tags': tags.split(','),
                    'related_posts': related_posts
                }
                return render(request, 'blog-details.html', context= context)
            except Exception as e:
                print(e)
                raise Http404("Page not found")
    except Exception as e:
        print(e)
        raise Http404("Something Went Wrong")