from django.db import models
from django.contrib.postgres import fields


# Create your models here.
class Shop(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True)
    staff_amount = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Shop(name='{self.name}')>"


class Department(models.Model):
    sphere = models.CharField(max_length=255, null=False)
    staff_amount = models.IntegerField(default=0)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='departments')

    def __str__(self):
        return f'{self.sphere}({self.shop})'

    def __repr__(self):
        return f"<Department(sphere='{self.sphere}', shop='{self.shop.name}')>"


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    price = models.IntegerField(default=0)
    is_sold = models.BooleanField(default=False)
    comments = fields.ArrayField(models.CharField(max_length=255), blank=True, default=list)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return f'{self.name} - {self.department}'

    def __repr__(self):
        return f"<Item(name='{self.name}', price={self.price}, is_sold={self.is_sold}, department='{self.department.sphere}')>"
