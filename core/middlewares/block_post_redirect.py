from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status


class BlockPostRedirectMiddleware(MiddlewareMixin):
    def process_request(self, request):
        message_error = {
            "errors": [
                {
                    "code": "error",
                    "details": {
                        "message": "URL must end with a slash (/)."
                    }
                }
            ]
        }

        if settings.APPEND_SLASH and request.method == 'POST' and not request.path.endswith('/'):
            return JsonResponse(message_error, status=status.HTTP_400_BAD_REQUEST)
        return None
