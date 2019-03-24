from django.urls import path, include
from rest_framework import routers

from .views import (
    UserViewSet, ShopViewSet, DepartmentViewSet,
    ItemViewSet, UnsoldItemViewSet
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'shops', ShopViewSet, 'shop')
router.register(r'departments', DepartmentViewSet, 'department')
router.register(r'items', ItemViewSet, 'item')
router.register(r'unsold_items', UnsoldItemViewSet, 'unsold_item')


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
