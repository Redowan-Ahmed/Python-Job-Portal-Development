from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from public.views import index, Account, AboutUs, Contact, Jobs, JobDetails, SignOut, CategorizedJobs, BlogDetails, Blogs
from accounts.views import CustomLogin, CustomSignUp

urlpatterns = [
    path('', index , name='home'),
    path('admin/', admin.site.urls),
    path('all/accounts/', include('allauth.urls')),
    path('sign-in/', CustomLogin.as_view(), name='signIn'),
    path('sign-up/', CustomSignUp.as_view() , name='signUp'),
    path('logout/', SignOut , name='logout'),
    path('account/', Account , name='account'),
    path('about-us/', AboutUs , name='about'),
    path('contact-us/', Contact , name='contact'),
    path('jobs/', Jobs , name='jobs'),
    path('job-detail/<str:pk>/', JobDetails, name='job'),
    path('jobs/category/<str:category>/', CategorizedJobs, name='categorized-jobs'),
    path('blogs/', Blogs, name='blogs'),
    path('blogs/<slug:slug>/', BlogDetails, name='blog'),

    # Debug
    path("__debug__/", include("debug_toolbar.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)