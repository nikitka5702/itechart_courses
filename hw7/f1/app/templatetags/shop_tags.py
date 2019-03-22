from django import template
from django.urls import reverse_lazy
from django.db.models import Sum, Count

register = template.Library()


@register.filter()
def to_int(value):
    return int(value)


@register.filter(name='to_url')
def to_url(shop):
    return reverse_lazy('shop', kwargs={'pk': shop.pk})


@register.inclusion_tag('app/form.html')
def form_tag(form, button_label):
    return {'form': form, 'button_label': button_label}


@register.inclusion_tag('app/deps_table.html')
def get_leader(dep1, dep2, fields):
    stuff = {
        'dep_staff': ('Department staff', dep1.staff_amount, dep2.staff_amount),
        'sold_items_cost': (
            'Sold items cost',
            dep1.items.filter(is_sold=True).aggregate(price=Sum('price'))['price'] or .0,
            dep2.items.filter(is_sold=True).aggregate(price=Sum('price'))['price'] or .0
        ),
        'selling_items_cost': (
            'Selling items cost',
            dep1.items.filter(is_sold=False).aggregate(price=Sum('price'))['price'] or .0,
            dep2.items.filter(is_sold=False).aggregate(price=Sum('price'))['price'] or .0
        ),
        'total_items_cost': (
            'Total items cost',
            dep1.items.aggregate(price=Sum('price'))['price'] or .0,
            dep2.items.aggregate(price=Sum('price'))['price'] or .0
        ),
        'sold_items_count': (
            'Sold items count',
            dep1.items.filter(is_sold=True).aggregate(count=Count('id'))['count'] or .0,
            dep2.items.filter(is_sold=True).aggregate(count=Count('id'))['count'] or .0
        ),
        'selling_items_count': (
            'Selling items count',
            dep1.items.filter(is_sold=False).aggregate(count=Count('id'))['count'] or .0,
            dep2.items.filter(is_sold=False).aggregate(count=Count('id'))['count'] or .0
        ),
        'total_count': (
            'Total count',
            dep1.items.aggregate(count=Count('id'))['count'] or .0,
            dep2.items.aggregate(count=Count('id'))['count'] or .0
        )
    }

    data = []

    for field, value in stuff.items():
        if field in fields:
            name, d1, d2 = value
            data.append((name, d1, d2, d1 > d2))

    return {'data': data}
