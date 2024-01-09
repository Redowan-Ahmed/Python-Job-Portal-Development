from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from public.views import index, AboutUs, Contact, Jobs, JobDetails, CategorizedJobs, BlogDetails, Blogs, ApplyJob, JobFavorite
from accounts.views import CustomLogin, CustomSignUp, SignOut

urlpatterns = [
    path('', index , name='home'),
    path('admin/', admin.site.urls),
    path('dashboard/', include('accounts.urls')),
    path('all/accounts/', include('allauth.urls')),
    path('sign-in/', CustomLogin.as_view(), name='signIn'),
    path('sign-up/', CustomSignUp.as_view() , name='signUp'),
    path('logout/', SignOut , name='logout'),
    path('about-us/', AboutUs , name='about'),
    path('contact-us/', Contact , name='contact'),
    path('jobs/', Jobs , name='jobs'),
    path('job-detail/<str:pk>/', JobDetails, name='job'),
    path('jobs/category/<str:category>/', CategorizedJobs, name='categorized-jobs'),
    path('job/apply/<str:pk>/', ApplyJob, name='job-apply'),
    path('blogs/', Blogs, name='blogs'),
    path('blogs/<slug:slug>/', BlogDetails, name='blog'),
    path('loved_job/<str:pk>/', JobFavorite, name='loved_job'),

    # Debug
    path("__debug__/", include("debug_toolbar.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)