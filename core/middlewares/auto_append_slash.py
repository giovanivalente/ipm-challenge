from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class AutoAppendSlashMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if settings.APPEND_SLASH and request.method == 'POST' and not request.path.endswith('/'):
            request.path_info += '/'
