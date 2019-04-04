from django.shortcuts import redirect

from app.models import Mark


class OverloadMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        url = request.get_full_path()

        if not any(url.startswith(i) for i in ['/admin/', '/info/']) and Mark.objects.count() >= 5:
            return redirect('info')

        response = self.get_response(request)
        return response
