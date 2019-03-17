from django.urls import path

from app.views import (
    IndexView, ShopView, ShopListView,
    ShopEdit, ShopDelete, DepartmentCreate,
    DepartmentUpdate, DepartmentDelete, ItemCreate,
    ItemUpdate, ItemDelete, ShopFilterView,
    ItemFilterView
)


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('shops/', ShopListView.as_view(), name='shops'),
    path('shop/<int:pk>/', ShopView.as_view(), name='shop'),
    path('shop/<int:pk>/edit', ShopEdit.as_view(), name='shop-update'),
    path('shop/<int:pk>/delete', ShopDelete.as_view(), name='shop-delete'),
    path('dep/<int:shop>/add', DepartmentCreate.as_view(), name='dep-add'),
    path('dep/<int:pk>/edit', DepartmentUpdate.as_view(), name='dep-update'),
    path('dep/<int:pk>/delete', DepartmentDelete.as_view(), name='dep-delete'),
    path('item/add', ItemCreate.as_view(), name='item-add'),
    path('item/<int:pk>/edit', ItemUpdate.as_view(), name='item-update'),
    path('item/<int:pk>/delete', ItemDelete.as_view(), name='item-delete'),
    path('filter/shop/<int:number>/', ShopFilterView.as_view(), name='shop-filter'),
    path('filter/item/<int:number>/', ItemFilterView.as_view(), name='item-filter')
]
