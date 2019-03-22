from django.db.models import Count

from app.models import Item


def items_processors(request):
    items = Item.objects.filter(is_sold=False).aggregate(count=Count('id'))['count'] or 0
    return {'ITEMS_AMOUNT': items}
