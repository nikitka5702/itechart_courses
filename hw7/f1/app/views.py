from django.db.models import Q, F, Count, Value, When, Case, Sum, Max
from django.views import View
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from app.models import Shop, Department, Item
from app.forms import ShopChooserForm


# Create your views here.
class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/index.html', {'form': ShopChooserForm()})

    def post(self, request, *args, **kwargs):
        form = ShopChooserForm(request.POST or None)

        if form.is_valid():
            shop = form.cleaned_data['shop']
            return redirect('shop', pk=shop.pk)
        return render(request, 'app/index.html', {'form': form})


class ShopListView(ListView):
    model = Shop


class ShopFilterView(ListView):
    model = Shop
    template_name = 'app/shop_filter_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        queries = [
            Shop.objects.annotate(
                department_staff=Sum('departments__staff_amount')
            ).filter(~Q(staff_amount__exact=F('department_staff'))).order_by('pk'),
            Shop.objects.filter(Q(departments__items__price__lt=5)).order_by('pk').distinct(),
            Shop.objects.raw(
                'select s.id, s.name, s.address, s.staff_amount, count(d.id) departments_count, sum(d.staff_amount) department_staff, sq.items_count, sq.max_price  from app_shop s inner join app_department d on s.id = d.shop_id inner join (select s.id, count(i.id) items_count, max(i.price) max_price from app_shop s inner join app_department d on s.id = d.shop_id inner join app_item i on d.id = i.department_id group by s.id) sq on s.id = sq.id group by s.id, s.name, s.address, s.staff_amount, sq.items_count, sq.max_price order by s.id'
            ),
            Shop.objects.raw(
                "select s.id, s.name, s.address, s.staff_amount, count(i.id) items_count from app_shop s inner join app_department ad on s.id = ad.shop_id inner join app_item i on ad.id = i.department_id where i.price <= 10 OR i.name ilike %s group by s.id, s.name, s.address, s.staff_amount", ('%a%', )
            )
        ]
        return super().get_context_data(object_list=queries[self.kwargs.get('number')], **kwargs)


class ShopView(DetailView):
    model = Shop


class ShopEdit(UpdateView):
    model = Shop
    template_name = 'app/update_form.html'
    fields = (
        'name',
        'address'
    )


class ShopDelete(DeleteView):
    model = Shop
    template_name = 'app/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('shops')


class DepartmentCreate(CreateView):
    model = Department
    fields = (
        'sphere',
        'staff_amount'
    )

    def form_valid(self, form):
        shop = get_object_or_404(Shop, pk=self.kwargs.get('shop'))
        form.instance.shop = shop
        return super().form_valid(form)


class DepartmentUpdate(UpdateView):
    model = Department
    template_name = 'app/update_form.html'
    fields = (
        'sphere',
        'staff_amount'
    )


class DepartmentDelete(DeleteView):
    model = Department
    template_name = 'app/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('shop', kwargs={'pk': self.object.shop.pk})


class ItemFilterView(ListView):
    model = Item
    template_name = 'app/item_filter_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        queries = [
            Item.objects.filter(department__shop__name__istartswith='i'),
            Item.objects.filter(Q(price__gt=10) & Q(department__staff_amount__lt=50)),
            Item.objects.filter(Q(price__gt=20) | Q(department__staff_amount__gt=50)),
            Item.objects.filter(department_id__in=[1, 3, 5, 6]),
            Item.objects.filter((Q(price__gt=10) & Q(name__icontains='a')) | (Q(price__lt=20) & Q(name__icontains='o'))),
            Item.objects.filter(Q(price__exact=F('department__staff_amount') + 10))
        ]
        return super().get_context_data(object_list=queries[self.kwargs.get('number')], **kwargs)


class ItemCreate(CreateView):
    model = Item
    fields = (
        'name',
        'description',
        'price',
        'is_sold',
        'comments',
        'department'
    )


class ItemUpdate(UpdateView):
    model = Item
    template_name = 'app/update_form.html'
    fields = (
        'name',
        'description',
        'price',
        'is_sold',
        'comments',
        'department'
    )


class ItemDelete(DeleteView):
    model = Item
    template_name = 'app/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('shop', kwargs={'pk': self.object.department.shop.pk})
