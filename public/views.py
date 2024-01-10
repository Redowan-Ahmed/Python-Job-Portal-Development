from django.core.paginator import Paginator
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import SupportContact, BlogPost, Category, Comment
from django.contrib import messages
from .forms import SupportContactForm
from django.contrib.auth.decorators import login_required
from accounts.models import User, CandidateProfile
from hr.models import JobCategory, JobPost, Company
from datetime import date
from django.shortcuts import get_object_or_404
from django.db.models import Q
from candidates.models import FavoriteJob


currentDate = date.today()

def index(request):
    categories = JobCategory.objects.filter(featured = True)[:8]
    jobs = JobPost.objects.select_related('user','job_category','company').filter(last_date_of_apply__gte = currentDate)[:6]
    companies = Company.objects.select_related('user').all()[:4]
    posts = BlogPost.objects.select_related('category','author').filter(status='Published').order_by('-created_at')[:3]
    context = {
        'categories': categories,
        'today': currentDate,
        'jobs': jobs,
        'companies': companies,
        'posts': posts
    }
    return render(request, 'index.html', context= context)



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
        jobs = JobPost.objects.filter(job_category = category).order_by("-created_at")
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
            if request.user.is_authenticated:
                loved_jobs = request.user.loved_jobs.all()
            else:
                loved_jobs = None
            try:
                page_obj = paginator.get_page(page_number)
                context = {
                    'jobs': page_obj.object_list,
                    "page_obj": page_obj,
                    'pages': page_obj.number,
                    'keyword': keyword,
                    'location': location,
                    'query': True,
                    'loved_jobs': loved_jobs
                }
                return render(request, 'job-grid.html', context= context)
            except Exception as e:
                print(e)
                raise Http404('NO page is available')
        except Exception as e:
            print(e)
            return render(request, 'job-grid.html')
    else:
        jobs = JobPost.objects.all().order_by('-last_date_of_apply','-created_at')
        paginator = Paginator(jobs, 8)
        page_number = request.GET.get("page")
        if request.user.is_authenticated:
            loved_jobs = request.user.loved_jobs.all()
        else:
            loved_jobs = None

        try:
            page_obj = paginator.get_page(page_number)
            context = {
                'jobs': page_obj.object_list,
                "page_obj": page_obj,
                'today': currentDate,
                'loved_jobs': loved_jobs
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
            'keywords':job_keyword,
            'today': currentDate,
        }
        return render(request, 'job-details.html', context)
    except Exception as e:
        print(e)
        raise Http404("Page not found")


def Blogs(request):
    try:
        blogs = BlogPost.objects.select_related('author','category').filter(status='Published').order_by('-created_at')
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
                if not 'sex' in str(comment).lower():
                    Comment.objects.create(comment = comment, user = commenter, post = blog)
                return redirect('blog', slug)
            else:
                return redirect('blog', slug)
        else:
            try:
                categories = Category.objects.all()
                related_posts = BlogPost.objects.select_related('author','category').filter(Q(category = blog.category) | Q(tags__icontains = blog.tags)).exclude(slug=slug)[:4]
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

@login_required
def ApplyJob(request, pk):
    job = get_object_or_404(JobPost, pk=pk)
    print('Got THe object=', job)

    return redirect('job', pk)

@login_required
def JobFavorite(request, pk):
    if request.POST:

        candidate = CandidateProfile.objects.filter(user = request.user)
        if candidate.exists():
            created, loved = FavoriteJob.objects.get_or_create(user= request.user, job_id= pk)
            #print('created', created , ' ', 'loved', loved)
            if not loved:
                created.delete()
        return redirect('jobs')
    else:
        return redirect('jobs')