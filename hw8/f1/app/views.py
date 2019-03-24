from typing import Type

from django.contrib.auth.models import User
from django.db.models import QuerySet, Q
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.serializers import BaseSerializer

from .models import Shop, Department, Item
from .serializers import (
    UserSerializer, AdminShopSerializer, AdminDepartmentSerializer,
    AdminItemSerializer, StaffShopSerializer, StaffDepartmentSerializer,
    StaffItemSerializer, NamelessShopSerializer, NamelessDepartmentSerializer,
    NamelessItemSerializer, AnonymousItemSerializer
)
from .permissions import IsSuper, IsStaff, StaffReadonly, AuthenticatedReadOnly, ReadOnly


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [
        IsSuper | StaffReadonly,
    ]


class ShopViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsSuper | IsStaff | AuthenticatedReadOnly,
    ]

    def get_serializer_class(self) -> Type[BaseSerializer]:
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return AdminShopSerializer
            elif self.request.user.is_staff or (self.request.user.first_name and self.request.user.last_name):
                return StaffShopSerializer
            return NamelessShopSerializer

    def get_queryset(self) -> QuerySet:
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Shop.objects.all()
        return Shop.objects.filter(Q(departments__items__isnull=False) | Q(departments__items__is_sold=False)).distinct().order_by('pk').all()


class DepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsSuper | IsStaff | AuthenticatedReadOnly,
    ]

    def get_serializer_class(self) -> Type[BaseSerializer]:
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return AdminDepartmentSerializer
            elif self.request.user.is_staff or (self.request.user.first_name and self.request.user.last_name):
                return StaffDepartmentSerializer
            return NamelessDepartmentSerializer

    def get_queryset(self) -> QuerySet:
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Department.objects.all()
        return Department.objects.filter(Q(items__isnull=False) | Q(items__is_sold=False)).distinct().order_by('pk').all()


class ItemViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsSuper | IsStaff | AuthenticatedReadOnly | ReadOnly,
    ]

    def get_serializer_class(self) -> Type[BaseSerializer]:
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return AdminItemSerializer
            elif self.request.user.is_staff or (self.request.user.first_name and self.request.user.last_name):
                return StaffItemSerializer
            return NamelessItemSerializer
        return AnonymousItemSerializer

    def get_queryset(self) -> QuerySet:
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser or self.request.user.is_staff:
                return Item.objects.all()
            if self.request.user.first_name and self.request.user.last_name:
                return Item.objects.filter(is_sold=False).all()
        return Item.objects.filter(is_sold=False).all()


class UnsoldItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.filter(is_sold=False).all()
    serializer_class = AdminItemSerializer
    http_method_names = ['get', 'delete']
    permission_classes = [
        IsSuper
    ]
