from django.urls import path

from app.views import IndexView, ShopView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('shop/<int:pk>', ShopView.as_view(), name='shop')
]
