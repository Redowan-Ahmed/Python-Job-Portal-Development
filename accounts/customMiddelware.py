from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.contrib import messages


class DashboardAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        fullPath = request.META.get('PATH_INFO')
        path = str(object=request.META.get('PATH_INFO')).split(sep='/')[1]
        if path == 'dashboard':
            if request.user.is_authenticated:
                return response
            else:
                # Redirect to login page
                messages.error(request=request, message='Please login before accessing the Dashboard!')
                return HttpResponseRedirect(redirect_to=f'/sign-in/?next={fullPath}')
        else:
            return response