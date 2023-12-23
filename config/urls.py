from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from public.views import index, SignIn, SignUp , Account, AboutUs, Contact, Jobs, JobDetails, SignOut

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index , name='home'),
    path('sign-in/', SignIn , name='signIn'),
    path('sign-up/', SignUp , name='signUp'),
    path('logout/', SignOut , name='logout'),
    path('account/', Account , name='account'),
    path('about-us/', AboutUs , name='about'),
    path('contact-us/', Contact , name='contact'),
    path('jobs/', Jobs , name='jobs'),
    path('job-detail/<pk>/', JobDetails, name='job')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)