from django.http import HttpResponseForbidden
import re


class RestrictIPMiddleware:
    ALLOWED_IPS = ['127.0.0.1']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)

        # / 경로에 대한 모든 요청 허용
        if request.path == '/':
            return self.get_response(request)

        # /api/notices/ 경로에 대한 POST 요청 허용
        if request.path.startswith(
                '/api/notices/') and request.method == 'POST':
            return self.get_response(request)

        # 나머지 API 요청에 대해 IP 제한 적용
        elif ip not in self.ALLOWED_IPS:
            return HttpResponseForbidden(
                f'Access denied: Your IP is not allowed.')

        else:
            return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
