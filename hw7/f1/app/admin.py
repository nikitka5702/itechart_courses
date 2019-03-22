from django.contrib import admin
from app.models import Shop, Department, Item


# Register your models here.
class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'staff_amount')


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'sphere', 'staff_amount', 'shop')


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_sold', 'department')


admin.site.register(Shop, ShopAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Item, ItemAdmin)
