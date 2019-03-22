from django.db.models import Count
from django.shortcuts import redirect

from app.models import Item, Statistics


class ItemMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        url = request.get_full_path()
        items = Item.objects.filter(is_sold=False).aggregate(count=Count('id'))['count'] or 0
        print(url)
        s, _ = Statistics.objects.get_or_create(url=url)
        s.hit()
        s.save()

        if (url not in ['/admin/', '/info/']) and items == 0:
            return redirect('info')

        response = self.get_response(request)
        return response
