from django.views.decorators.cache import cache_page
from functools import wraps


def userBasedCache(timeout):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            return cache_page(timeout, key_prefix="_auth_%s_" % request.user)(view_func)(request, *args, **kwargs)
        return _wrapped_view
    return decorator