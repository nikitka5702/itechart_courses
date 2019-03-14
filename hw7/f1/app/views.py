from django.views import View
from django.views.generic import DetailView
from django.shortcuts import render, redirect

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


class ShopView(DetailView):
    model = Shop
