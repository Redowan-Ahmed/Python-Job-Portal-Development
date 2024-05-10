from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from public.views import index, AboutUs, Contact, Jobs, JobDetails, CategorizedJobs, BlogDetails, Blogs, ApplyJob, JobFavorite, test
from accounts.views import CustomLogin, CustomSignUp, SignOut

urlpatterns = [
    path('', index , name='home'),
    path(route='admin/', view=admin.site.urls),
    path(route='dashboard/', view= include(arg='accounts.urls')), # secure route to dashboard
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
    #Test
    path('test/', test, name='test'),

    path('blogs/<slug:slug>/', BlogDetails, name='blog'),
    path(route='loved_job/<str:pk>/', view=JobFavorite, name='loved_job'),

    # Debug
    path("__debug__/", include("debug_toolbar.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)