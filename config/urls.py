from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from public.views import index, SignIn, SignUp , Account

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index , name='home'),
    path('sign-in/', SignIn , name='signIn'),
    path('sign-up/', SignUp , name='signUp'),
    path('account', Account , name='account'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)